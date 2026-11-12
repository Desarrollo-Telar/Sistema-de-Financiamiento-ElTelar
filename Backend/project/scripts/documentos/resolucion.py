"""
Módulo para la generación de la RESOLUCIÓN DEL COMITÉ TÉCNICO DE CRÉDITOS
en formato Word (.docx).
Diseñado para Inversiones Integrales El Telar S.A., compatible tanto con llamadas
directas (diccionario de datos) como extrayendo automáticamente la información
desde una Solicitud de Crédito (InvestmentPlan) o Crédito (Credit).
"""

import io
from datetime import date, datetime
from decimal import Decimal

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT, WD_ROW_HEIGHT_RULE
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

from .helpers import (
    formato_quetzales,
    resolver_solicitud_o_credito,
    obtener_tasa_mensual_porcentaje,
    construir_texto_garantia_item,
    generar_cuotas_para_contrato,
    sumar_meses_seguro,
    cui_dpi_a_letras,
)


COLOR_BORDE_HEX = "1E293B"
COLOR_FONDO_SUAVE_HEX = "F8FAFC"
COLOR_TITULO_RGB = RGBColor(15, 23, 42)
COLOR_TEXTO_RGB = RGBColor(30, 41, 59)
COLOR_ETIQUETA_RGB = RGBColor(51, 65, 85)


def obtener_datos_ejemplo_resolucion() -> dict:
    """
    Retorna un diccionario con la estructura completa de datos de ejemplo
    para la Resolución del Comité Técnico de Créditos de El Telar S.A.
    """
    return {
        "empresa_nombre": "INVERSIONES INTEGRALES EL TELAR S.A.",
        "titulo_documento": "RESOLUCIÓN",
        "subtitulo_comite": "COMITÉ TÉCNICO DE CRÉDITOS",
        "codigo_cliente": "2026-1",
        "codigo_solicitud": "01-IIT01-2026",
        "fecha": "11/11/2026",
        "acta": "045-2026",
        "cliente_nombre": "CANDY CLARAMARÍA CANTORAL CAAL DE PAPA",
        "calidad_cliente": "RECURRENTE",
        "estado": "ACEPTADO",
        "monto": "Q. 39,634.00",
        "destino": "COMERCIO - Comercio y capital de trabajo",
        "plazo": "12 meses",
        "forma_pago": "AMORTIZACIONES A CAPITAL",
        "tasa_interes": "10% mensual",
        "desembolso": "Q. 39,634.00 (Desembolso único)",
        "fecha_primer_pago": "11/12/2026",
        "garantia": (
            "1. [MOBILIARIA - Cobertura: Q. 50,000.00] Garantía mobiliaria sobre la empresa mercantil "
            "Comercial Agrícola W&A, inscrita en el Registro Mercantil bajo el número 1002212, folio 401, libro 1182.\n"
            "2. [FIADOR SOLIDARIO] FREDY JOEL GARCÍA MOSCOSO | DPI: 3268 85188 1604 | "
            "Lugar de trabajo/negocio: Comercial Agrícola W&A."
        ),
        "otras_condiciones": (
            "• Tipo de documento legal: CONTRATO | Pagaré: Normal.\n"
            "• Cumplir con la entrega de documentación completa previa al desembolso."
        ),
        "firma_1": "Firma",
        "firma_2": "Firma",
    }


def _formatear_fecha_corta(valor) -> str:
    """Formatea una fecha date/datetime/ISO string a dd/mm/yyyy."""
    if not valor:
        return ""
    if isinstance(valor, datetime):
        return valor.strftime("%d/%m/%Y")
    if isinstance(valor, date):
        return valor.strftime("%d/%m/%Y")
    if isinstance(valor, str):
        limpio = valor.strip()
        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
            try:
                return datetime.strptime(limpio[:10], fmt).strftime("%d/%m/%Y")
            except ValueError:
                continue
        return limpio
    return str(valor)


def _aplicar_borde_pagina(section, color: str = COLOR_BORDE_HEX, grosor: int = 12, espacio: int = 18):
    """Agrega un marco exterior limpio a la hoja respetando el orden OOXML en w:sectPr."""
    sectPr = section._sectPr
    prev = sectPr.find(qn("w:pgBorders"))
    if prev is not None:
        sectPr.remove(prev)

    pgBorders = OxmlElement("w:pgBorders")
    pgBorders.set(qn("w:offsetFrom"), "text")
    for lado in ("top", "left", "bottom", "right"):
        borde = OxmlElement(f"w:{lado}")
        borde.set(qn("w:val"), "single")
        borde.set(qn("w:sz"), str(grosor))
        borde.set(qn("w:space"), str(espacio))
        borde.set(qn("w:color"), color)
        pgBorders.append(borde)

    pgMar = sectPr.find(qn("w:pgMar"))
    if pgMar is not None:
        idx = list(sectPr).index(pgMar)
        sectPr.insert(idx + 1, pgBorders)
    else:
        sectPr.append(pgBorders)


def _quitar_bordes_tabla(tabla):
    """Elimina todos los bordes visibles de una tabla usada únicamente para maquetación."""
    tblPr = tabla._tbl.tblPr
    prev = tblPr.find(qn("w:tblBorders"))
    if prev is not None:
        tblPr.remove(prev)

    tblBorders = OxmlElement("w:tblBorders")
    for lado in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{lado}")
        el.set(qn("w:val"), "none")
        tblBorders.append(el)
    tblPr.append(tblBorders)


def _aplicar_bordes_celda(celda, lados: dict | None = None, color: str = COLOR_BORDE_HEX, grosor: int = 8):
    """Configura bordes individuales o completos en una celda de tabla."""
    tcPr = celda._tc.get_or_add_tcPr()
    prev = tcPr.find(qn("w:tcBorders"))
    if prev is not None:
        tcPr.remove(prev)

    tcBorders = OxmlElement("w:tcBorders")
    config = lados or {
        "top": ("single", grosor, color),
        "left": ("single", grosor, color),
        "bottom": ("single", grosor, color),
        "right": ("single", grosor, color),
    }
    for lado in ("top", "left", "bottom", "right"):
        el = OxmlElement(f"w:{lado}")
        if lado in config and config[lado] is not None:
            val, sz, col = config[lado]
            el.set(qn("w:val"), val)
            el.set(qn("w:sz"), str(sz))
            el.set(qn("w:space"), "0")
            el.set(qn("w:color"), col)
        else:
            el.set(qn("w:val"), "none")
        tcBorders.append(el)
    tcPr.append(tcBorders)


def _aplicar_padding_celda(celda, top: int = 90, bottom: int = 90, left: int = 160, right: int = 160):
    """Define márgenes internos (en dxa: 1/20 pt) para dar respiro visual dentro de una caja."""
    tcPr = celda._tc.get_or_add_tcPr()
    prev = tcPr.find(qn("w:tcMar"))
    if prev is not None:
        tcPr.remove(prev)

    tcMar = OxmlElement("w:tcMar")
    for lado, valor in (("top", top), ("bottom", bottom), ("left", left), ("right", right)):
        el = OxmlElement(f"w:{lado}")
        el.set(qn("w:w"), str(valor))
        el.set(qn("w:type"), "dxa")
        tcMar.append(el)
    tcPr.append(tcMar)


def _aplicar_sombreado_celda(celda, color_hex: str = COLOR_FONDO_SUAVE_HEX):
    """Aplica color de fondo sutil a una celda."""
    tcPr = celda._tc.get_or_add_tcPr()
    prev = tcPr.find(qn("w:shd"))
    if prev is not None:
        tcPr.remove(prev)

    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), color_hex)
    tcPr.append(shd)


def _evitar_salto_fila(row):
    """Marca una fila para no dividirse a la mitad entre dos páginas."""
    trPr = row._tr.get_or_add_trPr()
    if trPr.find(qn("w:cantSplit")) is None:
        trPr.append(OxmlElement("w:cantSplit"))


def _normalizar_lineas(valor) -> list[str]:
    """Convierte str o list en lista limpia de líneas no vacías."""
    if not valor:
        return []
    if isinstance(valor, (list, tuple)):
        return [str(v).strip() for v in valor if str(v).strip()]
    return [line.strip() for line in str(valor).splitlines() if line.strip()]


def _preparar_datos_resolucion(datos_entrada: dict | None) -> dict:
    """Combina los datos de entrada con valores base por defecto para renderizado seguro."""
    datos = obtener_datos_ejemplo_resolucion()
    if datos_entrada and isinstance(datos_entrada, dict):
        datos.update(datos_entrada)

    # Normalizar monto si llega numérico en lugar de formateado
    monto_val = datos.get("monto")
    if isinstance(monto_val, (int, float, Decimal)):
        datos["monto"] = f"Q. {float(monto_val):,.2f}"

    return datos


def _crear_caja_texto_libre(doc, etiqueta: str, contenido, altura_pulgadas: float = 1.45):
    """
    Renderiza una sección con etiqueta externa superior y un recuadro con borde completo,
    fiel al diseño de 'Garantia' y 'Otras Condiciones'.
    """
    p_lbl = doc.add_paragraph()
    p_lbl.paragraph_format.space_before = Pt(7)
    p_lbl.paragraph_format.space_after = Pt(2)
    r_lbl = p_lbl.add_run(etiqueta)
    r_lbl.bold = True
    r_lbl.font.size = Pt(10)
    r_lbl.font.color.rgb = COLOR_TITULO_RGB

    tabla = doc.add_table(rows=1, cols=1)
    tabla.alignment = WD_TABLE_ALIGNMENT.CENTER
    tabla.autofit = False
    tabla.columns[0].width = Inches(7.0)
    _evitar_salto_fila(tabla.rows[0])

    tabla.rows[0].height = Inches(altura_pulgadas)
    tabla.rows[0].height_rule = WD_ROW_HEIGHT_RULE.AT_LEAST

    celda = tabla.cell(0, 0)
    celda.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.TOP
    _aplicar_bordes_celda(celda, color=COLOR_BORDE_HEX, grosor=8)
    _aplicar_padding_celda(celda, top=90, bottom=90, left=160, right=160)

    lineas = _normalizar_lineas(contenido)
    if not lineas:
        p = celda.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        p.add_run(" ")
        return tabla

    for idx, linea in enumerate(lineas):
        p = celda.paragraphs[0] if idx == 0 else celda.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(linea)
        r.font.size = Pt(9.5)
        r.font.color.rgb = COLOR_TEXTO_RGB

    return tabla


def generar_resolucion_word(datos_entrada: dict | None = None, output_target=None):
    """
    Genera el archivo Word (.docx) de la Resolución del Comité Técnico de Créditos.

    Parámetros:
    -----------
    datos_entrada: dict | None
        Diccionario con los campos de la resolución (ver obtener_datos_ejemplo_resolucion()).
    output_target: io.BytesIO | str | None
        Ruta de archivo o stream donde guardar el .docx. Si es None, retorna io.BytesIO.
    """
    datos = _preparar_datos_resolucion(datos_entrada)

    doc = Document()
    for section in doc.sections:
        section.page_width = Inches(8.5)
        section.page_height = Inches(11.0)
        section.top_margin = Inches(0.65)
        section.bottom_margin = Inches(0.65)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)
        _aplicar_borde_pagina(section)

    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(10)
    style.font.color.rgb = COLOR_TEXTO_RGB

    # =========================================================================
    # 1. ENCABEZADO INSTITUCIONAL CENTRADO
    # =========================================================================
    encabezados = [
        (datos.get("empresa_nombre", "INVERSIONES INTEGRALES EL TELAR S.A."), 11.5, 1),
        (datos.get("titulo_documento", "RESOLUCIÓN"), 11.0, 1),
        (datos.get("subtitulo_comite", "COMITÉ TÉCNICO DE CRÉDITOS"), 10.5, 6),
    ]
    for texto, pt_size, sp_after in encabezados:
        p_h = doc.add_paragraph()
        p_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_h.paragraph_format.space_before = Pt(0)
        p_h.paragraph_format.space_after = Pt(sp_after)
        r_h = p_h.add_run(str(texto).upper())
        r_h.bold = True
        r_h.font.size = Pt(pt_size)
        r_h.font.color.rgb = COLOR_TITULO_RGB

    # =========================================================================
    # 2. CÓDIGO DE CLIENTE (ALINEADO A LA DERECHA SOBRE LÍNEA)
    # =========================================================================
    tabla_cod = doc.add_table(rows=1, cols=3)
    tabla_cod.alignment = WD_TABLE_ALIGNMENT.CENTER
    tabla_cod.autofit = False
    _quitar_bordes_tabla(tabla_cod)
    anchos_cod = (Inches(4.35), Inches(1.25), Inches(1.40))
    for idx_w, w in enumerate(anchos_cod):
        tabla_cod.columns[idx_w].width = w
        tabla_cod.cell(0, idx_w).width = w

    p_cod_lbl = tabla_cod.cell(0, 1).paragraphs[0]
    p_cod_lbl.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_cod_lbl.paragraph_format.space_after = Pt(2)
    r_cod_lbl = p_cod_lbl.add_run("Código Cliente:")
    r_cod_lbl.bold = True
    r_cod_lbl.font.size = Pt(9.5)
    r_cod_lbl.font.color.rgb = COLOR_ETIQUETA_RGB

    c_cod_val = tabla_cod.cell(0, 2)
    _aplicar_bordes_celda(c_cod_val, lados={"bottom": ("single", 6, COLOR_BORDE_HEX)})
    _aplicar_padding_celda(c_cod_val, top=10, bottom=20, left=40, right=40)
    p_cod_val = c_cod_val.paragraphs[0]
    p_cod_val.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cod_val.paragraph_format.space_after = Pt(1)
    r_cod_val = p_cod_val.add_run(str(datos.get("codigo_cliente") or " "))
    r_cod_val.bold = True
    r_cod_val.font.size = Pt(9.5)
    r_cod_val.font.color.rgb = COLOR_TITULO_RGB

    p_sep = doc.add_paragraph()
    p_sep.paragraph_format.space_before = Pt(2)
    p_sep.paragraph_format.space_after = Pt(2)

    # =========================================================================
    # 3. DATOS GENERALES (Fecha, ACTA, A nombre de, Calidad de Cliente, Estado)
    # =========================================================================
    tabla_meta = doc.add_table(rows=3, cols=3)
    tabla_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    tabla_meta.autofit = False
    _quitar_bordes_tabla(tabla_meta)

    anchos_meta = (Inches(4.05), Inches(1.45), Inches(1.50))
    for row in tabla_meta.rows:
        _evitar_salto_fila(row)
        for idx_w, w in enumerate(anchos_meta):
            row.cells[idx_w].width = w
            _aplicar_padding_celda(row.cells[idx_w], top=40, bottom=40, left=30, right=40)
    for idx_w, w in enumerate(anchos_meta):
        tabla_meta.columns[idx_w].width = w

    def _escribir_par(celda, etiqueta: str, valor: str, negrita_val: bool = False):
        p = celda.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(1)
        r1 = p.add_run(f"{etiqueta} ")
        r1.bold = True
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = COLOR_ETIQUETA_RGB
        r2 = p.add_run(str(valor or ""))
        r2.bold = negrita_val
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = COLOR_TITULO_RGB if negrita_val else COLOR_TEXTO_RGB

    # Fila 0: Fecha | ACTA (celdas 1 y 2 unidas)
    _escribir_par(tabla_meta.cell(0, 0), "Fecha:", datos.get("fecha", ""))
    celda_acta = tabla_meta.cell(0, 1).merge(tabla_meta.cell(0, 2))
    celda_acta.width = anchos_meta[1] + anchos_meta[2]
    _escribir_par(celda_acta, "ACTA:", datos.get("acta", "________________"))

    # Fila 1: A nombre de | Calidad de Cliente | [ Recuadro Calidad ]
    _escribir_par(tabla_meta.cell(1, 0), "A nombre de:", datos.get("cliente_nombre", ""), negrita_val=True)
    c_cal_lbl = tabla_meta.cell(1, 1)
    c_cal_lbl.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    p_cal_lbl = c_cal_lbl.paragraphs[0]
    p_cal_lbl.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_cal_lbl.paragraph_format.space_after = Pt(0)
    r_cal_lbl = p_cal_lbl.add_run("Calidad de Cliente:")
    r_cal_lbl.bold = True
    r_cal_lbl.font.size = Pt(9.0)
    r_cal_lbl.font.color.rgb = COLOR_ETIQUETA_RGB

    c_cal_box = tabla_meta.cell(1, 2)
    c_cal_box.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    _aplicar_bordes_celda(c_cal_box, color=COLOR_BORDE_HEX, grosor=8)
    _aplicar_sombreado_celda(c_cal_box, COLOR_FONDO_SUAVE_HEX)
    _aplicar_padding_celda(c_cal_box, top=35, bottom=35, left=60, right=60)
    p_cal_val = c_cal_box.paragraphs[0]
    p_cal_val.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cal_val.paragraph_format.space_after = Pt(0)
    r_cal_val = p_cal_val.add_run(str(datos.get("calidad_cliente", "") or " ").upper())
    r_cal_val.bold = True
    r_cal_val.font.size = Pt(9.0)
    r_cal_val.font.color.rgb = COLOR_TITULO_RGB

    # Fila 2: Estado | (Opcional referencia código solicitud discreta)
    _escribir_par(tabla_meta.cell(2, 0), "Estado:", str(datos.get("estado", "")).upper(), negrita_val=True)

    # =========================================================================
    # 4. CAJA 1: DESCRIPCIÓN (CON LOS 7 CAMPOS INDENTADOS DEL DISEÑO)
    # =========================================================================
    p_desc_lbl = doc.add_paragraph()
    p_desc_lbl.paragraph_format.space_before = Pt(7)
    p_desc_lbl.paragraph_format.space_after = Pt(2)
    r_desc_lbl = p_desc_lbl.add_run("Descripción:")
    r_desc_lbl.bold = True
    r_desc_lbl.font.size = Pt(10)
    r_desc_lbl.font.color.rgb = COLOR_TITULO_RGB

    tabla_desc = doc.add_table(rows=1, cols=1)
    tabla_desc.alignment = WD_TABLE_ALIGNMENT.CENTER
    tabla_desc.autofit = False
    tabla_desc.columns[0].width = Inches(7.0)
    _evitar_salto_fila(tabla_desc.rows[0])
    tabla_desc.rows[0].height = Inches(1.85)
    tabla_desc.rows[0].height_rule = WD_ROW_HEIGHT_RULE.AT_LEAST

    c_desc = tabla_desc.cell(0, 0)
    c_desc.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.TOP
    _aplicar_bordes_celda(c_desc, color=COLOR_BORDE_HEX, grosor=8)
    _aplicar_padding_celda(c_desc, top=110, bottom=110, left=220, right=180)

    campos_descripcion = [
        ("Monto:", datos.get("monto", "")),
        ("Destino:", datos.get("destino", "")),
        ("Plazo:", datos.get("plazo", "")),
        ("Forma de Pago:", datos.get("forma_pago", "")),
        ("Tasa de Interés:", datos.get("tasa_interes", "")),
       
        ("Fecha de Primer Pago:", datos.get("fecha_primer_pago", "")),
    ]
    for idx, (lbl, val) in enumerate(campos_descripcion):
        p = c_desc.paragraphs[0] if idx == 0 else c_desc.add_paragraph()
        p.paragraph_format.left_indent = Inches(2.05)
        p.paragraph_format.first_line_indent = Inches(-1.75)
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.tab_stops.add_tab_stop(Inches(2.05))

        r_l = p.add_run(f"{lbl}\t")
        r_l.bold = True
        r_l.font.size = Pt(9.5)
        r_l.font.color.rgb = COLOR_ETIQUETA_RGB

        r_v = p.add_run(str(val or "—"))
        r_v.font.size = Pt(9.5)
        r_v.font.color.rgb = COLOR_TITULO_RGB if idx == 0 else COLOR_TEXTO_RGB
        r_v.bold = idx == 0

    # =========================================================================
    # 5. CAJA 2: GARANTÍA
    # =========================================================================
    _crear_caja_texto_libre(doc, "Garantía:", datos.get("garantia", ""), altura_pulgadas=1.55)

    # =========================================================================
    # 6. CAJA 3: OTRAS CONDICIONES
    # =========================================================================
    _crear_caja_texto_libre(doc, "Otras Condiciones:", datos.get("otras_condiciones", ""), altura_pulgadas=1.45)

    # =========================================================================
    # 7. PIE DE FIRMAS (2 FIRMAS: IZQUIERDA Y DERECHA)
    # =========================================================================
    p_esp = doc.add_paragraph()
    p_esp.paragraph_format.space_before = Pt(18)
    p_esp.paragraph_format.space_after = Pt(4)

    tabla_firmas = doc.add_table(rows=1, cols=2)
    tabla_firmas.alignment = WD_TABLE_ALIGNMENT.CENTER
    tabla_firmas.autofit = False
    _quitar_bordes_tabla(tabla_firmas)
    _evitar_salto_fila(tabla_firmas.rows[0])
    tabla_firmas.columns[0].width = Inches(3.5)
    tabla_firmas.columns[1].width = Inches(3.5)

    for col_idx, clave_firma in ((0, "firma_1"), (1, "firma_2")):
        celda_f = tabla_firmas.cell(0, col_idx)
        celda_f.width = Inches(3.5)
        p_f = celda_f.paragraphs[0]
        p_f.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_f.paragraph_format.space_before = Pt(8)
        p_f.paragraph_format.space_after = Pt(0)

        r_lin = p_f.add_run("____________________________\n")
        r_lin.bold = True
        r_lin.font.size = Pt(9.5)
        r_lin.font.color.rgb = COLOR_TITULO_RGB

        r_txt = p_f.add_run(str(datos.get(clave_firma) or "Firma"))
        r_txt.bold = True
        r_txt.font.size = Pt(9.5)
        r_txt.font.color.rgb = COLOR_ETIQUETA_RGB

    # GUARDAR O RETORNAR STREAM
    if isinstance(output_target, str):
        doc.save(output_target)
        return output_target
    if output_target is not None and hasattr(output_target, "write"):
        doc.save(output_target)
        return output_target

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer


def _determinar_calidad_cliente(solicitud, cliente) -> str:
    """Determina si el solicitante es cliente NUEVO, RECURRENTE o en REESTRUCTURACIÓN."""
    tipo_pagare = str(getattr(solicitud, "tipo_pagare", "") or "").strip().lower()
    credito_ant = getattr(solicitud, "credito_anterior_vigente", None)

    if tipo_pagare == "restructuracion" or credito_ant:
        return "RECURRENTE"

    if cliente is None:
        return "NUEVO"

    # Consultar historial real de créditos/solicitudes previas en ORM si está disponible
    try:
        from apps.financings.models import Credit
        sol_id = getattr(solicitud, "id", None)
        es_sol = hasattr(solicitud, "total_value_of_the_product_or_service") or hasattr(solicitud, "investment_plan_code")
        qs_cred = Credit.objects.filter(customer_id=cliente)
        if es_sol and sol_id:
            qs_cred = qs_cred.exclude(destino_id_id=sol_id)
        elif not es_sol and sol_id:
            qs_cred = qs_cred.exclude(id=sol_id)
        if qs_cred.exists():
            return "RECURRENTE"
    except Exception:
        pass

    try:
        from apps.InvestmentPlan.models import InvestmentPlan
        sol_id = getattr(solicitud, "id", None)
        qs_plan = InvestmentPlan.objects.filter(customer_id=cliente)
        if sol_id:
            qs_plan = qs_plan.exclude(id=sol_id)
        if qs_plan.exists():
            return "RECURRENTE"
    except Exception:
        pass

    return "NUEVO"


def _obtener_resumen_desembolso(solicitud, capital: float) -> str:
    """Obtiene la descripción de desembolso desde Disbursement real, reestructuración o monto autorizado."""
    monto_txt = formato_quetzales(capital).replace("Q.", "Q. ")

    # 1. Consultar Disbursement reales si ya existe un Credit asociado o es instancia de Credit
    try:
        from apps.financings.models import Credit, Disbursement
        credit_obj = None
        if not hasattr(solicitud, "total_value_of_the_product_or_service"):
            credit_obj = solicitud
        elif getattr(solicitud, "id", None):
            credit_obj = Credit.objects.filter(destino_id=solicitud).first()

        if credit_obj is not None:
            desembolsos = list(Disbursement.objects.filter(credit_id=credit_obj).order_by("pk"))
            if desembolsos:
                formas = []
                total_neto = 0.0
                for d in desembolsos:
                    forma = str(getattr(d, "forma_desembolso", "") or "").strip()
                    if forma and forma not in formas:
                        formas.append(forma)
                    neto = float(getattr(d, "monto_total_desembolso", 0) or getattr(d, "monto_desembolsado", 0) or 0)
                    total_neto += neto
                formas_str = ", ".join(formas) if formas else "Desembolso registrado"
                if total_neto > 0:
                    return f"Q. {total_neto:,.2f} ({formas_str})"
                return f"{monto_txt} ({formas_str})"
    except Exception:
        pass

    # 2. Si es reestructuración o cancelación de crédito anterior en la solicitud
    cred_ant = getattr(solicitud, "credito_anterior_vigente", None)
    tipo_pagare = str(getattr(solicitud, "tipo_pagare", "") or "").strip()
    if cred_ant or tipo_pagare.lower() == "restructuracion":
        return f"{monto_txt} (Aplicación / Reestructuración de crédito vigente)"

    # 3. Valor por defecto de solicitud aprobada pendiente de desembolso
    return f"{monto_txt} (Desembolso único)"


def _construir_resumen_garantias_solicitud(solicitud) -> str:
    """Extrae y formatea todas las garantías y fiadores de la solicitud para el recuadro de Garantía."""
    lineas = []

    garantias_raw = getattr(solicitud, "garantias", None)
    if not garantias_raw and getattr(solicitud, "destino_id", None) is not None:
        garantias_raw = getattr(solicitud.destino_id, "garantias", None)
    if not isinstance(garantias_raw, list):
        garantias_raw = []

    # 1. Garantías de bienes / hipotecas / cheques / laborales / mobiliarias
    idx_g = 0
    for g in garantias_raw:
        if not isinstance(g, dict):
            continue
        tipo = str(g.get("tipo") or g.get("tipo_garantia") or "").strip().upper()
        if tipo == "FIADOR":
            continue
        idx_g += 1
        specs = g.get("especificaciones") if isinstance(g.get("especificaciones"), dict) else {}
        desc = str(g.get("descripcion") or "").strip()
        txt_g = construir_texto_garantia_item(tipo or "MOBILIARIA", specs, desc)
        if txt_g:
            txt_g = txt_g[0].upper() + txt_g[1:]

        valor = g.get("valor") or g.get("valor_cobertura")
        valor_str = ""
        if valor:
            try:
                valor_str = f" - Cobertura: Q. {float(valor):,.2f}"
            except (ValueError, TypeError):
                valor_str = ""

        lineas.append(f"{idx_g}. [{tipo or 'GARANTÍA'}{valor_str}] {txt_g}.")

    # 2. Si es Credit sin garantías JSON en el plan, revisar DetailsGuarantees
    if idx_g == 0 and not hasattr(solicitud, "total_value_of_the_product_or_service") and getattr(solicitud, "id", None):
        try:
            from apps.financings.models import DetailsGuarantees
            detalles = DetailsGuarantees.objects.filter(
                garantia_id__credit_id=solicitud
            ).exclude(tipo_garantia="FIADOR").order_by("pk")
            for det in detalles:
                idx_g += 1
                tg = str(det.tipo_garantia or "GARANTÍA").strip().upper()
                specs = det.especificaciones if isinstance(det.especificaciones, dict) else {}
                txt_g = construir_texto_garantia_item(tg, specs, "")
                if txt_g:
                    txt_g = txt_g[0].upper() + txt_g[1:]
                val_cov = getattr(det, "valor_cobertura", None)
                val_str = f" - Cobertura: Q. {float(val_cov):,.2f}" if val_cov else ""
                lineas.append(f"{idx_g}. [{tg}{val_str}] {txt_g}.")
        except Exception:
            pass

    # 3. Fiadores solidarios (desde solicitud.fiador + garantias tipo FIADOR + DetailsGuarantees)
    vistos_cod = set()
    vistos_nom = set()

    def _agregar_fiador_linea(nombre: str, dpi: str = "", trabajo: str = "", cod: str = ""):
        nonlocal idx_g
        nom_norm = nombre.strip().upper()
        if not nom_norm:
            return
        if cod and cod in vistos_cod:
            return
        if nom_norm in vistos_nom:
            return
        if cod:
            vistos_cod.add(cod)
        vistos_nom.add(nom_norm)

        idx_g += 1
        partes = [f"{idx_g}. [FIADOR SOLIDARIO] {nom_norm}"]
        if dpi:
            _, dpi_f = cui_dpi_a_letras(dpi, con_espacio=True)
            partes.append(f"DPI: {dpi_f or dpi}")
        if trabajo and trabajo.upper() not in ("N/A", "---", "NONE"):
            partes.append(f"Lugar de trabajo/negocio: {trabajo}")
        lineas.append(" | ".join(partes) + ".")

    # Mapa auxiliar de especificaciones en garantias FIADOR
    specs_fiador_por_cod = {}
    garantias_fiador = []
    for g in garantias_raw:
        if isinstance(g, dict) and str(g.get("tipo") or g.get("tipo_garantia") or "").strip().upper() == "FIADOR":
            garantias_fiador.append(g)
            sp = g.get("especificaciones") if isinstance(g.get("especificaciones"), dict) else {}
            cod_sp = str(sp.get("Codigo_de_Cliente") or "").strip()
            if cod_sp:
                specs_fiador_por_cod[cod_sp] = sp

    raw_fiadores = getattr(solicitud, "fiador", None)
    if not raw_fiadores and getattr(solicitud, "destino_id", None) is not None:
        raw_fiadores = getattr(solicitud.destino_id, "fiador", None)
    if isinstance(raw_fiadores, dict):
        raw_fiadores = [raw_fiadores]
    elif isinstance(raw_fiadores, int):
        raw_fiadores = [{"id": raw_fiadores}]
    elif not isinstance(raw_fiadores, (list, tuple)):
        raw_fiadores = []

    for f_entry in raw_fiadores:
        cust_obj = None
        f_id = None
        sp_dict = {}

        if isinstance(f_entry, dict):
            f_id = f_entry.get("id") or f_entry.get("customer_id")
            sp_dict = f_entry
            if f_id:
                try:
                    from apps.customers.models import Customer
                    cust_obj = Customer.objects.filter(id=f_id).first()
                except Exception:
                    cust_obj = None
        elif isinstance(f_entry, int):
            f_id = f_entry
            try:
                from apps.customers.models import Customer
                cust_obj = Customer.objects.filter(id=f_id).first()
            except Exception:
                cust_obj = None
        elif hasattr(f_entry, "first_name") or hasattr(f_entry, "get_full_name") or hasattr(f_entry, "identification_number"):
            cust_obj = f_entry

        if cust_obj is not None:
            cod_c = str(getattr(cust_obj, "customer_code", "") or "").strip()
            nom_c = (
                cust_obj.get_full_name() if callable(getattr(cust_obj, "get_full_name", None))
                else f"{getattr(cust_obj, 'first_name', '')} {getattr(cust_obj, 'last_name', '')}"
            ).strip()
            dpi_c = str(getattr(cust_obj, "identification_number", "") or "").strip()
            sp_extra = specs_fiador_por_cod.get(cod_c) or sp_dict
            trab = str(sp_extra.get("Lugar_de_Trabajo") or sp_extra.get("lugar_trabajo") or "").strip()
            if not trab:
                wi = getattr(cust_obj, "_mock_working_info", None)
                if wi is None:
                    try:
                        from apps.FinancialInformation.models import WorkingInformation
                        wi = WorkingInformation.objects.filter(customer_id=cust_obj).first()
                    except Exception:
                        wi = None
                if wi is not None:
                    trab = str(getattr(wi, "company_name", "") or "").strip()
            _agregar_fiador_linea(nom_c, dpi=dpi_c, trabajo=trab, cod=cod_c)
        elif sp_dict and (sp_dict.get("nombre") or sp_dict.get("Nombre") or sp_dict.get("first_name")):
            nom_d = sp_dict.get("nombre") or sp_dict.get("Nombre") or f"{sp_dict.get('first_name', '')} {sp_dict.get('last_name', '')}".strip()
            dpi_d = str(sp_dict.get("dpi") or sp_dict.get("DPI") or sp_dict.get("identification_number") or "").strip()
            trab_d = str(sp_dict.get("Lugar_de_Trabajo") or sp_dict.get("lugar_trabajo") or "").strip()
            _agregar_fiador_linea(nom_d, dpi=dpi_d, trabajo=trab_d, cod=str(sp_dict.get("Codigo_de_Cliente") or ""))

    for gf in garantias_fiador:
        sp = gf.get("especificaciones") if isinstance(gf.get("especificaciones"), dict) else {}
        cod = str(sp.get("Codigo_de_Cliente") or "").strip()
        nom = str(sp.get("Nombre") or sp.get("nombre") or "").strip()
        dpi_g = str(sp.get("DPI") or sp.get("dpi") or "").strip()
        trab_g = str(sp.get("Lugar_de_Trabajo") or sp.get("lugar_trabajo") or "").strip()
        if (not nom or not dpi_g) and cod:
            try:
                from apps.customers.models import Customer
                cust = Customer.objects.filter(customer_code=cod).first()
                if cust is not None:
                    nom = nom or (cust.get_full_name() if callable(getattr(cust, "get_full_name", None)) else f"{cust.first_name} {cust.last_name}")
                    dpi_g = dpi_g or str(cust.identification_number or "")
            except Exception:
                pass
        if nom:
            _agregar_fiador_linea(nom, dpi=dpi_g, trabajo=trab_g, cod=cod)

    if not hasattr(solicitud, "total_value_of_the_product_or_service") and getattr(solicitud, "id", None):
        try:
            from apps.financings.models import DetailsGuarantees
            for det in DetailsGuarantees.objects.filter(garantia_id__credit_id=solicitud, tipo_garantia="FIADOR").order_by("pk"):
                sp = det.especificaciones if isinstance(det.especificaciones, dict) else {}
                _agregar_fiador_linea(
                    str(sp.get("Nombre") or sp.get("nombre") or ""),
                    dpi=str(sp.get("DPI") or sp.get("dpi") or ""),
                    trabajo=str(sp.get("Lugar_de_Trabajo") or ""),
                    cod=str(sp.get("Codigo_de_Cliente") or ""),
                )
        except Exception:
            pass

    if not lineas:
        return "Sin garantías específicas registradas en la solicitud."

    return "\n".join(lineas)


def _construir_otras_condiciones(solicitud, destino_principal: str) -> str:
    """Recopila condiciones adicionales relevantes de la solicitud para la resolución."""
    condiciones = []

    tipo_doc = str(getattr(solicitud, "tipo_documento", "") or "").strip()
    tipo_pag = str(getattr(solicitud, "tipo_pagare", "") or "").strip()
    if tipo_doc or tipo_pag:
        partes_doc = []
        if tipo_doc:
            partes_doc.append(f"Documento legal: {tipo_doc}")
        if tipo_pag:
            partes_doc.append(f"Modalidad de pagaré: {tipo_pag}")
        condiciones.append("• " + " | ".join(partes_doc) + ".")

    gracia = int(getattr(solicitud, "plazo_gracia", 0) or 0)
    if gracia > 0:
        condiciones.append(f"• Cuenta con período de gracia de {gracia} {'mes' if gracia == 1 else 'meses'}.")

    cred_ant = getattr(solicitud, "credito_anterior_vigente", None)
    if cred_ant:
        cods = []
        if isinstance(cred_ant, (list, tuple)):
            for item in cred_ant:
                if isinstance(item, dict):
                    cods.append(str(item.get("codigo_credito") or item.get("codigo") or item.get("id") or ""))
                else:
                    cods.append(str(item))
        cods_txt = ", ".join(c for c in cods if c)
        if cods_txt:
            condiciones.append(f"• Vinculado a crédito(s) anterior(es): {cods_txt}.")

    desc_larga = str(getattr(solicitud, "investment_plan_description", "") or getattr(solicitud, "proposito", "") or "").strip()
    if desc_larga and desc_larga.lower() not in destino_principal.lower():
        condiciones.append(f"• Detalle adicional del destino: {desc_larga}")

    mitigadores = str(getattr(solicitud, "mitigadores", "") or "").strip()
    if mitigadores and mitigadores.lower() not in ("n/a", "ninguno", "---"):
        condiciones.append(f"• Mitigadores: {mitigadores}")

    return "\n".join(condiciones)


def _obtener_acta_solicitud(solicitud) -> tuple[str, object]:
    """Obtiene (numero_acta, fecha_acta) desde DetalleActa / Acta si la solicitud está vinculada a un acta."""
    sol_ref = (
        solicitud
        if hasattr(solicitud, "total_value_of_the_product_or_service")
        else getattr(solicitud, "destino_id", None)
    )
    if sol_ref is None:
        return ("", None)

    detalle = None
    det_mgr = getattr(sol_ref, "detalles_acta", None)
    if det_mgr is not None and hasattr(det_mgr, "select_related"):
        try:
            detalle = det_mgr.select_related("acta").order_by("-acta__fecha_acta", "-id").first()
        except Exception:
            try:
                detalle = det_mgr.first()
            except Exception:
                detalle = None
    elif getattr(sol_ref, "id", None):
        try:
            from apps.InvestmentPlan.models import DetalleActa
            detalle = (
                DetalleActa.objects
                .select_related("acta")
                .filter(solicitud_credito=sol_ref)
                .order_by("-acta__fecha_acta", "-id")
                .first()
            )
        except Exception:
            detalle = None

    if detalle is not None and getattr(detalle, "acta", None) is not None:
        acta_obj = detalle.acta
        num = str(getattr(acta_obj, "numero_acta", "") or "").strip()
        fec = getattr(acta_obj, "fecha_acta", None)
        return (num, fec)

    return ("", None)


def extraer_datos_resolucion_desde_solicitud(solicitud, overrides: dict | None = None) -> dict:
    """
    Extrae toda la información real desde una Solicitud (InvestmentPlan) o Crédito (Credit)
    y la asigna al esquema exacto de la Resolución del Comité Técnico de Créditos.
    """
    cliente = getattr(solicitud, "customer_id", None)

    if cliente:
        codigo_cliente = str(getattr(cliente, "customer_code", "") or "").strip()
        cliente_nombre = (
            cliente.get_full_name() if callable(getattr(cliente, "get_full_name", None))
            else f"{getattr(cliente, 'first_name', '')} {getattr(cliente, 'last_name', '')}".strip()
        ).upper()
    else:
        codigo_cliente = ""
        cliente_nombre = "------"

    codigo_solicitud = str(
        getattr(solicitud, "investment_plan_code", None)
        or getattr(solicitud, "codigo_credito", None)
        or ""
    ).strip()

    # Acta y Fecha: priorizar fecha del acta vinculada o fecha_inicio / creation_date de la solicitud
    acta_numero, acta_fecha = _obtener_acta_solicitud(solicitud)
    fecha_raw = acta_fecha or getattr(solicitud, "fecha_inicio", None) or getattr(solicitud, "creation_date", None) or date.today()
    fecha_str = _formatear_fecha_corta(fecha_raw) or _formatear_fecha_corta(date.today())

    # Estado de aprobación o estado de crédito
    if hasattr(solicitud, "estado_aprobacion"):
        estado = str(getattr(solicitud, "estado_aprobacion", None) or "PENDIENTE").strip().upper()
    elif getattr(solicitud, "is_paid_off", False):
        estado = "CANCELADO"
    else:
        estado = "APROBADO"

    calidad_cliente = _determinar_calidad_cliente(solicitud, cliente)

    # Condiciones financieras
    capital = float(
        getattr(solicitud, "total_value_of_the_product_or_service", None)
        or getattr(solicitud, "monto", 0)
        or 0
    )
    monto_str = f"Q. {capital:,.2f}"

    tipo_prod = str(getattr(solicitud, "type_of_product_or_service", None) or getattr(solicitud, "tipo_credito", None) or "").strip()
    sub_dest = str(getattr(solicitud, "sub_destino", None) or "").strip()
    desc_plan = str(getattr(solicitud, "investment_plan_description", None) or getattr(solicitud, "proposito", None) or "").strip()
    destino_esp = sub_dest or desc_plan
    if tipo_prod and destino_esp and destino_esp.lower() != tipo_prod.lower():
        destino = f"{tipo_prod} - {destino_esp}"
    else:
        destino = tipo_prod or destino_esp or "Comercio y capital de trabajo"

    plazo_int = int(getattr(solicitud, "plazo", 0) or 0)
    gracia_int = int(getattr(solicitud, "plazo_gracia", 0) or 0)
    plazo_str = f"{plazo_int} {'mes' if plazo_int == 1 else 'meses'}" if plazo_int > 0 else "N/A"
    if gracia_int > 0:
        plazo_str += f" (Gracia: {gracia_int} {'mes' if gracia_int == 1 else 'meses'})"

    forma_pago = str(getattr(solicitud, "forma_de_pago", None) or "NIVELADA").strip().upper()
    frec_pago = str(getattr(solicitud, "frecuencia_pago", None) or "").strip().upper()
    if frec_pago and frec_pago not in forma_pago:
        forma_pago_str = f"{forma_pago} ({frec_pago})"
    else:
        forma_pago_str = forma_pago

    tasa_mensual = obtener_tasa_mensual_porcentaje(solicitud)
    tasa_fmt = str(int(tasa_mensual)) if float(tasa_mensual).is_integer() else f"{tasa_mensual:g}"
    tasa_interes_str = f"{tasa_fmt}% mensual"

    desembolso_str = _obtener_resumen_desembolso(solicitud, capital)

    # Fecha de Primer Pago: primera cuota del plan o fecha_inicio + 1 mes
    fecha_primer_pago_val = None
    try:
        cuotas = generar_cuotas_para_contrato(solicitud)
        if cuotas and cuotas[0].get("fecha_final"):
            fecha_primer_pago_val = cuotas[0]["fecha_final"]
    except Exception:
        fecha_primer_pago_val = None

    if not fecha_primer_pago_val:
        f_ini_base = getattr(solicitud, "fecha_inicio", None)
        if f_ini_base:
            fecha_primer_pago_val = sumar_meses_seguro(f_ini_base, 1)

    fecha_primer_pago_str = _formatear_fecha_corta(fecha_primer_pago_val) or "Por definir"

    garantia_str = _construir_resumen_garantias_solicitud(solicitud)
    otras_condiciones_str = _construir_otras_condiciones(solicitud, destino)

    datos = {
        "empresa_nombre": "INVERSIONES INTEGRALES EL TELAR S.A.",
        "titulo_documento": "RESOLUCIÓN",
        "subtitulo_comite": "COMITÉ TÉCNICO DE CRÉDITOS",
        "codigo_cliente": codigo_cliente,
        "codigo_solicitud": codigo_solicitud,
        "fecha": fecha_str,
        "acta": acta_numero or "________________",
        "cliente_nombre": cliente_nombre,
        "calidad_cliente": calidad_cliente,
        "estado": estado,
        "monto": monto_str,
        "destino": destino,
        "plazo": plazo_str,
        "forma_pago": forma_pago_str,
        "tasa_interes": tasa_interes_str,
        "desembolso": desembolso_str,
        "fecha_primer_pago": fecha_primer_pago_str,
        "garantia": garantia_str,
        "otras_condiciones": otras_condiciones_str,
        "firma_1": "Firma",
        "firma_2": "Firma",
    }

    if overrides and isinstance(overrides, dict):
        datos.update(overrides)

    return datos


def generar_resolucion_desde_solicitud(solicitud_o_id, overrides: dict | None = None, output_target=None):
    """
    Genera la Resolución del Comité Técnico de Créditos en Word (.docx)
    extrayendo automáticamente los datos desde una Solicitud (InvestmentPlan) o Crédito (Credit).
    """
    solicitud = resolver_solicitud_o_credito(solicitud_o_id)
    datos = extraer_datos_resolucion_desde_solicitud(solicitud, overrides=overrides)
    return generar_resolucion_word(datos, output_target=output_target)


generar_resolucion_desde_credito = generar_resolucion_desde_solicitud
