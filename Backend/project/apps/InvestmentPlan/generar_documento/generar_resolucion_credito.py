"""Genera un acta de resolución del Comité Técnico de Créditos en Word.
Instalar: pip install python-docx
Ejecutar: python generar_resolucion_credito.py
"""
from docx import Document
from docx.shared import Cm, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


def borde_celda(celda, color='333333', grosor=10):
    tcPr = celda._tc.get_or_add_tcPr()
    borders = tcPr.first_child_found_in('w:tcBorders')
    if borders is None:
        borders = OxmlElement('w:tcBorders')
        tcPr.append(borders)
    for lado in ('top', 'left', 'bottom', 'right'):
        tag = 'w:' + lado
        el = borders.find(qn(tag))
        if el is None:
            el = OxmlElement(tag)
            borders.append(el)
        for k, v in {'val': 'single', 'sz': str(grosor), 'color': color}.items():
            el.set(qn('w:' + k), v)


def escribir(celda, texto, negrita=False):
    p = celda.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run(str(texto))
    r.bold = negrita
    r.font.name = 'Courier New'
    r.font.size = Pt(9)
    return p


def fila_texto(doc, izquierda, derecha='', ancho_izq=10):
    tabla = doc.add_table(rows=1, cols=2)
    tabla.autofit = False
    tabla.columns[0].width = Cm(ancho_izq)
    tabla.columns[1].width = Cm(17.5 - ancho_izq)
    escribir(tabla.cell(0, 0), izquierda)
    escribir(tabla.cell(0, 1), derecha)
    return tabla


def caja(doc, contenido, altura_cm=2.8):
    tabla = doc.add_table(rows=1, cols=1)
    tabla.autofit = False
    tabla.columns[0].width = Cm(17.5)
    celda = tabla.cell(0, 0)
    celda.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.TOP
    borde_celda(celda)
    if isinstance(contenido, dict):
        for i, (etiqueta, valor) in enumerate(contenido.items()):
            p = celda.paragraphs[0] if i == 0 else celda.add_paragraph()
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(f'   {etiqueta}:  {valor}')
            r.font.name = 'Courier New'
            r.font.size = Pt(9)
    else:
        p = celda.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(str(contenido) if contenido else ' ')
        r.font.name = 'Courier New'
        r.font.size = Pt(9)
    from docx.enum.table import WD_ROW_HEIGHT_RULE
    tabla.rows[0].height = Cm(altura_cm)
    tabla.rows[0].height_rule = WD_ROW_HEIGHT_RULE.AT_LEAST
    return tabla


def espacio(doc, puntos=10):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.space_before = Pt(0)
    p.add_run(' ').font.size = Pt(puntos)


def generar_resolucion_credito(datos, ruta='resolucion_credito.docx'):
    """datos: diccionario con fecha, acta, asociado, calidad_asociado, estado,
    descripcion, monto, destino, plazo, forma_pago, tasa_interes, desembolso,
    fecha_primer_pago, garantia, otras_condiciones, firmas, numero_asociado.
    """
    doc = Document()
    sec = doc.sections[0]
    sec.page_height, sec.page_width = Cm(29.7), Cm(21)
    sec.top_margin = Cm(1.25)
    sec.bottom_margin = Cm(1.2)
    sec.left_margin = sec.right_margin = Cm(1.75)
    normal = doc.styles['Normal']
    normal.font.name = 'Courier New'
    normal.font.size = Pt(9)

    for titulo in ('INVERSIONES INTEGRALES EL TELAR S.A.', 'RESOLUCIÓN', 'COMITÉ TÉCNICO DE CRÉDITOS'):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(1)
        r = p.add_run(titulo)
        r.font.name = 'Courier New'
        r.font.size = Pt(9)
        r.bold = True

    espacio(doc, 12)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p.add_run(f"No. Asociado: {datos.get('numero_asociado', '________________')}")
    fila_texto(doc, f"Fecha: {datos.get('fecha', '')}", f"ACTA: {datos.get('acta', '')}")
    espacio(doc, 7)
    fila_texto(doc, f"A nombre de: {datos.get('asociado', '')}", f"Calidad de Asociado: {datos.get('calidad_asociado', '')}")
    espacio(doc, 7)
    doc.add_paragraph(f"Estado: {datos.get('estado', '')}")
    doc.add_paragraph(f"Descripción: {datos.get('descripcion', '')}")

    caja(doc, {
        'Monto': datos.get('monto', ''),
        'Destino': datos.get('destino', ''),
        'Plazo': datos.get('plazo', ''),
        'Forma de Pago': datos.get('forma_pago', ''),
        'Tasa de Interés': datos.get('tasa_interes', ''),
        'Desembolso': datos.get('desembolso', ''),
        'Fecha de Primer Pago': datos.get('fecha_primer_pago', ''),
    }, 4.4)

    espacio(doc, 11)
    doc.add_paragraph('Garantía:')
    caja(doc, datos.get('garantia', ''), 3.3)
    espacio(doc, 11)
    doc.add_paragraph('Otras Condiciones:')
    caja(doc, datos.get('otras_condiciones', ''), 3.3)
    espacio(doc, 18)
    fila_texto(doc, '       __________________', '       __________________')
    fila_texto(doc, f"       {datos.get('firma_1', 'Firma')}", f"       {datos.get('firma_2', 'Firma')}")
    doc.save(ruta)
    return ruta


if __name__ == '__main__':
    ejemplo = {
        'numero_asociado': '00125', 'fecha': '21/10/2026', 'acta': '25-2026',
        'asociado': 'NOMBRE DEL CLIENTE', 'calidad_asociado': 'Activo',
        'estado': 'APROBADO', 'descripcion': 'Crédito para capital de trabajo.',
        'monto': 'Q 15,000.00', 'destino': 'Capital de trabajo',
        'plazo': '12 meses', 'forma_pago': 'Mensual', 'tasa_interes': '18% anual',
        'desembolso': 'Q 15,000.00', 'fecha_primer_pago': '21/11/2026',
        'garantia': 'Garantía fiduciaria respaldada por fiador.',
        'otras_condiciones': 'Sujeto a verificación documental.',
        'firma_1': 'Firma', 'firma_2': 'Firma',
    }
    print(generar_resolucion_credito(ejemplo))
