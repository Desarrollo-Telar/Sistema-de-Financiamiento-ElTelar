"""
Módulo para la generación del documento PAGARÉ LIBRE DE PROTESTO en formato Word (.docx).
Diseñado para El Telar S.A., compatible tanto con llamadas directas (diccionario de datos)
como con instancias del modelo Credit de Django.
"""

import io
import os
from datetime import date, datetime
from decimal import Decimal

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

from .helpers import (
    numero_a_letras,
    formato_quetzales,
    monto_a_letras_quetzales,
    cui_dpi_a_letras,
    nit_a_letras,
    cuenta_a_letras,
    porcentaje_a_letras,
    plazo_a_letras,
    cuotas_a_letras,
    fecha_a_texto_estandar,
    fecha_a_texto_notarial,
)


def obtener_datos_ejemplo() -> dict:
    """
    Retorna un diccionario con los datos de ejemplo exactos
    proporcionados en la plantilla legal de El Telar S.A.
    """
    return {
        "acreedor_nombre_corto": "EL TELAR, S.A.",
        "acreedor_nombre_completo": "INVERSIONES INTEGRALES EL TELAR, SOCIEDAD ANONIMA",
        "capital_adeudado": 360000.00,
        "plazo_meses": 12,
        "fecha_vencimiento": "08 de noviembre 2027",
        "deudor_nombre": "Mario Antonio Chen Caal",
        "deudor_dpi": "2526 22097 1601",
        "deudor_dpi_letras": "Dos mil quinientos veintiséis, Veintidós mil noventa y siete, Mil seiscientos uno",
        "deudor_nit": "1012084K",
        "deudor_nit_letras": "uno cero uno dos cero ocho cuatro K",
        "tasa_interes": 4.5,
        "tasa_interes_letras": "CUATRO PUNTO CINCO",
        "banco_nombre": "Banco de Desarrollo Rural, Banrural",
        "cuenta_bancaria": "3696008759",
        "cuenta_bancaria_letras": "TRES SEIS NUEVE SEIS CERO CERO OCHO SIETE CINCO NUEVE",
        "numero_cuotas": 12,
        "numero_cuotas_letras": "DOCE",
        "amortizaciones_capital_texto": "una (1) amortización (es)",
        "amortizaciones_interes_cuotas": "DOCE (12) amortización(es)",
        "porcentaje_atraso": "diez por ciento (10%)",
        "direccion_notificaciones": "-----",
        "lugar_emision": "--------",
        "fecha_emision": "---- de octubre 2026",
        # Avalista
        "incluir_aval": True,
        "avalistas": [
            {
                "nombre": "Juan Pérez",
                "dpi": "2545 74211 1601",
                "domicilio": "Cobán, Alta Verapaz",
            },
            {
                "nombre": "María López",
                "dpi": "1837 11882 1601",
                "domicilio": "San Pedro Carchá, Alta Verapaz",
            },
        ],
        
        "aval_monto": 360000.00,
        "aval_monto_letras": "TRESCIENTOS SESENTA MIL",
        "aval_lugar_fecha": "________________________________________________________________",
       
        # Legalización Notarial
        "incluir_autentica": True,
        "notario_ciudad": "Cobán",
        "notario_departamento": "Alta Verapaz",
        "notario_fecha_letras": "dieciséis de octubre del año dos mil veintiséis",
        "notario_firmantes": "JOSÉ y EDGAR",
        "notario_cui_firmantes": [
            "dos mil quinientos cuarenta y cinco espacio setenta y cuatro mil doscientos once espacio un mil seiscientos uno",
            "un mil ochocientos treinta y siete espacio once mil ochocientos ochenta y dos espacio un mil seiscientos uno",
        ],
    }


def _preparar_datos(datos_entrada: dict | None) -> dict:
    """
    Normaliza y completa los datos con valores calculados automáticamente si faltan.
    """
    datos = obtener_datos_ejemplo()
    if datos_entrada:
        datos.update(datos_entrada)

    # Capital
    capital = datos.get("capital_adeudado", 360000.00)
    try:
        cap_val = float(capital)
    except (ValueError, TypeError):
        cap_val = 0.0

    if "capital_adeudado_formato" not in datos:
        datos["capital_adeudado_formato"] = formato_quetzales(cap_val)
    if "capital_adeudado_letras" not in datos or not datos["capital_adeudado_letras"]:
        datos["capital_adeudado_letras"] = monto_a_letras_quetzales(cap_val)

    # Plazo
    plazo = datos.get("plazo_meses", 12)
    try:
        plazo_int = int(plazo)
    except (ValueError, TypeError):
        plazo_int = 12
    if "plazo_letras" not in datos or not datos["plazo_letras"]:
        datos["plazo_letras"] = plazo_a_letras(plazo_int)

    # CUI/DPI Deudor
    cui_raw = datos.get("deudor_dpi", "")
    if cui_raw:
        letras_cui, form_cui = cui_dpi_a_letras(cui_raw)
        if "deudor_dpi_letras" not in datos or not datos["deudor_dpi_letras"]:
            datos["deudor_dpi_letras"] = letras_cui
        if "deudor_dpi_formateado" not in datos:
            datos["deudor_dpi_formateado"] = form_cui
    else:
        datos["deudor_dpi_formateado"] = ""

    # NIT Deudor
    nit_raw = datos.get("deudor_nit", "")
    if nit_raw and ("deudor_nit_letras" not in datos or not datos["deudor_nit_letras"]):
        datos["deudor_nit_letras"] = nit_a_letras(nit_raw)

    # Tasa
    tasa = datos.get("tasa_interes", 4.5)
    if "tasa_interes_letras" not in datos or not datos["tasa_interes_letras"]:
        datos["tasa_interes_letras"] = porcentaje_a_letras(tasa)
    try:
        tasa_f = float(tasa)
        datos["tasa_interes_formato"] = f"{tasa_f:.1f}%" if tasa_f % 1 != 0 else f"{int(tasa_f)}%"
    except Exception:
        datos["tasa_interes_formato"] = f"{tasa}%"

    # Cuenta bancaria
    cuenta = datos.get("cuenta_bancaria", "3696008759")
    if "cuenta_bancaria_letras" not in datos or not datos["cuenta_bancaria_letras"]:
        datos["cuenta_bancaria_letras"] = cuenta_a_letras(cuenta)

    # Cuotas
    cuotas = datos.get("numero_cuotas", plazo_int)
    try:
        cuotas_int = int(cuotas)
    except (ValueError, TypeError):
        cuotas_int = plazo_int
    if "numero_cuotas_letras" not in datos or not datos["numero_cuotas_letras"]:
        datos["numero_cuotas_letras"] = cuotas_a_letras(cuotas_int)

    # Fecha vencimiento
    f_venc = datos.get("fecha_vencimiento")
    if isinstance(f_venc, (date, datetime)):
        datos["fecha_vencimiento"] = fecha_a_texto_estandar(f_venc)

    # Persona avalada
    if not datos.get("aval_persona_avalada"):
        datos["aval_persona_avalada"] = datos.get("deudor_nombre", "")

    # Monto aval
    if "aval_monto" not in datos:
        datos["aval_monto"] = cap_val
    if "aval_monto_letras" not in datos or not datos["aval_monto_letras"]:
        datos["aval_monto_letras"] = monto_a_letras_quetzales(datos["aval_monto"]).replace(" QUETZALES EXACTOS", "")

    # Una lista explícita sustituye los campos históricos de avalista único.
    entrada = datos_entrada or {}
    if "avalistas" in entrada:
        avalistas = entrada["avalistas"] or []
        if not isinstance(avalistas, (list, tuple)) or any(
            not isinstance(avalista, dict) for avalista in avalistas
        ):
            raise ValueError("avalistas debe ser una lista de diccionarios")
        datos["avalistas"] = [dict(avalista) for avalista in avalistas]
        datos["incluir_aval"] = bool(avalistas) and entrada.get("incluir_aval", True)
    elif datos.get("incluir_aval") or any(
        datos.get(campo) for campo in ("avalista_nombre", "avalista_dpi", "avalista_domicilio")
    ):
        datos["avalistas"] = [{
            "nombre": datos.get("avalista_nombre", ""),
            "dpi": datos.get("avalista_dpi", ""),
            "domicilio": datos.get("avalista_domicilio", ""),
        }]
        datos["incluir_aval"] = entrada.get("incluir_aval", True)
    else:
        datos["avalistas"] = []

    if datos["incluir_aval"]:
        firmantes = [(datos.get("deudor_nombre", ""), datos.get("deudor_dpi", ""))]
        firmantes.extend((aval.get("nombre", ""), aval.get("dpi", "")) for aval in datos["avalistas"])
        if "notario_firmantes" not in entrada:
            datos["notario_firmantes"] = "; ".join(nombre or "________________" for nombre, _ in firmantes)
        if "notario_cui_firmantes" not in entrada:
            datos["notario_cui_firmantes"] = [
                cui_dpi_a_letras(dpi)[0] if dpi else "________________" for _, dpi in firmantes
            ]

    return datos


def _aplicar_estilos_base(doc: Document):
    """Configura márgenes y fuentes predeterminadas del documento."""
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.5)
        section.page_height = Inches(11.0)

    # Ajuste de estilo Normal
    style = doc.styles["Normal"]
    font = style.font
    font.name = "Calibri"
    font.size = Pt(10.5)
    font.color.rgb = RGBColor(20, 20, 20)


def _agregar_parrafo_justificado(doc: Document, texto: str = "", espacio_despues: int = 4):
    """Crea un párrafo con alineación justificada e interlineado legal."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(espacio_despues)
    if texto:
        p.add_run(texto)
    return p


def _agregar_item_lista(doc: Document, texto_run_bold: str, texto_run_normal: str):
    """Agrega un elemento con viñeta y sangría para causales y pactos."""
    p = doc.add_paragraph(style="List Bullet")
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(3)
    if texto_run_bold:
        r_bold = p.add_run(texto_run_bold)
        r_bold.bold = True
    if texto_run_normal:
        p.add_run(texto_run_normal)
    return p


def _agregar_linea_firma(table, col: int, titulo: str, nombre: str, dpi: str, extra: str = None):
    """Rellena una celda de firma en una tabla."""
    cell = table.cell(0, col)
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(2)

    r_tit = p.add_run(f"{titulo}\n")
    r_tit.bold = True

    r_line = p.add_run("Firma: ______________________________________\n")
    p.add_run(f"Nombre: {nombre or '____________________________________'}\n")
    p.add_run(f"DPI: {dpi or '_______________________________________'}\n")
    if extra:
        p.add_run(f"{extra}\n")


def generar_pagare_word(datos_entrada: dict | None = None, output_target=None):
    """
    Genera el documento Word (.docx) del PAGARÉ LIBRE DE PROTESTO.

    Parámetros:
    -----------
    datos_entrada : dict, opcional
        Diccionario con las variables del documento (deudor, montos, plazos, aval, etc.).
        avalistas: lista de diccionarios con nombre, dpi y domicilio; genera un bloque
        por persona. Una lista vacía omite el aval. incluir_aval=False lo desactiva.
        Se mantienen los campos avalista_nombre, avalista_dpi y avalista_domicilio.
        Si se omite o faltan campos, se autocompletan con datos de ejemplo estándar.
    output_target : str o archivo-like (ej. BytesIO), opcional
        Si se pasa un str (ruta), guarda el archivo en disco.
        Si se pasa un stream o None, retorna un objeto io.BytesIO() con el binario del docx.

    Retorno:
    --------
    io.BytesIO o str (la ruta de archivo si fue especificada)
    """
    datos = _preparar_datos(datos_entrada)
    doc = Document()
    _aplicar_estilos_base(doc)

    # 1. ENCABEZADO
    p_titulo = doc.add_paragraph()
    p_titulo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_titulo.paragraph_format.space_after = Pt(2)
    p_titulo.paragraph_format.space_before = Pt(0)
    run_t1 = p_titulo.add_run("PAGARÉ")
    run_t1.bold = True
    run_t1.font.size = Pt(13)

    p_subtitulo = doc.add_paragraph()
    p_subtitulo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_subtitulo.paragraph_format.space_after = Pt(8)
    run_t2 = p_subtitulo.add_run("LIBRE DE PROTESTO")
    run_t2.bold = True
    run_t2.font.size = Pt(11)

    # Beneficiario / Orden
    p_orden = doc.add_paragraph()
    p_orden.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_orden.paragraph_format.space_after = Pt(4)
    run_ord_label = p_orden.add_run("A la orden o endoso de: ")
    
    empresa = p_orden.add_run(datos.get("acreedor_nombre_corto", "EL TELAR, S.A."))
    empresa.bold = True

    # Caja / Fila de Resumen: Capital, Plazo, Vencimiento
    tabla_resumen = doc.add_table(rows=2, cols=2)
    tabla_resumen.alignment = WD_TABLE_ALIGNMENT.CENTER
    tabla_resumen.autofit = False

    # Configuración de ancho de columnas
    tabla_resumen.columns[0].width = Inches(3.5)
    tabla_resumen.columns[1].width = Inches(3.0)

    # Fila 0: Capital y Plazo
    c00 = tabla_resumen.cell(0, 0).paragraphs[0]
    c00.paragraph_format.space_after = Pt(2)
    r_cap_lbl = c00.add_run("Capital Adeudado: ")
    r_cap_lbl.bold = True
    c00.add_run(datos["capital_adeudado_formato"])

    c01 = tabla_resumen.cell(0, 1).paragraphs[0]
    c01.paragraph_format.space_after = Pt(2)
    r_plz_lbl = c01.add_run("Plazo: ")
    r_plz_lbl.bold = True
    c01.add_run(f"{datos['plazo_meses']} meses")

    # Fila 1: Fecha de vencimiento
    c10 = tabla_resumen.cell(1, 0).paragraphs[0]
    c10.paragraph_format.space_after = Pt(6)
    r_fvc_lbl = c10.add_run("Fecha de vencimiento: ")
    r_fvc_lbl.bold = True
    c10.add_run(str(datos.get("fecha_vencimiento", "")))

    # Separación
    p_sep = doc.add_paragraph()
    p_sep.paragraph_format.space_before = Pt(4)
    p_sep.paragraph_format.space_after = Pt(4)

    # 2. IDENTIFICACIÓN DE LA PARTE DEUDORA
    p_deudor = _agregar_parrafo_justificado(doc, espacio_despues=6)
    p_deudor.add_run("Yo, ")
    r_deudor_nom = p_deudor.add_run(f"{datos.get('deudor_nombre', '')} ")
    r_deudor_nom.bold = False
    p_deudor.add_run(
        "me identifico con el Documento Personal de Identificación con Código Único de Identificación "
        f"{datos.get('deudor_dpi_letras', '')} ({datos.get('deudor_dpi_formateado') or datos.get('deudor_dpi', '')}) "
        "extendido por el Registro Nacional de las Personas (RENAP); así mismo con el número de "
        f"Identificación Tributaria {datos.get('deudor_nit_letras', '')} ({datos.get('deudor_nit', '')}) "
        "en adelante referido también simple e indistintamente como "
    )

    r_deudor = p_deudor.add_run('"LA PARTE DEUDORA". ')
    r_deudor.bold = True

    # 3. PROMESA INCONDICIONAL DE PAGO
    p_promesa = _agregar_parrafo_justificado(doc, espacio_despues=8)
    p_promesa.add_run("Por el presente acto, ")
    r_prometo = p_promesa.add_run("PROMETO INCONDICIONALMENTE PAGAR ")
    r_prometo.bold = True
    p_promesa.add_run(
        "a la orden o endoso de "   
    )

    r_promesa_empresa = p_promesa.add_run(f"{datos.get('acreedor_nombre_completo', 'INVERSIONES INTEGRALES EL TELAR, SOCIEDAD ANONIMA')}, ")
    r_promesa_empresa.bold = True

    p_promesa.add_run(
        "en adelante referido simple e indistintamente como el "
    )

    r_p_promesa_acreedor = p_promesa.add_run("ACREEDOR, ")
    r_p_promesa_acreedor.bold = True

    p_promesa.add_run(
        "la cantidad indicada como "
    )

    r_p_promesa_capital = p_promesa.add_run("Capital Adeudado ")
    r_p_promesa_capital.bold = True

    p_promesa.add_run(
        "y cualquier otro interés, costo y/o gasto que resulte aplicable (en adelante conjuntamente “Suma Adeudada”)."
    )

    # 4. TÉRMINOS Y CONDICIONES DEL PAGARÉ
    p_tc_tit = doc.add_paragraph()
    p_tc_tit.paragraph_format.space_before = Pt(4)
    p_tc_tit.paragraph_format.space_after = Pt(4)
    r_tc = p_tc_tit.add_run("TÉRMINOS Y CONDICIONES DEL PAGARÉ:")
    r_tc.bold = True

    # Cláusula PLAZO
    p_plazo = _agregar_parrafo_justificado(doc)
    p_plazo.add_run("A. PLAZO: ").bold = True
    p_plazo.add_run(
        f"El plazo del presente pagaré será de "
        
    )

    p_plazo.add_run(f"{datos.get('plazo_letras', '')}, ").bold = True
    p_plazo.add_run("contados a partir de la fecha de "
                    "aceptación y firma de este documento. El ACREEDOR podrá, en cualquier momento después del vencimiento inicial "
                            "del pagaré, exigir el pago del capital, intereses, cargos por atrasos, comisiones y cargos que correspondan "
                            "a LA PARTE DEUDORA, sin perjuicio de cualquier plazo de gracia otorgado.")

    # Cláusula INTERESES ORDINARIOS
    p_intereses = _agregar_parrafo_justificado(doc)
    p_intereses.add_run("B. INTERESES ORDINARIOS: ").bold = True
    p_intereses.add_run(
        "LA PARTE DEUDORA reconoce y se obliga a pagar el capital, cargos y los intereses aplicables. Sobre el capital adeudado, se generará un interés total del ")
    p_intereses.add_run(
        f"{datos.get('tasa_interes_letras', '')} ").bold = True
    p_intereses.add_run("por ciento "
        f"({datos.get('tasa_interes_formato', '')}) sobre el capital adeudado. El capital adeudado más intereses "
        "será acreditado a LA PARTE DEUDORA, mediante transferencia bancaria o mediante deposito a la cuenta monetaria "
        f"número {datos.get('cuenta_bancaria_letras', '')} ({datos.get('cuenta_bancaria', '')}) del {datos.get('banco_nombre', 'Banco de Desarrollo Rural, Banrural')}."
    )

    # Cláusula AMORTIZACIONES
    p_amort = _agregar_parrafo_justificado(doc)
    p_amort.add_run("C. AMORTIZACIONES: ").bold = True
    p_amort.add_run(
        f"LA PARTE DEUDORA deberá pagar el capital, cargos, los intereses y cualquier impuesto aplicable en ")
    p_amort.add_run( f"{datos.get('numero_cuotas_letras', '')} ").bold = True

    p_amort.add_run(
        "cuota(s). La(s) cuota(s) incluye(n) el cálculo de los intereses "
        "aplicables sobre el total del capital adeudado y el impuesto al Valor Agregado (IVA). En ese sentido, la "
        f"PARTE DEUDORA deberá pagar la cantidad de {datos.get('capital_adeudado_letras', '')} ({datos['capital_adeudado_formato']}) "
        "en concepto de capital; más intereses y recargos por mora. Para el cálculo y pago de cada cuota, el ACREEDOR "
        "podrá redondear los decimales al número entero más cercano."
    )

    # Cláusula CALENDARIO DE PAGOS
    p_cal = _agregar_parrafo_justificado(doc)
    p_cal.add_run("D. CALENDARIO DE PAGOS: ").bold = True
    p_cal.add_run("La(s) cuota(s) se deberá(n) pagar en la(s) fechas pactadas según la tabla de amortización adjunta.")

    # Cláusula FORMA Y LUGAR DE PAGO
    p_forma = _agregar_parrafo_justificado(doc)
    p_forma.add_run("E. FORMA Y LUGAR DE PAGO: ").bold = True
    p_forma.add_run(
        f"El pago del capital se hará mediante {datos.get('amortizaciones_capital_texto', 'una (1) amortización (es)')}, "
        f"más los intereses, cargos y los impuestos aplicables en ")
    p_forma.add_run(   
        f"{datos.get('amortizaciones_interes_cuotas', 'DOCE (12) amortización(es)')}. ").bold = True
    
    p_forma.add_run(
        "Todos los pagos que, por cualquier naturaleza, procedan conforme a este pagaré deben hacerse mediante depósito "
        "o transferencias bancaria a la cuenta que indique el ACREEDOR. La Suma Adeudada deberá pagarse al ACREEDOR en la fecha "
        "de vencimiento, sin necesidad de protesto, aviso de falta de pago, requerimiento de pago y actos similares "
        "exigidos para la vigencia y ejecutabilidad de los derechos y acciones aquí contenidos.\n"
        "El ACREEDOR podrá aceptar pagos parciales en los casos que considere apropiado, sin que esto limite o implique "
        "una renuncia a su derecho a exigir el pago completo o cobrar judicialmente el pagaré. Adicionalmente, la aceptación "
        "de cualquier pago parcial no representará una renuncia al cobro de cualquier interés, cargo por atraso, impuesto, "
        "cargo o gasto que resulte aplicable."
    )

    # Cláusula CARGO POR ATRASO
    p_atraso = _agregar_parrafo_justificado(doc)
    p_atraso.add_run("F. CARGO POR ATRASO: ").bold = True
    p_atraso.add_run(
        "En caso de incumplimiento, que se producirá por la falta de pago de cualquiera de las cantidades pactadas "
        "en las fechas establecidas en la cláusula “E” de este documento, y sin que por ello se considere prorrogado el Plazo, "
        "sin necesidad de requerimiento alguno, LA PARTE DEUDORA deberá pagar los intereses vencidos, más, el equivalente "
        f"al {datos.get('porcentaje_atraso', 'diez por ciento (10%)')} del interés vencido y acumulado en concepto de cargo por atraso, "
        "a partir del día siguiente a la fecha de vencimiento. Estos montos ya incluyen el Impuesto al Valor Agregado (IVA)."
    )

    # Cláusula ORDEN DE PAGOS
    p_orden_p = _agregar_parrafo_justificado(doc)
    p_orden_p.add_run("G. ORDEN DE PAGOS: ").bold = True
    p_orden_p.add_run(
        "Todo pago que realice LA PARTE DEUDORA se aplicará, en primer lugar, a los cargos por atraso que se hayan generado "
        "y, al liquidar el monto correspondiente, en segundo lugar se aplicará a los intereses vencidos, en tercer lugar "
        "se aplicara a los intereses ordinarios, y, por último, al capital adeudado. En ningún momento se podrá solicitar el "
        "pago al capital adeudado, sin estar solvente en el pago de los otros conceptos."
    )

    # Cláusula REFINANCIAMIENTO
    p_ref = _agregar_parrafo_justificado(doc)
    p_ref.add_run("H. REFINANCIAMIENTO: ").bold = True
    p_ref.add_run(
        "Sin perjuicio de los derechos que incorpora el presente pagaré y la exigencia de estos, El ACREEDOR podrá recibir "
        "solicitudes para el refinanciamiento de la Suma Adeudada. El ACREEDOR podrá analizar las solicitudes de refinanciamiento "
        "y, a su sola discreción, autorizar o no la solicitud."
    )

    # Cláusula CAMBIO DE CONDICIONES
    p_cambio = _agregar_parrafo_justificado(doc)
    p_cambio.add_run("I. CAMBIO DE CONDICIONES: ").bold = True
    p_cambio.add_run(
        "En caso que algún ente regulador o alguna entidad debidamente autorizada para el efecto estableciera tasas de "
        "interés máximas para operaciones aquí previstas, se aplicarán las siguientes reglas: (i) los intereses que devengará "
        "este contrato serán los intereses máximos que fije la entidad autorizada para estas operaciones, a menos que El "
        "ACREEDOR decida cobrar una tasa menor; (ii) la tasa variará automáticamente a partir de la fecha en que adquiera vigencia "
        "cualquier variación de la tasa máxima activa acordada por la entidad autorizada para el efecto o cuando, dentro de los "
        "límites legales, la parte acreedora así lo disponga; (iii.) se entiende que lo estipulado en este inciso se aplicará "
        "únicamente en el caso de que existan límites a la tasa de interés que la parte acreedora pueda cobrar en sus operaciones; "
        "(iv) en caso deje de aplicar lo antes mencionado, se volverá a lo dispuesto en los términos y condiciones aplicables del presente contrato."
    )

    # Cláusula CEDIBILIDAD
    p_ced = _agregar_parrafo_justificado(doc)
    p_ced.add_run("J. CEDIBILIDAD: ").bold = True
    p_ced.add_run(
        "El ACREEDOR podrá transferir y negociar en cualquier forma sus derechos provenientes del presente pagaré a cualquier "
        "título sin necesidad de previa autorización, debiendo únicamente notificar de la cesión a LA PARTE DEUDORA. "
        "LA PARTE DEUDORA no podrá ceder o transferir en forma o título alguno de sus derechos u obligaciones derivados "
        "del presente pagaré sin contar con la autorización previa, expresa y por escrito del ACREEDOR."
    )

    # Cláusula VENCIMIENTO ANTICIPADO
    p_va = _agregar_parrafo_justificado(doc)
    p_va.add_run("K. VENCIMIENTO ANTICIPADO: ").bold = True
    p_va.add_run("EL ACREEDOR podrá dar por vencido el plazo del presente pagaré y exigir el pago de la totalidad de la suma adeudada en los casos siguientes:")

    _agregar_item_lista(doc, "", "Si los bienes de LA PARTE DEUDORA fueren objeto de embargo o en caso de insolvencia o quiebra.")
    _agregar_item_lista(doc, "", "Si LA PARTE DEUDORA tiene un cambio desfavorable con respecto a sus condiciones financieras que resulten, en opinión razonable del ACREEDOR, en una falta de capacidad en el pago de la deuda derivada del presente pagaré.")
    _agregar_item_lista(doc, "", "Por incumplimiento en el pago de otros créditos ante el ACREEDOR.")

    p_va_cierre = _agregar_parrafo_justificado(doc)
    p_va_cierre.add_run(
        "La circunstancia de que LA PARTE DEUDORA incurra en cualquiera de las causales anteriores concede al ACREEDOR el derecho "
        "automático para dar por vencido el plazo del presente título de crédito y reclamar el pago del capital pendiente de pago y "
        "para cobrar ejecutivamente dicho capital, intereses vencidos, intereses ordinarios, cargos administrativos, cargos por atrasos, "
        "costas judiciales, recargos, comisiones y demás gastos de cobranza y otras sumas que le corresponden pagar a LA PARTE DEUDORA "
        "de acuerdo a este pagaré."
    )

    # Cláusula COSTAS Y GASTOS
    p_costas = _agregar_parrafo_justificado(doc)
    p_costas.add_run("L. COSTAS Y GASTOS: ").bold = True
    p_costas.add_run(
        "Las costas judiciales, honorarios y cualquier otro gasto que se genere directa o indirectamente en virtud de la ejecución "
        "del presente pagaré, serán todos por cuenta única y exclusiva de LA PARTE DEUDORA, y devengará cargos por atraso en la misma "
        "forma que las demás obligaciones derivadas de este documento."
    )

    # Cláusula PACTOS PROCESALES
    p_pactos = _agregar_parrafo_justificado(doc)
    p_pactos.add_run("M. PACTOS PROCESALES: ").bold = True
    p_pactos.add_run("Para el efectivo cumplimiento de sus obligaciones, LA PARTE DEUDORA expresamente:")

    _agregar_item_lista(doc, "", "Renuncia a cualquier cobro o requerimiento alguno, necesidad de protesto del presente pagaré (por lo que el presente pagaré se emite \"libre de protesto\"), aviso de falta de pago, requerimiento de pago y/o actos similares exigidos para la vigencia y ejecutabilidad de los derechos y acciones aquí contenidos.")
    _agregar_item_lista(doc, "", "Renuncia al fuero de su domicilio y se somete expresamente a los tribunales que elija el ACREEDOR.")
    _agregar_item_lista(doc, "", f"Señala como dirección para recibir notificaciones, emplazamientos, citaciones, comunicaciones, avisos y/o diligencias la: {datos.get('direccion_notificaciones', '-----')}")
    _agregar_item_lista(doc, "", "Acepta como buenas, válidas y bien hechas las notificaciones, comunicaciones y/o citaciones que se le hicieran en la dirección antes señalada, mientras no hubiere comunicado por escrito al ACREEDOR con por lo menos diez (10) días hábiles de anticipación al cambio, una nueva dirección para recibirlas o medio electrónico de comunicación, son penas de tenerse por no modificada la dirección aquí señalada, de manera que las notificaciones, emplazamientos, citaciones, comunicaciones, avisos y/o diligencias que ahí se practiquen se tendrán por válidas y bien hechas.")
    _agregar_item_lista(doc, "", "Acepta desde ya como buenas y exactas las cuentas que sobre la presente obligación se le formule y como líquido exigible y de plazo vencido el saldo que se le reclame.")

    # Cierre de aceptación y fecha
    p_cierre = _agregar_parrafo_justificado(doc, espacio_despues=12)
    p_cierre.add_run(
        f"En virtud de lo anterior acepto el presente pagaré en {datos.get('lugar_emision', '--------')}, "
        f"el {datos.get('fecha_emision', '---- de octubre 2026')}."
    )

    # 5. FIRMA DEL SUSCRIPTOR O DEUDOR
    p_firma_tit = doc.add_paragraph()
    p_firma_tit.paragraph_format.space_before = Pt(8)
    p_firma_tit.paragraph_format.space_after = Pt(4)
    p_firma_tit.add_run("FIRMA DEL SUSCRIPTOR O DEUDOR:").bold = True

    p_firma_bloque = doc.add_paragraph()
    p_firma_bloque.paragraph_format.line_spacing = 1.2
    p_firma_bloque.paragraph_format.space_after = Pt(12)
    p_firma_bloque.add_run("Firma: ______________________________________\n")
    p_firma_bloque.add_run(f"Nombre: {datos.get('deudor_nombre', '____________________________________')}\n")
    p_firma_bloque.add_run(f"DPI: {datos.get('deudor_dpi_formateado') or datos.get('deudor_dpi', '_______________________________________')}\n")

    # 6. AVAL (OPCIONAL O INCLUIDO)
    for indice, avalista in enumerate(datos["avalistas"] if datos["incluir_aval"] else [], start=1):
        p_aval_tit = doc.add_paragraph()
        p_aval_tit.paragraph_format.space_before = Pt(10)
        p_aval_tit.paragraph_format.space_after = Pt(4)
        p_aval_tit.add_run(f"AVAL {indice}:" if len(datos["avalistas"]) > 1 else "AVAL:").bold = True

        p_aval_cuerpo = _agregar_parrafo_justificado(doc, espacio_despues=6)
        p_aval_cuerpo.add_run(
            "POR AVAL, garantizo el pago total del presente pagaré a favor de EL ACREEDOR y por cuenta de "
            f"{datos.get('aval_persona_avalada', '___________________________________________')}, "
            "quien es la persona avalada.\n"
            f"El presente aval garantiza la cantidad de Q__________ ({datos.get('aval_monto_letras', '________________________________________')} quetzales exactos), "
            "más los intereses, recargos por atraso y demás cantidades legalmente procedentes conforme al pagaré.\n"
            "El avalista manifiesta que conoce y acepta el contenido del pagaré y que su obligación se mantendrá vigente "
            "hasta el pago total de la cantidad avalada.\n"
            f"Lugar y fecha: {datos.get('aval_lugar_fecha', '________________________________________________________________')}."
        )

        p_aval_firma_tit = doc.add_paragraph()
        p_aval_firma_tit.paragraph_format.space_before = Pt(4)
        p_aval_firma_tit.paragraph_format.space_after = Pt(4)
        p_aval_firma_tit.add_run("FIRMA DEL AVALISTA:").bold = True

        p_aval_firma_bloque = doc.add_paragraph()
        p_aval_firma_bloque.paragraph_format.line_spacing = 1.2
        p_aval_firma_bloque.paragraph_format.space_after = Pt(12)
        p_aval_firma_bloque.add_run("Firma: ______________________________________\n")
        p_aval_firma_bloque.add_run(f"Nombre: {avalista.get('nombre') or '____________________________________'}\n")
        p_aval_firma_bloque.add_run(f"DPI: {avalista.get('dpi') or '_______________________________________'}\n")
        p_aval_firma_bloque.add_run(f"Domicilio: {avalista.get('domicilio') or '_______________________________________'}\n")

    # 7. ACTA NOTARIAL DE LEGALIZACIÓN DE FIRMAS (AUTÉNTICA)
    if datos.get("incluir_autentica", True):
        firmantes_cui = datos.get("notario_cui_firmantes", [])
        if len(firmantes_cui) > 1:
            cui_texto = "; ".join(f"firmante {i}: {cui}" for i, cui in enumerate(firmantes_cui, 1))
        elif firmantes_cui:
            cui_texto = firmantes_cui[0]
        else:
            cui_texto = "________________"

        p_autentica = _agregar_parrafo_justificado(doc, espacio_despues=8)
        p_autentica.paragraph_format.space_before = Pt(8)
        p_autentica.add_run(
            f"En la ciudad de {datos.get('notario_ciudad', 'Cobán')} del departamento de {datos.get('notario_departamento', 'Alta Verapaz')}, "
            f"a {datos.get('notario_fecha_letras', 'dieciséis de octubre del año dos mil veintiséis')}, como Notaria en ejercicio. "
        )
        r_doy_fe = p_autentica.add_run("DOY FE: ")
        r_doy_fe.bold = True
        p_autentica.add_run(
            "que las firmas que anteceden "
        )
        p_autentica.add_run("SON AUTENTICAS").bold = True
        p_autentica.add_run(
            f", por haber sido puestas en el PAGARÉ, el día de hoy en mi presencia por: {datos.get('notario_firmantes', 'JOSÉ y EDGAR')}, "
            f"quienes se identifican con los documentos personales de identificación -DPI- Código Único de Identificación -CUI- números: "
            f"{cui_texto}; extendidos por el Registro Nacional de las Personas -RENAP- de la República de Guatemala; "
            "y, quienes vuelven a firmar junto conmigo en la presente acta de legalización de firmas."
        )

        p_notario_cierre = doc.add_paragraph()
        p_notario_cierre.paragraph_format.space_before = Pt(14)
        p_notario_cierre.paragraph_format.space_after = Pt(4)
        p_notario_cierre.add_run("ANTE MÍ:").bold = True

    # GUARDAR O RETORNAR STREAM
    if isinstance(output_target, str):
        doc.save(output_target)
        return output_target
    elif output_target is not None and hasattr(output_target, "write"):
        doc.save(output_target)
        return output_target
    else:
        buffer = io.BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        return buffer


def sumar_meses(fecha_base: date, meses: int) -> date:
    """Suma un número determinado de meses a una fecha."""
    try:
        from dateutil.relativedelta import relativedelta
        return fecha_base + relativedelta(months=meses)
    except ImportError:
        nuevo_anio = fecha_base.year + (fecha_base.month + meses - 1) // 12
        nuevo_mes = (fecha_base.month + meses - 1) % 12 + 1
        nuevo_dia = min(fecha_base.day, 28)
        return date(nuevo_anio, nuevo_mes, nuevo_dia)


def extraer_datos_pagare_desde_solicitud(solicitud, aval_info: dict | None = None, notario_info: dict | None = None) -> dict:
    """
    Extrae la información de la Solicitud (InvestmentPlan) y construye
    la estructura exacta de datos para la generación del Pagaré Word.
    """
    capital = float(getattr(solicitud, 'total_value_of_the_product_or_service', None) or getattr(solicitud, 'monto', 0) or 0)
    plazo_int = int(getattr(solicitud, 'plazo', 12) or 12)

    # Fechas
    f_venc = getattr(solicitud, 'fecha_vencimiento', None)
    if isinstance(f_venc, (date, datetime)):
        fecha_vencimiento_str = fecha_a_texto_estandar(f_venc)
    elif getattr(solicitud, 'fecha_inicio', None):
        fecha_vencimiento_str = fecha_a_texto_estandar(sumar_meses(solicitud.fecha_inicio, plazo_int))
    else:
        fecha_vencimiento_str = "---- de -------- 2027"

    f_ini = getattr(solicitud, 'fecha_inicio', None) or date.today()
    if isinstance(f_ini, (date, datetime)):
        fecha_emision_str = fecha_a_texto_estandar(f_ini)
    else:
        fecha_emision_str = str(f_ini)

    # Cliente / Deudor
    cliente = getattr(solicitud, 'customer_id', None)
    if cliente:
        deudor_nombre = cliente.get_full_name() if hasattr(cliente, 'get_full_name') else f"{getattr(cliente, 'first_name', '')} {getattr(cliente, 'last_name', '')}".strip()
        deudor_dpi_raw = getattr(cliente, 'identification_number', '') or ""
        deudor_nit = getattr(cliente, 'number_nit', '') or ""
    else:
        deudor_nombre = "------"
        deudor_dpi_raw = ""
        deudor_nit = ""

    deudor_dpi_letras, deudor_dpi_formateado = cui_dpi_a_letras(deudor_dpi_raw) if deudor_dpi_raw else ("", "")
    deudor_dpi = deudor_dpi_formateado or deudor_dpi_raw
    deudor_nit_letras = nit_a_letras(deudor_nit) if deudor_nit else ""

    # Tasa de Interés
    tasa_raw = float(getattr(solicitud, 'tasa_interes', 0) or 0)
    if 0 < tasa_raw < 1:
        tasa_interes = round(tasa_raw * 100, 2)
    else:
        tasa_interes = tasa_raw if tasa_raw > 0 else 4.5
    tasa_interes_letras = porcentaje_a_letras(tasa_interes)

    # Cuotas y amortizaciones
    numero_cuotas = plazo_int
    numero_cuotas_letras = numero_a_letras(plazo_int).upper()
    cuotas_fmt = cuotas_a_letras(plazo_int)

    amortizaciones_capital_texto = "una (1) amortización (es)"
    amortizaciones_interes_cuotas = f"{cuotas_fmt} amortización(es)"

    # Dirección para notificaciones
    direccion_notificaciones = "-----"
    if cliente:
        try:
            from apps.addresses.models import Address
            dir_obj = Address.objects.filter(customer_id=cliente).first()
            if dir_obj:
                direccion_notificaciones = dir_obj.direccion() if hasattr(dir_obj, 'direccion') else str(dir_obj)
        except Exception:
            pass

    # Lugar de emisión
    sucursal = getattr(solicitud, 'sucursal', None)
    if sucursal and hasattr(sucursal, 'city') and sucursal.city:
        lugar_emision = f"{sucursal.city}, {getattr(sucursal, 'state', 'Alta Verapaz') or 'Alta Verapaz'}"
    else:
        lugar_emision = "Cobán, Alta Verapaz"

    # Avalistas
    avalistas = []

    # 1. De solicitud.fiador
    fiadores_campo = getattr(solicitud, 'fiador', None) or []
    if isinstance(fiadores_campo, dict):
        fiadores_campo = [fiadores_campo]
    ids_fiadores = []
    if isinstance(fiadores_campo, (list, tuple)):
        for f in fiadores_campo:
            if isinstance(f, dict) and f.get('id'):
                ids_fiadores.append(f['id'])
            elif isinstance(f, int):
                ids_fiadores.append(f)

    if ids_fiadores:
        try:
            from apps.customers.models import Customer
            from apps.addresses.models import Address
            clientes_fiadores = Customer.objects.filter(id__in=ids_fiadores)
            for cf in clientes_fiadores:
                addr = Address.objects.filter(customer_id=cf).first()
                dom = (addr.direccion() if hasattr(addr, 'direccion') else str(addr)) if addr else f"{cf.place_birth or 'Cobán, Alta Verapaz'}"
                nom = cf.get_full_name() if hasattr(cf, 'get_full_name') else f"{cf.first_name} {cf.last_name}".strip()
                dpi_fmt = cf.identification_number or ""
                if dpi_fmt:
                    _, dpi_fmt = cui_dpi_a_letras(dpi_fmt)
                avalistas.append({
                    "nombre": nom,
                    "dpi": dpi_fmt or cf.identification_number or "",
                    "domicilio": dom or "Cobán, Alta Verapaz",
                })
        except Exception:
            pass

    # 2. De solicitud.garantias (tipo FIADOR)
    garantias_campo = getattr(solicitud, 'garantias', None) or []
    if isinstance(garantias_campo, list):
        for g in garantias_campo:
            if isinstance(g, dict) and (g.get('tipo') == 'FIADOR' or g.get('tipo_garantia') == 'FIADOR'):
                specs = g.get('especificaciones') or {}
                if isinstance(specs, dict):
                    nom = specs.get('Nombre') or specs.get('nombre') or ""
                    dpi_val = specs.get('DPI') or specs.get('dpi') or ""
                    dom_val = specs.get('Domicilio') or specs.get('domicilio') or specs.get('Lugar_de_Trabajo') or ""
                    cod = specs.get('Codigo_de_Cliente')
                    if (not dpi_val or not dom_val) and cod:
                        try:
                            from apps.customers.models import Customer
                            from apps.addresses.models import Address
                            cust = Customer.objects.filter(customer_code=cod).first()
                            if cust:
                                if not nom:
                                    nom = cust.get_full_name() if hasattr(cust, 'get_full_name') else f"{cust.first_name} {cust.last_name}".strip()
                                if not dpi_val:
                                    dpi_val = cust.identification_number
                                if not dom_val:
                                    addr = Address.objects.filter(customer_id=cust).first()
                                    dom_val = (addr.direccion() if hasattr(addr, 'direccion') else str(addr)) if addr else f"{cust.place_birth or 'Cobán, Alta Verapaz'}"
                        except Exception:
                            pass
                    if dpi_val:
                        _, dpi_fmt = cui_dpi_a_letras(dpi_val)
                        if dpi_fmt:
                            dpi_val = dpi_fmt
                    if nom and not any(a['nombre'].strip().lower() == nom.strip().lower() for a in avalistas):
                        avalistas.append({
                            "nombre": nom,
                            "dpi": dpi_val or "",
                            "domicilio": dom_val or "Cobán, Alta Verapaz",
                        })

    incluir_aval = bool(avalistas)
    aval_monto = capital
    aval_monto_letras = monto_a_letras_quetzales(aval_monto).replace(" QUETZALES EXACTOS", "")

    # Notario y Legalización
    notario_ciudad = sucursal.city if sucursal and hasattr(sucursal, 'city') and sucursal.city else "Cobán"
    notario_departamento = sucursal.state if sucursal and hasattr(sucursal, 'state') and sucursal.state else "Alta Verapaz"
    notario_fecha_letras = fecha_a_texto_notarial(f_ini)

    firmantes = [deudor_nombre] + [a["nombre"] for a in avalistas if a.get("nombre")]
    if len(firmantes) == 1:
        notario_firmantes = firmantes[0]
    elif len(firmantes) == 2:
        notario_firmantes = f"{firmantes[0]} y {firmantes[1]}"
    else:
        notario_firmantes = f"{', '.join(firmantes[:-1])} y {firmantes[-1]}"

    dpis = [deudor_dpi] + [a["dpi"] for a in avalistas if a.get("dpi")]
    notario_cui_firmantes = [cui_dpi_a_letras(d)[0] if d else "________________" for d in dpis]

    datos = {
        "acreedor_nombre_corto": "EL TELAR, S.A.",
        "acreedor_nombre_completo": "INVERSIONES INTEGRALES EL TELAR, SOCIEDAD ANONIMA",
        "capital_adeudado": capital,
        "plazo_meses": plazo_int,
        "fecha_vencimiento": fecha_vencimiento_str,
        "deudor_nombre": deudor_nombre,
        "deudor_dpi": deudor_dpi,
        "deudor_dpi_letras": deudor_dpi_letras,
        "deudor_nit": deudor_nit,
        "deudor_nit_letras": deudor_nit_letras,
        "tasa_interes": tasa_interes,
        "tasa_interes_letras": tasa_interes_letras,
        "banco_nombre": "Banco de Desarrollo Rural, Banrural",
        "cuenta_bancaria": "3696008759",
        "cuenta_bancaria_letras": cuenta_a_letras("3696008759"),
        "numero_cuotas": numero_cuotas,
        "numero_cuotas_letras": numero_cuotas_letras,
        "amortizaciones_capital_texto": amortizaciones_capital_texto,
        "amortizaciones_interes_cuotas": amortizaciones_interes_cuotas,
        "porcentaje_atraso": "diez por ciento (10%)",
        "direccion_notificaciones": direccion_notificaciones,
        "lugar_emision": lugar_emision,
        "fecha_emision": fecha_emision_str,
        # Avalista
        "incluir_aval": incluir_aval,
        "avalistas": avalistas,
        "aval_monto": aval_monto,
        "aval_monto_letras": aval_monto_letras,
        "aval_lugar_fecha": "________________________________________________________________",
        # Legalización Notarial
        "incluir_autentica": True,
        "notario_ciudad": notario_ciudad,
        "notario_departamento": notario_departamento,
        "notario_fecha_letras": notario_fecha_letras,
        "notario_firmantes": notario_firmantes,
        "notario_cui_firmantes": notario_cui_firmantes,
    }

    if aval_info and isinstance(aval_info, dict):
        datos.update(aval_info)
    if notario_info and isinstance(notario_info, dict):
        datos.update(notario_info)

    return datos


def generar_pagare_desde_credito(credito_o_id, aval_info: dict | None = None, notario_info: dict | None = None, output_target=None):
    """
    Construye un pagaré Word extrayendo la información desde la base de datos de Django
    a partir de una Solicitud (InvestmentPlan) o de un Crédito (Credit).
    """
    solicitud = None
    if isinstance(credito_o_id, (int, str)):
        try:
            from apps.InvestmentPlan.models import InvestmentPlan
            solicitud = InvestmentPlan.objects.select_related("customer_id", "sucursal").filter(id=credito_o_id).first()
        except Exception:
            solicitud = None

        if not solicitud:
            try:
                from apps.financings.models import Credit
                credito = Credit.objects.select_related("customer_id", "destino_id").get(id=credito_o_id)
            except Exception:
                raise RuntimeError(f"No se encontró Solicitud o Crédito con ID: {credito_o_id}")
        else:
            credito = solicitud
    else:
        credito = credito_o_id

    # Si es instancia de InvestmentPlan (o tiene los campos del plan de inversión)
    if hasattr(credito, "total_value_of_the_product_or_service") or hasattr(credito, "investment_plan_code"):
        datos = extraer_datos_pagare_desde_solicitud(credito, aval_info=aval_info, notario_info=notario_info)
    else:
        # Es una instancia del modelo Credit
        try:
            from apps.financings.models import DetailsGuarantees
            from apps.addresses.models import Address
        except ImportError:
            raise RuntimeError("No se pudieron importar los modelos de Django.")

        cliente = credito.customer_id
        direccion_obj = Address.objects.filter(customer_id=cliente).first()
        direccion_str = str(direccion_obj) if direccion_obj else "-----"

        detalles_fiadores = DetailsGuarantees.objects.filter(
            garantia_id__credit_id=credito,
            tipo_garantia__in=["FIADOR", "CHEQUE / PAGARE"],
        ).order_by("pk")
        avalistas = []
        for detalle in detalles_fiadores:
            especificaciones = detalle.especificaciones
            if not isinstance(especificaciones, dict):
                continue
            nombre = especificaciones.get("Nombre", "")
            if detalle.tipo_garantia == "CHEQUE / PAGARE" and not nombre:
                continue
            dpi_f = especificaciones.get("DPI") or especificaciones.get("dpi", "")
            if dpi_f:
                _, dpi_fmt = cui_dpi_a_letras(dpi_f)
                if dpi_fmt:
                    dpi_f = dpi_fmt
            avalistas.append({
                "nombre": nombre,
                "dpi": dpi_f,
                "domicilio": especificaciones.get("Domicilio") or especificaciones.get("domicilio", ""),
            })

        tasa = float(credito.tasa_interes) * 100 if float(credito.tasa_interes) < 1 else float(credito.tasa_interes)
        deudor_nombre = cliente.get_full_name() if hasattr(cliente, "get_full_name") else f"{cliente.first_name} {cliente.last_name}".strip()
        deudor_dpi = cliente.identification_number or ""
        if deudor_dpi:
            _, dpi_fmt = cui_dpi_a_letras(deudor_dpi)
            deudor_dpi = dpi_fmt or deudor_dpi

        deudor_nit = cliente.number_nit or ""

        firmantes = [deudor_nombre] + [a["nombre"] for a in avalistas if a.get("nombre")]
        if len(firmantes) == 1:
            notario_firmantes = firmantes[0]
        elif len(firmantes) == 2:
            notario_firmantes = f"{firmantes[0]} y {firmantes[1]}"
        else:
            notario_firmantes = f"{', '.join(firmantes[:-1])} y {firmantes[-1]}"

        dpis = [deudor_dpi] + [a["dpi"] for a in avalistas if a.get("dpi")]
        notario_cui_firmantes = [cui_dpi_a_letras(d)[0] if d else "________________" for d in dpis]

        datos = {
            "acreedor_nombre_corto": "EL TELAR, S.A.",
            "acreedor_nombre_completo": "INVERSIONES INTEGRALES EL TELAR, SOCIEDAD ANONIMA",
            "capital_adeudado": float(credito.monto),
            "plazo_meses": credito.plazo,
            "fecha_vencimiento": fecha_a_texto_estandar(credito.fecha_vencimiento) if isinstance(credito.fecha_vencimiento, (date, datetime)) else str(credito.fecha_vencimiento),
            "deudor_nombre": deudor_nombre,
            "deudor_dpi": deudor_dpi,
            "deudor_dpi_letras": cui_dpi_a_letras(deudor_dpi)[0] if deudor_dpi else "",
            "deudor_nit": deudor_nit,
            "deudor_nit_letras": nit_a_letras(deudor_nit) if deudor_nit else "",
            "tasa_interes": tasa,
            "tasa_interes_letras": porcentaje_a_letras(tasa),
            "banco_nombre": "Banco de Desarrollo Rural, Banrural",
            "cuenta_bancaria": "3696008759",
            "cuenta_bancaria_letras": cuenta_a_letras("3696008759"),
            "numero_cuotas": credito.plazo,
            "numero_cuotas_letras": numero_a_letras(credito.plazo).upper(),
            "amortizaciones_capital_texto": "una (1) amortización (es)",
            "amortizaciones_interes_cuotas": f"{cuotas_a_letras(credito.plazo)} amortización(es)",
            "porcentaje_atraso": "diez por ciento (10%)",
            "direccion_notificaciones": direccion_str,
            "lugar_emision": "Cobán, Alta Verapaz",
            "fecha_emision": fecha_a_texto_estandar(credito.fecha_inicio or date.today()),
            "incluir_aval": bool(avalistas),
            "avalistas": avalistas,
            "aval_monto": float(credito.monto),
            "aval_monto_letras": monto_a_letras_quetzales(float(credito.monto)).replace(" QUETZALES EXACTOS", ""),
            "aval_lugar_fecha": "________________________________________________________________",
            "incluir_autentica": True,
            "notario_ciudad": "Cobán",
            "notario_departamento": "Alta Verapaz",
            "notario_fecha_letras": fecha_a_texto_notarial(credito.fecha_inicio or date.today()),
            "notario_firmantes": notario_firmantes,
            "notario_cui_firmantes": notario_cui_firmantes,
        }

        if aval_info:
            datos.update(aval_info)
        if notario_info:
            datos.update(notario_info)

    return generar_pagare_word(datos, output_target=output_target)


generar_pagare_desde_solicitud = generar_pagare_desde_credito
