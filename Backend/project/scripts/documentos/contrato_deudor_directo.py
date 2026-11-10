"""
Módulo para la generación del CONTRATO DE RECONOCIMIENTO DE DEUDA - DEUDOR DIRECTO (SIN FIADOR)
en formato Word (.docx).
Diseñado para El Telar S.A.
Plantilla basada en el caso Candy Claramaría Cantoral Caal de Papa.
Soporta garantía mobiliaria (empresa mercantil) o laboral (sueldo institucional).
"""

import io
from datetime import date, datetime
from decimal import Decimal

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

from .helpers import (
    numero_a_letras,
    formato_quetzales,
    monto_a_letras_quetzales,
    cui_dpi_a_letras,
    edad_a_letras,
    fecha_a_texto_notarial,
)


def obtener_datos_ejemplo_deudor_directo() -> dict:
    """
    Retorna un diccionario con los datos de ejemplo exactos de la plantilla
    proporcionada (CANDY CLARAMARÍA CANTORAL CAAL DE PAPA).
    """
    return {
        "ciudad": "Cobán",
        "departamento": "Alta Verapaz",
        "fecha_contrato_letras": "siete de enero del año dos mil veintiséis",
        # Deudor
        "deudor_nombre": "CANDY CLARAMARÍA CANTORAL CAAL DE PAPA",
        "deudor_edad_letras": "treinta y tres",
        "deudor_estado_civil": "casada",
        "deudor_nacionalidad": "guatemalteca",
        "deudor_profesion": "Maestra de Educación Primaria",
        "deudor_domicilio": "de este domicilio",
        "deudor_dpi": "2159 83866 1608",
        "deudor_cui_letras": "dos mil ciento cincuenta y nueve espacio ochenta y tres mil ochocientos sesenta y seis espacio un mil ochocientos tres",
        "deudor_direccion": "cero calle B, zona cuatro, Barrio Chamché, de la jurisdicción municipal de Tactic del departamento de Alta Verapaz",
        # Representante Legal El Telar
        "rep_legal_nombre": "EDGAR ARMANDO ALVARADO BERMÚDEZ",
        "rep_legal_edad_letras": "cuarenta y un",
        "rep_legal_estado_civil": "soltero",
        "rep_legal_nacionalidad": "guatemalteco",
        "rep_legal_profesion": "Ingeniero Civil",
        "rep_legal_domicilio": "de este domicilio",
        "rep_legal_dpi": "1837 11882 1601",
        "rep_legal_cui_letras": "un mil ochocientos treinta y siete espacio once mil ochocientos ochenta y dos espacio un mil seiscientos uno",
        "rep_legal_cargo": "ADMINISTRADOR ÚNICO Y REPRESENTANTE LEGAL",
        # Empresa El Telar
        "empresa_nombre": "INVERSIONES INTEGRALES EL TELAR, SOCIEDAD ANÓNIMA",
        "empresa_cuenta_bancaria": "3696008759",
        "empresa_direccion": "octava avenida uno guion doce, zona uno, de la jurisdicción municipal de Cobán del departamento de Alta Verapaz",
        # Registro Mercantil El Telar
        "reg_acta_nombramiento_fecha": "diecisiete de junio del año dos mil veinticuatro",
        "reg_notario_nombramiento": "Adán Leal Natareno",
        "reg_numero_nombramiento": "SETECIENTOS CUARENTA Y SIETE MIL SEISCIENTOS CINCO (747605)",
        "reg_folio_nombramiento": "SETECIENTOS NOVENTA Y SIETE (797)",
        "reg_libro_nombramiento": "OCHOCIENTOS TREINTA Y TRES (833), de Auxiliares de Comercio",
        "reg_expediente_nombramiento": "SETENTA Y TRES MIL CUARENTA GUION DOS MIL VEINTICUATRO (73040-2024)",
        "reg_fecha_inscripcion_nombramiento": "veinticinco de junio del año dos mil veinticuatro",
        "reg_doc_numero_rm": "quinientos veintisiete mil cuatrocientos noventa y tres",
        "reg_sociedad_numero": "CIENTO SESENTA Y SEIS MIL CIENTO VEINTE (166120)",
        "reg_sociedad_folio": "OCHOCIENTOS CINCUENTA Y NUEVE (859)",
        "reg_sociedad_libro": "CUATROCIENTOS NOVENTA Y DOS (492), de Sociedades Mercantiles",
        # Condiciones del Crédito
        "monto_capital": 39634.00,
        "monto_capital_letras": "TREINTA Y NUEVE MIL SEISCIENTOS TREINTA Y CUATRO QUETZALES",
        "plazo_cuotas_letras": "DOCE",
        "desglose_cuotas_texto": (
            "el primer pago será por la cantidad de Cuatro mil trescientos treinta y cuatro quetzales (Q. 4,334.00); "
            "el segundo pago será por la cantidad de cuatro mil ciento cuarenta y siete quetzales (Q. 4,147.00); "
            "el tercer pago será por la cantidad de tres mil novecientos cincuenta y nueve quetzales (Q. 3,959.00); "
            "el cuarto pago será por la cantidad de tres mil setecientos setenta y dos quetzales (Q. 3,772.00); "
            "el quinto pago será por la cantidad de tres mil quinientos ochenta y cuatro quetzales (Q. 3,584.00); "
            "el sexto pago será por la cantidad de tres mil trescientos noventa y siete quetzales (Q. 3,397.00); "
            "el séptimo pago será por la cantidad de tres mil doscientos nueve quetzales (Q. 3,209.00); "
            "el octavo pago será por la cantidad de tres mil veintidós quetzales (Q. 3,022.00); "
            "el noveno pago será por la cantidad de dos mil ochocientos treinta y cuatro quetzales (Q. 2,834.00); "
            "el décimo pago será por la cantidad de dos mil seiscientos cuarenta y seis quetzales (Q. 2,646.00); "
            "el pago décimo primero será por la cantidad de dos mil cuatrocientos cincuenta y nueve quetzales (Q. 2,459.00); "
            "y, un último pago al vencimiento de la obligación que será por la cantidad de dos mil doscientos setenta y dos (Q. 2,271.00); "
            "debiendo hacer el primer pago el día siete de febrero del año dos mil veintiséis; "
            "y, los pagos mensuales subsiguientes los días siete de cada mes calendario; "
            "y, un último pago al vencimiento de la obligación el día siete de enero del año dos mil veintisiete."
        ),
        "destino_credito": "comercio y capital de trabajo",
        "tasa_interes_letras": "DIEZ POR CIENTO",
        "tasa_interes_num": "10",
        "multa_mora_pct": "10",
        "resolucion_ente": "------",
        "acta_numero": "--- guion de fecha -----",
        # Garantía (soporta MOBILIARIA o LABORAL)
        "tipo_garantia": "MOBILIARIA",  # o "LABORAL"
        "garantia_texto": (
            "garantía mobiliaria sobre la empresa mercantil de mi propiedad bajo los siguientes datos registrales: "
            "Empresa mercantil de nombre Comercial Agrícola W&A, inscrita en el Registro Mercantil bajo el número 1002212; "
            "folio 401; del libro 1182, de Empresas Mercantiles."
        ),
        # Notario
        "notario_fecha_letras": "siete de enero del año dos mil veintiséis",
        "notario_dpi_deudor": "2159 83866 1603",
    }


def _preparar_datos_deudor_directo(datos_entrada: dict | None) -> dict:
    datos = obtener_datos_ejemplo_deudor_directo()
    if datos_entrada:
        datos.update(datos_entrada)

    # Formatos automáticos de capital
    cap = datos.get("monto_capital", 39634.00)
    try:
        cap_val = float(cap)
    except (ValueError, TypeError):
        cap_val = 0.0
    datos["monto_capital_formato"] = formato_quetzales(cap_val)
    if "monto_capital_letras" not in datos or not datos["monto_capital_letras"]:
        datos["monto_capital_letras"] = monto_a_letras_quetzales(cap_val).replace(" EXACTOS", "")

    # DPI deudor
    cui_raw = datos.get("deudor_dpi", "")
    if cui_raw:
        letras_cui, form_cui = cui_dpi_a_letras(cui_raw, con_espacio=True)
        if "deudor_cui_letras" not in datos or not datos["deudor_cui_letras"]:
            datos["deudor_cui_letras"] = letras_cui
        if "deudor_dpi_formateado" not in datos:
            datos["deudor_dpi_formateado"] = form_cui
    else:
        datos["deudor_dpi_formateado"] = ""

    # Garantía si se eligió tipo LABORAL pero no se especificó texto
    if datos.get("tipo_garantia") == "LABORAL" and "garantia_texto" not in datos_entrada:
        datos["garantia_texto"] = (
            "el sueldo que devengo como empleada del INSTITUTO NACIONAL DE BOSQUES -INAB-, "
            "como secretaria Subregional de la Dirección Subregional II-1 Santa Cruz Verapaz "
            "de la Dirección Regional II - Alta Verapaz e Ixcán."
        )

    return datos


def generar_contrato_deudor_directo_word(datos_entrada: dict | None = None, output_target=None):
    """
    Genera el archivo Word (.docx) del Contrato de Reconocimiento de Deuda para Deudor Directo.

    Retorno:
    --------
    io.BytesIO o str (si output_target es una ruta de archivo)
    """
    datos = _preparar_datos_deudor_directo(datos_entrada)

    doc = Document()
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.5)
        section.page_height = Inches(11.0)

    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(10.5)
    style.font.color.rgb = RGBColor(20, 20, 20)

    # 1. COMPARECENCIA Y ANTECEDENTES
    p_intro = doc.add_paragraph()
    p_intro.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_intro.paragraph_format.line_spacing = 1.15
    p_intro.paragraph_format.space_after = Pt(8)

    p_intro.add_run(
        f"En la Ciudad de {datos['ciudad']} del departamento de {datos['departamento']}, a {datos['fecha_contrato_letras']}. "
    )
    p_intro.add_run("NOSOTROS: ").bold = True
    p_intro.add_run(
        f"por una parte Yo, {datos['deudor_nombre']}, de {datos['deudor_edad_letras']} años de edad, "
        f"{datos['deudor_estado_civil']}, {datos['deudor_nacionalidad']}, {datos['deudor_profesion']}, {datos['deudor_domicilio']}, "
        "me identifico con el Documento Personal de Identificación –DPI- Código Único de Identificación número "
        f"{datos['deudor_cui_letras']} ({datos['deudor_dpi_formateado'] or datos['deudor_dpi']}); extendido por el "
        "Registro Nacional de las Personas –RENAP-, de la República de Guatemala; "
        f"y por la otra parte Yo, {datos['rep_legal_nombre']}, de {datos['rep_legal_edad_letras']} años de edad, "
        f"{datos['rep_legal_estado_civil']}, {datos['rep_legal_nacionalidad']}, {datos['rep_legal_profesion']}, {datos['rep_legal_domicilio']}, "
        "me identifico con el Documento Personal de Identificación –DPI- Código Único de Identificación número "
        f"{datos['rep_legal_cui_letras']} ({datos['rep_legal_dpi']}); extendido por el Registro Nacional de las Personas –RENAP- "
        f"de la República de Guatemala; actúo en mi calidad de {datos['rep_legal_cargo']} de la entidad denominada "
        f"{datos['empresa_nombre']}, calidad que acredito con mi nombramiento, el cual está contenido en el acta notarial "
        f"que contiene mi nombramiento, autorizada en la ciudad de Cobán Alta Verapaz, de fecha {datos['reg_acta_nombramiento_fecha']}, "
        f"por el Notario {datos['reg_notario_nombramiento']}, la que se encuentra debidamente inscrita en el Registro Mercantil "
        f"bajo el número {datos['reg_numero_nombramiento']}, folio {datos['reg_folio_nombramiento']}, del libro {datos['reg_libro_nombramiento']}, "
        f"según expediente número {datos['reg_expediente_nombramiento']}, según inscripción de fecha {datos['reg_fecha_inscripcion_nombramiento']}; "
        f"según documento emitido por el Registro Mercantil con número {datos['reg_doc_numero_rm']}; documento en el que hago constar "
        f"que la empresa denominada {datos['empresa_nombre']}, se encuentra debidamente inscrita en el Registro Mercantil, "
        f"bajo el número {datos['reg_sociedad_numero']}, folio {datos['reg_sociedad_folio']}, del libro {datos['reg_sociedad_libro']}, "
        "manifiesto en la calidad en la que actúo que en el curso del presente documento mi representada será denominada simplemente "
        "como la parte acreedora o la entidad acreedora. Todos aseguramos ser de las generales consignadas, hallarnos en el libre ejercicio "
        "de nuestros derechos civiles y que por el presente acto celebramos "
    )
    p_intro.add_run("CONTRATO DE RECONOCIMIENTO DE DEUDA").bold = True
    p_intro.add_run(", contenido en las cláusulas siguientes:")

    # 2. CLÁUSULA PRIMERA
    p_primera = doc.add_paragraph()
    p_primera.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_primera.paragraph_format.line_spacing = 1.15
    p_primera.paragraph_format.space_after = Pt(8)

    p_primera.add_run("PRIMERA: ").bold = True
    p_primera.add_run(
        f"Yo, {datos['deudor_nombre']}, declaro que me reconozco LISA Y LLANA DEUDORA, de la entidad {datos['empresa_nombre']}, "
        f"por medio de su {datos['rep_legal_cargo']}, representada por el señor {datos['rep_legal_nombre']}, por la cantidad de "
        f"{datos['monto_capital_letras']}, ({datos['monto_capital_formato']}). El reconocimiento se regirá bajo las condiciones siguientes:\n"
        f"a) LA FORMA DE PAGO: El pago de la deuda será a través de {datos['plazo_cuotas_letras']} CUOTAS MENSUALES, distribuidos de la siguiente manera: "
        f"{datos['desglose_cuotas_texto']} "
        f"Los pagos deberán efectuarse mediante deposito a la cuenta monetaria número {datos['empresa_cuenta_bancaria']} a nombre de la empresa denominada "
        f"{datos['empresa_nombre']}, empresa ubicada en la {datos['empresa_direccion']}, sin necesidad de requerimiento o cobro alguno;\n"
        f"b) Manifiesto yo, {datos['deudor_nombre']}, que la cantidad que me fue otorgada por la entidad acreedora, la invertiré exclusivamente en: "
        f"{datos['destino_credito']}, tal y como consta en mi solicitud de crédito;\n"
        f"c) Comprometiéndome desde ya a pagar una tasa de interés del {datos['tasa_interes_letras']} ({datos['tasa_interes_num']}%), mensual, sin que estos se capitalicen, "
        "pudiendo variar en el transcurso del plazo, si el pago de los intereses y capital no se efectúa en la fecha establecida en este contrato "
        f"de reconocimiento de deuda la entidad acreedora, tendrá derecho de cobrar en concepto de multa la cantidad de {datos['multa_mora_pct']}% sobre el monto de "
        "intereses vencidos, iniciando el día inmediato posterior a la fecha de pago acordada, la multa por morosidad permanecerá constante "
        f"hasta que el saldo quede al día tal como se me indicó previamente en la empresa {datos['empresa_nombre']};\n"
        f"d) Autorizo que este crédito sea cedible o negociable, sin necesidad que la empresa {datos['empresa_nombre']}, me de aviso previo o posterior notificación;\n"
        f"e) La falta de pago de la cantidad adeudada, dará derecho a la entidad: {datos['empresa_nombre']}, por medio de su {datos['rep_legal_cargo']}, "
        f"representada por el señor {datos['rep_legal_nombre']}, a dar por vencido el plazo y al cobro de la cantidad adeudada, intereses y costas procesales "
        "y el presente documento debidamente legalizado por Notario en sus firmas servirá de título ejecutivo para iniciar el juicio correspondiente "
        "y en esta forma se podrá dar por vencido el plazo si se da el dinero mutuado un destino diferente para el que fue concedido según la solicitud "
        f"de crédito y la resolución emitida por {datos['resolucion_ente']} de la empresa {datos['empresa_nombre']}, contenida en Acta número "
        f"{datos['acta_numero']} mediante la cual fue autorizado el presente Crédito;\n"
        f"f) La falta de pago de la cantidad adeudada, dará derecho a la entidad: {datos['empresa_nombre']}, por medio de su {datos['rep_legal_cargo']}, "
        f"representada por el señor {datos['rep_legal_nombre']}, a dar por vencido el plazo y al cobro de la cantidad adeudada, intereses y costas procesales "
        "y del presente documento debidamente legalizado por Notario en sus firmas servirá de título ejecutivo para iniciar el juicio correspondiente;\n"
        f"g) Para los efectos legales, yo, {datos['deudor_nombre']}, renuncio al fuero de mi domicilio y me sujeto expresamente a los tribunales que la acreedora elija, "
        f"señalando desde ya como lugar para recibir citaciones, notificaciones y emplazamientos en la siguiente dirección: {datos['deudor_direccion']}, "
        "casa plenamente conocida, lugar donde resido actualmente; y acepto como buenas, exactas, de plazo vencido, líquidas y exigibles las cantidades "
        "que a consecuencia de este crédito se me presenten en caso de incumplimiento a cualquiera de las estipulaciones de este contrato, y si cambiará de dirección "
        f"tengo la obligación de comunicarlo a la entidad {datos['empresa_nombre']}, por medio de su {datos['rep_legal_cargo']}, representada por el señor "
        f"{datos['rep_legal_nombre']}, caso contrario las citaciones, notificaciones y emplazamientos se me harán en la dirección antes indicada y se tendrán como válidas;\n"
        f"h) LA GARANTÍA DE PAGO: Yo, {datos['deudor_nombre']}, garantizo la deuda, intereses, multa por morosidad y costas procesales con {datos['garantia_texto']}."
    )

    # 3. CLÁUSULA SEGUNDA
    p_segunda = doc.add_paragraph()
    p_segunda.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_segunda.paragraph_format.line_spacing = 1.15
    p_segunda.paragraph_format.space_after = Pt(8)
    p_segunda.add_run("SEGUNDA: ").bold = True
    p_segunda.add_run(
        f"Por mi parte Yo, {datos['rep_legal_nombre']}, en mi calidad de {datos['rep_legal_cargo']} de la entidad denominada "
        f"{datos['empresa_nombre']}, expreso que en los términos relacionados ACEPTO EXPRESAMENTE, para mi representada el contenido íntegro del presente contrato."
    )

    # 4. CLÁUSULA TERCERA
    p_tercera = doc.add_paragraph()
    p_tercera.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_tercera.paragraph_format.line_spacing = 1.15
    p_tercera.paragraph_format.space_after = Pt(14)
    p_tercera.add_run("TERCERA: ").bold = True
    p_tercera.add_run(
        "Todos los que intervenimos en este contrato, en las calidades en que actuamos declaramos que ACEPTAMOS EXPRESAMENTE, "
        "el contenido íntegro del presente. Leemos lo escrito y bien impuestos de su contenido, objeto, valor y demás efectos legales, "
        "lo aceptamos, ratificamos y firmamos."
    )

    # 5. LÍNEAS DE FIRMA (2 FIRMAS: DEUDOR Y REPRESENTANTE LEGAL)
    tabla_firmas = doc.add_table(rows=1, cols=2)
    tabla_firmas.alignment = WD_TABLE_ALIGNMENT.CENTER
    tabla_firmas.autofit = False
    tabla_firmas.columns[0].width = Inches(3.2)
    tabla_firmas.columns[1].width = Inches(3.2)

    c0 = tabla_firmas.cell(0, 0).paragraphs[0]
    c0.paragraph_format.space_after = Pt(14)
    c0.add_run("f.____________________________\n").bold = True
    c0.add_run(f"DEUDORA\n{datos['deudor_nombre']}")

    c1 = tabla_firmas.cell(0, 1).paragraphs[0]
    c1.paragraph_format.space_after = Pt(14)
    c1.add_run("f.____________________________\n").bold = True
    c1.add_run(f"REPRESENTANTE LEGAL\n{datos['empresa_nombre']}")

    # 6. ACTA NOTARIAL DE LEGALIZACIÓN DE FIRMAS
    p_notario = doc.add_paragraph()
    p_notario.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_notario.paragraph_format.line_spacing = 1.15
    p_notario.paragraph_format.space_before = Pt(14)
    p_notario.paragraph_format.space_after = Pt(14)

    p_notario.add_run(
        f"En la Ciudad de {datos['ciudad']} del departamento de {datos['departamento']}, a {datos['notario_fecha_letras']}. "
        "Como Notario en ejercicio "
    )
    p_notario.add_run("DOY FE: ").bold = True
    p_notario.add_run("Que las firmas que anteceden son ")
    p_notario.add_run("AUTÉNTICAS").bold = True
    p_notario.add_run(
        ", por haber sido puestas en el CONTRATO DE RECONOCIMIENTO DE DEUDA, día de hoy a mi presencia por los señores: "
        f"{datos['deudor_nombre']}, quien se identifica con el Documento Personal de Identificación –DPI– Código Único de Identificación "
        f"número {datos['deudor_cui_letras']} ({datos.get('notario_dpi_deudor') or datos['deudor_dpi_formateado'] or datos['deudor_dpi']}), "
        "extendido por el Registro Nacional de las Personas –RENAP–, de la República de Guatemala; y, "
        f"{datos['rep_legal_nombre']}, en la calidad en que actúa como {datos['rep_legal_cargo']} de la entidad denominada "
        f"{datos['empresa_nombre']}, quien se identifica con el Documento Personal de Identificación –DPI– Código Único de Identificación "
        f"número {datos['rep_legal_cui_letras']} ({datos['rep_legal_dpi']}), extendido por el Registro Nacional de las Personas –RENAP–, "
        "de la República de Guatemala, quienes vuelven a firmar junto conmigo la presente acta de legalización de firmas."
    )

    # Líneas de firmas del acta notarial
    tabla_not = doc.add_table(rows=1, cols=2)
    tabla_not.alignment = WD_TABLE_ALIGNMENT.CENTER
    tabla_not.autofit = False
    tabla_not.columns[0].width = Inches(3.2)
    tabla_not.columns[1].width = Inches(3.2)

    cn0 = tabla_not.cell(0, 0).paragraphs[0]
    cn0.paragraph_format.space_after = Pt(14)
    cn0.add_run("f.____________________________\n").bold = True
    cn0.add_run(f"DEUDORA\n{datos['deudor_nombre']}")

    cn1 = tabla_not.cell(0, 1).paragraphs[0]
    cn1.paragraph_format.space_after = Pt(14)
    cn1.add_run("f.____________________________\n").bold = True
    cn1.add_run(f"REPRESENTANTE LEGAL\n{datos['empresa_nombre']}")

    p_ante = doc.add_paragraph()
    p_ante.paragraph_format.space_before = Pt(14)
    p_ante.add_run("ANTE MI:").bold = True

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
