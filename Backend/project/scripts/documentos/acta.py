"""
Módulo para la generación del ACTA NOTARIAL DE ENTREGA DE CHEQUE Y COMPROMISO DE PAGO
en formato Word (.docx).
Diseñado para Inversiones Integrales El Telar S.A., compatible tanto con llamadas directas
(diccionario de datos) como extrayendo automáticamente la información desde una
Solicitud de Crédito (InvestmentPlan) o Crédito (Credit).
"""

import io
from datetime import date, datetime, time

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

from .helpers import (
    DIGITOS_LETRAS,
    FECHA_NACIMIENTO_EDGAR_ALVARADO,
    FECHA_NACIMIENTO_GRECIA_RODRIGUEZ,
    numero_a_letras,
    formato_quetzales,
    monto_a_letras_quetzales,
    bloque_a_letras,
    cui_dpi_a_letras,
    edad_a_letras,
    edad_notarial_desde_fecha,
    fecha_a_texto_notarial,
    resolver_solicitud_o_credito,
    extraer_persona_notarial,
)


def digitos_a_letras_minusculas(valor: str) -> str:
    """
    Convierte una secuencia de dígitos a lectura dígito a dígito en minúsculas,
    conservando ceros iniciales.
    Ejemplo: '00000388' -> 'cero cero cero cero cero tres ocho ocho'
             '3197005470' -> 'tres uno nueve siete cero cero cinco cuatro siete cero'
    """
    if not valor:
        return ""
    partes = []
    for ch in str(valor).strip():
        if ch in DIGITOS_LETRAS:
            partes.append(DIGITOS_LETRAS[ch])
        elif ch.isalnum():
            partes.append(ch.lower())
    return " ".join(partes)


def cui_dpi_a_letras_acta(cui_raw: str) -> tuple[str, str]:
    """
    Formatea un CUI/DPI guatemalteco (13 dígitos) en el estilo del Acta Notarial:
    primer bloque capitalizado y bloques separados por coma, usando 'un mil' en bloques 1 y 3.
    Ejemplo: '1837 11882 1601' ->
      ('Un mil ochocientos treinta y siete, once mil ochocientos ochenta y dos, un mil seiscientos uno',
       '1837 11882 1601')
    """
    if not cui_raw:
        return ("", "")

    limpio = "".join(c for c in str(cui_raw) if c.isdigit())
    if len(limpio) != 13:
        return cui_dpi_a_letras(cui_raw, con_espacio=False)

    p1 = limpio[0:4]
    p2 = limpio[4:9]
    p3 = limpio[9:13]
    formateado = f"{p1} {p2} {p3}"

    try:
        w1 = bloque_a_letras(p1, usar_un_mil=True)
        w1 = w1[0].upper() + w1[1:] if w1 else w1
        w2 = bloque_a_letras(p2, usar_un_mil=False)
        w3 = bloque_a_letras(p3, usar_un_mil=True)
        return (f"{w1}, {w2}, {w3}", formateado)
    except Exception:
        return (formateado, formateado)


def hora_a_texto_notarial(valor=None) -> str:
    """
    Convierte una hora (datetime, time o string 'HH:MM') a formato notarial en letras.
    Ejemplos:
      15:00 -> 'quince horas'
      08:15 -> 'ocho horas con quince minutos'
      01:01 -> 'una hora con un minuto'
    """
    if isinstance(valor, str):
        limpio = valor.strip()
        if ":" in limpio:
            try:
                partes = limpio.split(":")
                h = int(partes[0])
                m = int(partes[1])
            except (ValueError, IndexError):
                return limpio
        else:
            return limpio
    elif isinstance(valor, datetime):
        h, m = valor.hour, valor.minute
    elif isinstance(valor, time):
        h, m = valor.hour, valor.minute
    else:
        ahora = datetime.now()
        h, m = ahora.hour, ahora.minute

    if h == 1:
        hora_txt = "una hora"
    elif h == 21:
        hora_txt = "veintiuna horas"
    else:
        hora_txt = f"{numero_a_letras(h, mayusculas=False)} horas"

    if m == 0:
        return hora_txt

    if m == 1:
        min_txt = "un minuto"
    elif m == 21:
        min_txt = "veintiún minutos"
    else:
        min_txt = f"{numero_a_letras(m, mayusculas=False)} minutos"

    return f"{hora_txt} con {min_txt}"


REQUIRENTE_1_HOMBRE = {
    "req1_nombre": "EDGAR ARMANDO ALVARADO BERMÚDEZ",
    "req1_genero": "M",
    "req1_fecha_nacimiento": FECHA_NACIMIENTO_EDGAR_ALVARADO,
    "req1_estado_civil": "soltero",
    "req1_nacionalidad": "guatemalteco",
    "req1_profesion": "Ingeniero Civil",
    "req1_domicilio": "de este domicilio",
    "req1_dpi": "1837 11882 1601",
    "req1_cui_letras": "Un mil ochocientos treinta y siete, once mil ochocientos ochenta y dos, un mil seiscientos uno",
}

REQUIRENTE_1_MUJER = {
    "req1_nombre": "GRECIA MAYARI RODRIGUEZ ROQUEL",
    "req1_genero": "F",
    "req1_fecha_nacimiento": FECHA_NACIMIENTO_GRECIA_RODRIGUEZ,
    "req1_estado_civil": "soltera",
    "req1_nacionalidad": "guatemalteca",
    "req1_profesion": "comerciante",
    "req1_domicilio": "de paso por este municipio",
    "req1_dpi": "2341 24938 2101",
    "req1_cui_letras": "Dos mil trescientos cuarenta y uno, veinticuatro mil novecientos treinta y ocho, dos mil ciento uno",
}


def _obtener_requirente_1_por_genero(
    genero_deudor: str | None,
    fecha_referencia: date | datetime | str | None = None,
) -> dict:
    """
    Retorna los datos del Requirente 1 según el género del deudor, calculando su edad
    automáticamente desde su fecha de nacimiento:
      - Mujer ('F') -> GRECIA MAYARI RODRIGUEZ ROQUEL (14/12/1987)
      - Hombre ('M') -> EDGAR ARMANDO ALVARADO BERMÚDEZ (15/02/1985)
    """
    g = str(genero_deudor or "M").strip().upper()
    base = dict(REQUIRENTE_1_MUJER if (g.startswith("F") or "MUJ" in g) else REQUIRENTE_1_HOMBRE)
    fecha_nac = base.pop("req1_fecha_nacimiento")
    edad_num, edad_letras = edad_notarial_desde_fecha(fecha_nac, fecha_referencia=fecha_referencia)
    base["req1_edad_num"] = edad_num
    base["req1_edad_letras"] = edad_letras
    return base


def obtener_datos_ejemplo_acta(ejemplo: int = 2) -> dict:
    """
    Retorna datos de ejemplo reales del Acta Notarial de entrega de cheque:
      - ejemplo=2 (por defecto): Edgar Armando Alvarado Bermúdez y Victor Humberto Cú Isém (Q.3,789.00)
      - ejemplo=1: Grecia Mayari Rodriguez Roquel y Stella Floridalma Cal Jom de Castro (Q.39,600.00)
    """
    if ejemplo == 1:
        return {
            "ciudad": "Cobán",
            "departamento": "Alta Verapaz",
            "hora_letras": "quince horas",
            "fecha_acta_letras": "treinta de noviembre del año dos mil veintitrés",
            # Notario
            "notario_nombre": "ADAN LEAL NATARENO",
            "notario_colegiado_texto": "catorce mil novecientos cuarenta (14,940)",
            "notario_oficina": 'la séptima avenida dos guion dieciocho “A” de la zona uno de Cobán, del departamento de Alta Verapaz',
            # Requirente 1 (Mujer -> Grecia Mayari Rodriguez Roquel, edad dinámica)
            **_obtener_requirente_1_por_genero("F"),
            # Requirente 2 (Deudora / Quien entrega el cheque)
            "req2_nombre": "STELLA FLORIDALMA CAL JOM DE CASTRO",
            "req2_genero": "F",
            "req2_edad_letras": "cuarenta y dos",
            "req2_estado_civil": "casada",
            "req2_nacionalidad": "guatemalteca",
            "req2_profesion": "comerciante",
            "req2_domicilio": "de este domicilio",
            "req2_dpi": "2581 70743 1601",
            "req2_cui_letras": "Dos mil quinientos ochenta y uno, setenta mil setecientos cuarenta y tres, un mil seiscientos uno",
            # Datos del Cheque
            "cheque_numero": "25400073",
            "cuenta_numero": "3030886155",
            "cuenta_nombre": "STELLA CAL JOM",
            "cuenta_nombre_legal": "STELLA CAL JOM",
            "cuenta_titular_dpi": "2581 70743 1601",
            "banco_nombre": "BANCO AGROMERCANTIL DE GUATEMALA S. A.",
            "monto": 39600.00,
        }

    return {
        "ciudad": "Cobán",
        "departamento": "Alta Verapaz",
        "hora_letras": "ocho horas con quince minutos",
        "fecha_acta_letras": "diez de septiembre del año dos mil veinticinco",
        # Notario
        "notario_nombre": "ADAN LEAL NATARENO",
        "notario_colegiado_texto": "catorce mil novecientos cuarenta (14,940)",
        "notario_oficina": 'la séptima avenida dos guion dieciocho “A” de la zona uno de Cobán, del departamento de Alta Verapaz',
        # Requirente 1 (Hombre -> Edgar Armando Alvarado Bermúdez, edad dinámica)
        **_obtener_requirente_1_por_genero("M"),
        # Requirente 2 (Cliente / Librador del cheque)
        "req2_nombre": "VICTOR HUMBERTO CÚ ISÉM",
        "req2_genero": "M",
        "req2_edad_letras": "sesenta y dos",
        "req2_estado_civil": "soltero",
        "req2_nacionalidad": "guatemalteco",
        "req2_profesion": "comerciante",
        "req2_domicilio": "de este domicilio",
        "req2_dpi": "2462 09984 1604",
        "req2_cui_letras": "Dos mil cuatrocientos sesenta y dos, cero noventa mil novecientos ochenta y cuatro, un mil seiscientos cuatro",
        # Datos del Cheque
        "cheque_numero": "00000388",
        "cuenta_numero": "3197005470",
        "cuenta_nombre": "VICTOR HUMBERTO CÚ ISÉM",
        "cuenta_nombre_legal": "VICTOR HUMBERTO CÚ ISÉM",
        "cuenta_titular_dpi": "2462 09984 1604",
        "banco_nombre": "BANCO DE DESARROLLO RURAL S.A.",
        "monto": 3789.00,
    }


def _preparar_datos_acta(datos_entrada: dict | None) -> dict:
    """Normaliza y calcula campos derivados (letras de DPI, cheque, cuenta, monto, hora y género)."""
    datos = obtener_datos_ejemplo_acta(ejemplo=2)
    entrada = datos_entrada if isinstance(datos_entrada, dict) else {}
    fecha_ref = entrada.get("fecha")

    # Si no se especificó explícitamente req1_nombre, seleccionar Requirente 1 según género del deudor (req2_genero)
    if "req1_nombre" not in entrada:
        genero_ref = entrada.get("req2_genero", datos.get("req2_genero"))
        datos.update(_obtener_requirente_1_por_genero(genero_ref, fecha_referencia=fecha_ref))

    datos.update(entrada)

    # Hora y fecha
    if isinstance(datos.get("hora"), (datetime, time, str)) and "hora_letras" not in entrada:
        datos["hora_letras"] = hora_a_texto_notarial(datos["hora"])
    elif not datos.get("hora_letras"):
        datos["hora_letras"] = hora_a_texto_notarial()

    if isinstance(datos.get("fecha"), (date, datetime, str)) and "fecha_acta_letras" not in entrada:
        datos["fecha_acta_letras"] = fecha_a_texto_notarial(datos["fecha"])
    elif not datos.get("fecha_acta_letras"):
        datos["fecha_acta_letras"] = fecha_a_texto_notarial(date.today())

    # Normalizar nombres en mayúsculas
    datos["notario_nombre"] = str(datos.get("notario_nombre") or "ADAN LEAL NATARENO").strip().upper()
    datos["req1_nombre"] = str(datos.get("req1_nombre") or "").strip().upper()
    datos["req2_nombre"] = str(datos.get("req2_nombre") or "").strip().upper()

    # Normalizar géneros ('M' o 'F')
    for pref in ("req1", "req2"):
        g_raw = str(datos.get(f"{pref}_genero") or "M").strip().upper()
        datos[f"{pref}_genero"] = "F" if g_raw.startswith("F") or "MUJ" in g_raw else "M"

        # Edad si pasaron edad numérica sin edad_letras
        if f"{pref}_edad_num" in entrada and f"{pref}_edad_letras" not in entrada:
            datos[f"{pref}_edad_letras"] = edad_a_letras(entrada[f"{pref}_edad_num"])

        # DPI y CUI en letras
        dpi_val = str(datos.get(f"{pref}_dpi") or "").strip()
        if dpi_val:
            cui_l, dpi_f = cui_dpi_a_letras_acta(dpi_val)
            datos[f"{pref}_dpi_formateado"] = dpi_f or dpi_val
            if f"{pref}_cui_letras" not in entrada or not datos.get(f"{pref}_cui_letras"):
                if f"{pref}_dpi" in entrada or not datos.get(f"{pref}_cui_letras"):
                    datos[f"{pref}_cui_letras"] = cui_l
        else:
            datos[f"{pref}_dpi_formateado"] = "________________"
            datos[f"{pref}_cui_letras"] = datos.get(f"{pref}_cui_letras") or "________________"

    # Cheque y cuenta
    cheque_num = str(datos.get("cheque_numero") or "").strip()
    datos["cheque_numero"] = cheque_num or "________"
    if not datos.get("cheque_numero_letras") or "cheque_numero" in entrada:
        cheque_letras = digitos_a_letras_minusculas(cheque_num) if cheque_num else ""
        datos["cheque_numero_letras"] = cheque_letras or "________________"

    cuenta_num = str(datos.get("cuenta_numero") or "").strip()
    datos["cuenta_numero"] = cuenta_num or "________"
    if not datos.get("cuenta_numero_letras") or "cuenta_numero" in entrada:
        cuenta_letras = digitos_a_letras_minusculas(cuenta_num) if cuenta_num else ""
        datos["cuenta_numero_letras"] = cuenta_letras or "________________"

    datos["cuenta_nombre"] = str(datos.get("cuenta_nombre") or datos["req2_nombre"] or "________").strip().upper()
    datos["cuenta_nombre_legal"] = str(
        datos.get("cuenta_nombre_legal") or datos["req2_nombre"] or datos["cuenta_nombre"]
    ).strip().upper()

    titular_dpi_raw = str(datos.get("cuenta_titular_dpi") or datos.get("req2_dpi_formateado") or "").strip()
    if titular_dpi_raw and titular_dpi_raw != "________________":
        _, titular_dpi_f = cui_dpi_a_letras_acta(titular_dpi_raw)
        datos["cuenta_titular_dpi"] = titular_dpi_f or titular_dpi_raw
    else:
        datos["cuenta_titular_dpi"] = datos.get("req2_dpi_formateado") or "________________"

    datos["banco_nombre"] = str(datos.get("banco_nombre") or "________________").strip().upper()

    # Monto
    try:
        monto_val = float(datos.get("monto") or 0)
    except (ValueError, TypeError):
        monto_val = 0.0
    datos["monto"] = monto_val
    datos["monto_formato"] = formato_quetzales(monto_val)
    if not datos.get("monto_letras") or "monto" in entrada:
        datos["monto_letras"] = monto_a_letras_quetzales(monto_val)

    return datos


def generar_acta_word(datos_entrada: dict | None = None, output_target=None):
    """
    Genera el archivo Word (.docx) del Acta Notarial de Entrega de Cheque y Compromiso de Pago.

    Parámetros:
    -----------
    datos_entrada : dict | None
        Diccionario con datos del notario, requirentes, cheque y monto.
    output_target : io.BytesIO | str | None
        Ruta de archivo o stream donde guardar el .docx. Si es None, retorna io.BytesIO.
    """
    datos = _preparar_datos_acta(datos_entrada)

    ambas_mujeres = datos["req1_genero"] == "F" and datos["req2_genero"] == "F"
    art_senores = "las señoras" if ambas_mujeres else "los señores"
    senores_pl = "señoras" if ambas_mujeres else "señores"
    pron_ellos = "ellas" if ambas_mujeres else "ellos"
    art_requirentes = "las requirentes" if ambas_mujeres else "los requirentes"
    advertidos_txt = "advertidas" if ambas_mujeres else "advertidos"
    enterados_txt = "enteradas" if ambas_mujeres else "enterados"

    art_req1 = "la señora" if datos["req1_genero"] == "F" else "el señor"
    art_req2 = "la señora" if datos["req2_genero"] == "F" else "el señor"

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

    # =========================================================================
    # CUERPO DEL ACTA NOTARIAL
    # =========================================================================
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(14)

    # Encabezado, Notario y Requirentes
    p.add_run(
        f"En la ciudad de {datos['ciudad']}, del departamento de {datos['departamento']}, "
        f"siendo las {datos['hora_letras']} del día {datos['fecha_acta_letras']}. "
        f"YO: "
    )
    p.add_run(datos["notario_nombre"]).bold = True
    p.add_run(
        f", Notario, colegiado activo número {datos['notario_colegiado_texto']}, "
        f"constituido en mi oficina profesional ubicada en {datos['notario_oficina']}, "
        f"soy requerido por {art_senores}: "
    )

    # Requirente 1
    p.add_run(datos["req1_nombre"]).bold = True
    p.add_run(
        f", de {datos['req1_edad_letras']} años de edad, {datos['req1_estado_civil']}, "
        f"{datos['req1_nacionalidad']}, {datos['req1_profesion']}, {datos['req1_domicilio']}, "
        "se identifica con Documento Personal de Identificación -DPI- con Código Único de Identificación -CUI- "
        f"número: {datos['req1_cui_letras']} ({datos['req1_dpi_formateado']}) extendido por el "
        "Registro Nacional de las Personas -RENAP- de la República de Guatemala y "
    )

    # Requirente 2
    p.add_run(datos["req2_nombre"]).bold = True
    p.add_run(
        f", de {datos['req2_edad_letras']} años de edad, {datos['req2_estado_civil']}, "
        f"{datos['req2_nacionalidad']}, {datos['req2_profesion']}, {datos['req2_domicilio']}, "
        "se identifica con Documento Personal de Identificación -DPI- con Código Único de Identificación -CUI- "
        f"número {datos['req2_cui_letras']} ({datos['req2_dpi_formateado']}) extendido por el "
        "Registro Nacional de las Personas -RENAP- de la República de Guatemala. "
        "Me aseguran ser de los datos de identificación personal indicados, hallarse en el libre ejercicio de sus "
        "derechos civiles y que por el presente acto comparecen para hacer constar lo siguiente, por lo que se procede "
        "de la manera siguiente: "
    )

    # PRIMERO
    p.add_run("PRIMERO: ").bold = True
    p.add_run(f"Me manifiestan {art_senores}, ")
    p.add_run(datos["req1_nombre"]).bold = True
    p.add_run(" y ")
    p.add_run(datos["req2_nombre"]).bold = True
    p.add_run(f", que por negocio realizado entre {pron_ellos}, {art_req2} ")
    p.add_run(datos["req2_nombre"]).bold = True
    p.add_run(
        f" por este acto le entrega cheque número: {datos['cheque_numero_letras']} ({datos['cheque_numero']}) "
        f"de la cuenta número: {datos['cuenta_numero_letras']} ({datos['cuenta_numero']}) "
        f"cuenta a nombre de "
    )
    p.add_run(datos["cuenta_nombre"]).bold = True
    p.add_run(", nombre que por este acto se aclara corresponde legalmente a ")
    p.add_run(datos["cuenta_nombre_legal"]).bold = True
    p.add_run(
        ", quien se identifica con el Documento Personal de Identificación —DPI— con Código Único de Identidad —CUI— "
        f"número [{datos['cuenta_titular_dpi']}], por tratarse de la misma persona del "
    )
    p.add_run(datos["banco_nombre"]).bold = True
    p.add_run(". Por la cantidad de ")
    p.add_run(f"{datos['monto_letras']} ({datos['monto_formato']})").bold = True
    p.add_run(". ")

    # SEGUNDO
    p.add_run("SEGUNDO: ").bold = True
    p.add_run(f"Siguen manifestando {art_requirentes}, {senores_pl} ")
    p.add_run(datos["req1_nombre"]).bold = True
    p.add_run(" y ")
    p.add_run(datos["req2_nombre"]).bold = True
    p.add_run(", ")
    p.add_run("BAJO JURAMENTO SOLEMNE").bold = True
    p.add_run(
        f" y {advertidos_txt} de las penas relativas al delito de perjurio, "
        f"que por este medio se compromete {art_req1} "
    )
    p.add_run(datos["req1_nombre"]).bold = True
    p.add_run(
        f" a respetar la fecha en la que deberá de cumplirse la obligación de pago por parte de {art_req2} "
    )
    p.add_run(datos["req2_nombre"]).bold = True
    p.add_run(", quien a su vez se compromete a respetar la fecha de pago del mismo. ")

    # TERCERO
    p.add_run("TERCERO: ").bold = True
    p.add_run(
        "Por último y no habiendo más que hacer constar se finaliza la presente acta, "
        f"diez minutos después en el mismo lugar y fecha de su inicio, la que es leída a {art_requirentes}, "
        f"quienes bien {enterados_txt} de su objeto, validez y efectos legales, la ratifican, aceptan y firman "
        "con el Infrascrito Notario que "
    )
    p.add_run("DA FE.").bold = True

    # =========================================================================
    # BLOQUE DE FIRMAS (REQUIRENTES + ANTE MÍ NOTARIO)
    # =========================================================================
    p_esp = doc.add_paragraph()
    p_esp.paragraph_format.space_before = Pt(18)
    p_esp.paragraph_format.space_after = Pt(6)

    tabla_firmas = doc.add_table(rows=1, cols=2)
    tabla_firmas.alignment = WD_TABLE_ALIGNMENT.CENTER
    tabla_firmas.autofit = False
    tabla_firmas.columns[0].width = Inches(3.2)
    tabla_firmas.columns[1].width = Inches(3.2)

    c0 = tabla_firmas.cell(0, 0).paragraphs[0]
    c0.alignment = WD_ALIGN_PARAGRAPH.CENTER
    c0.paragraph_format.space_after = Pt(14)
    c0.add_run("f.____________________________\n").bold = True
    c0.add_run(f"{datos['req1_nombre']}")

    c1 = tabla_firmas.cell(0, 1).paragraphs[0]
    c1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    c1.paragraph_format.space_after = Pt(14)
    c1.add_run("f.____________________________\n").bold = True
    c1.add_run(f"{datos['req2_nombre']}")

    p_ante = doc.add_paragraph()
    p_ante.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ante.paragraph_format.space_before = Pt(18)
    p_ante.paragraph_format.space_after = Pt(28)
    p_ante.add_run("ANTE MÍ:").bold = True

    p_not = doc.add_paragraph()
    p_not.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_not.add_run("f.____________________________\n").bold = True
    p_not.add_run(f"{datos['notario_nombre']}\nNOTARIO")

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


def _extraer_garantia_cheque(solicitud) -> tuple[dict | None, object]:
    """
    Busca una garantía de tipo 'CHEQUE / PAGARE' en:
      1. solicitud.garantias (garantías del deudor)
      2. solicitud.fiador[*]['garantias'] (garantías registradas en algún fiador)
      3. DetailsGuarantees (si es un Credit)
    Retorna (garantia_dict, propietario_customer_obj_or_None).
    """
    garantias_raw = getattr(solicitud, "garantias", None)
    if not garantias_raw and getattr(solicitud, "destino_id", None) is not None:
        garantias_raw = getattr(solicitud.destino_id, "garantias", None)

    if isinstance(garantias_raw, list):
        for g in garantias_raw:
            if not isinstance(g, dict):
                continue
            tg = str(g.get("tipo") or g.get("tipo_garantia") or "").strip().upper()
            if tg == "CHEQUE / PAGARE":
                return (g, getattr(solicitud, "customer_id", None))

    # Revisar garantías dentro de los fiadores
    raw_fiadores = getattr(solicitud, "fiador", None)
    if not raw_fiadores and getattr(solicitud, "destino_id", None) is not None:
        raw_fiadores = getattr(solicitud.destino_id, "fiador", None)
    if isinstance(raw_fiadores, dict):
        raw_fiadores = [raw_fiadores]
    if isinstance(raw_fiadores, list):
        for f_entry in raw_fiadores:
            if not isinstance(f_entry, dict):
                continue
            f_gars = f_entry.get("garantias")
            if not isinstance(f_gars, list):
                continue
            for g in f_gars:
                if not isinstance(g, dict):
                    continue
                tg = str(g.get("tipo") or g.get("tipo_garantia") or "").strip().upper()
                if tg == "CHEQUE / PAGARE":
                    f_obj = None
                    f_id = f_entry.get("id") or f_entry.get("customer_id")
                    if f_id:
                        try:
                            from apps.customers.models import Customer
                            f_obj = Customer.objects.filter(id=f_id).first()
                        except Exception:
                            f_obj = None
                    return (g, f_obj or getattr(solicitud, "customer_id", None))

    # Si es Credit sin garantías JSON, buscar en DetailsGuarantees
    if not hasattr(solicitud, "total_value_of_the_product_or_service") and getattr(solicitud, "id", None):
        try:
            from apps.financings.models import DetailsGuarantees
            det = DetailsGuarantees.objects.filter(
                garantia_id__credit_id=solicitud,
                tipo_garantia="CHEQUE / PAGARE",
            ).order_by("pk").first()
            if det is not None:
                return (
                    {
                        "tipo": det.tipo_garantia,
                        "valor": float(getattr(det, "valor_cobertura", 0) or 0),
                        "especificaciones": det.especificaciones if isinstance(det.especificaciones, dict) else {},
                    },
                    getattr(solicitud, "customer_id", None),
                )
        except Exception:
            pass

    return (None, getattr(solicitud, "customer_id", None))


def extraer_datos_acta_desde_solicitud(solicitud, overrides: dict | None = None) -> dict:
    """
    Extrae toda la información real desde una Solicitud (InvestmentPlan) o Crédito (Credit)
    para generar el Acta Notarial de Entrega de Cheque y Compromiso de Pago.
    """
    cliente = getattr(solicitud, "customer_id", None)
    garantia_cheque, propietario_cheque = _extraer_garantia_cheque(solicitud)
    persona_librador = extraer_persona_notarial(propietario_cheque or cliente, default_genero="M")

    # Ciudad / Departamento desde sucursal
    sucursal = getattr(solicitud, "sucursal", None)
    ciudad = "Cobán"
    departamento = "Alta Verapaz"
    if sucursal is not None:
        suc_addr = getattr(sucursal, "_mock_address", None)
        if suc_addr is None and callable(getattr(sucursal, "get_direc", None)):
            try:
                suc_addr = sucursal.get_direc()
            except Exception:
                suc_addr = None
        if suc_addr is not None and not isinstance(suc_addr, str):
            ciudad = str(getattr(suc_addr, "state", None) or getattr(sucursal, "city", None) or ciudad).strip()
            departamento = str(getattr(suc_addr, "city", None) or getattr(sucursal, "state", None) or departamento).strip()
        else:
            if getattr(sucursal, "city", None):
                ciudad = str(sucursal.city).strip()
            if getattr(sucursal, "state", None):
                departamento = str(sucursal.state).strip()

    # Notario asignado (si se asignó uno diferente a Adán Leal Natareno, respetar su nombre sin mezclar colegiado)
    notario_nombre = "ADAN LEAL NATARENO"
    notario_colegiado_texto = "catorce mil novecientos cuarenta (14,940)"
    notario_oficina = 'la séptima avenida dos guion dieciocho “A” de la zona uno de Cobán, del departamento de Alta Verapaz'

    notarios_raw = getattr(solicitud, "notarios", None)
    if isinstance(notarios_raw, list) and notarios_raw:
        notario_doc = next(
            (n for n in notarios_raw if isinstance(n, dict) and n.get("modulo") == "documentacion" and n.get("nombre")),
            None,
        ) or next(
            (n for n in notarios_raw if isinstance(n, dict) and n.get("nombre")),
            None,
        )
        if notario_doc:
            nom_n = str(notario_doc.get("nombre") or "").strip().upper()
            if nom_n and "ADAN" not in nom_n and "ADÁN" not in nom_n and "LEAL" not in nom_n:
                notario_nombre = nom_n
                notario_colegiado_texto = "________________ (______)"
                notario_oficina = f"la ciudad de {ciudad}, del departamento de {departamento}"

    # Datos del cheque desde la garantía CHEQUE / PAGARE
    specs = {}
    if isinstance(garantia_cheque, dict):
        specs = garantia_cheque.get("especificaciones") if isinstance(garantia_cheque.get("especificaciones"), dict) else {}

    cheque_numero = str(
        specs.get("noCheque") or specs.get("numero_cheque") or specs.get("NoCheque") or ""
    ).strip()
    cuenta_numero = str(
        specs.get("noCuenta") or specs.get("NumeroCuenta") or specs.get("numero_cuenta") or specs.get("cuenta") or ""
    ).strip()
    cuenta_nombre = str(
        specs.get("NombreCuenta") or specs.get("nombre_cuenta") or persona_librador["nombre"] or ""
    ).strip().upper()
    banco_nombre = str(
        specs.get("Banco") or specs.get("banco") or ""
    ).strip().upper()

    capital_solicitud = float(
        getattr(solicitud, "total_value_of_the_product_or_service", None)
        or getattr(solicitud, "monto", 0)
        or 0
    )
    monto_cheque_raw = (
        specs.get("Monto_cheque")
        or (garantia_cheque.get("valor") if isinstance(garantia_cheque, dict) else None)
        or capital_solicitud
    )
    try:
        monto_cheque = float(monto_cheque_raw or 0)
    except (ValueError, TypeError):
        monto_cheque = capital_solicitud

    cui_req2_letras, dpi_req2_fmt = cui_dpi_a_letras_acta(persona_librador["dpi"])
    ahora = datetime.now()
    fecha_ref = overrides.get("fecha") if isinstance(overrides, dict) and overrides.get("fecha") else ahora.date()
    req1_datos = _obtener_requirente_1_por_genero(persona_librador["genero"], fecha_referencia=fecha_ref)

    datos = {
        "ciudad": ciudad,
        "departamento": departamento,
        "hora_letras": hora_a_texto_notarial(ahora),
        "fecha_acta_letras": fecha_a_texto_notarial(ahora.date()),
        # Notario
        "notario_nombre": notario_nombre,
        "notario_colegiado_texto": notario_colegiado_texto,
        "notario_oficina": notario_oficina,
        # Requirente 1 (Hombre -> Edgar Armando Alvarado Bermúdez; Mujer -> Grecia Mayari Rodriguez Roquel)
        **req1_datos,
        # Requirente 2 (Cliente / Librador)
        "req2_nombre": persona_librador["nombre"],
        "req2_genero": persona_librador["genero"],
        "req2_edad_letras": persona_librador["edad_letras"],
        "req2_estado_civil": persona_librador["estado_civil"],
        "req2_nacionalidad": persona_librador["nacionalidad"],
        "req2_profesion": persona_librador["profesion"].lower() if persona_librador["profesion"] else "comerciante",
        "req2_domicilio": persona_librador["domicilio"],
        "req2_dpi": dpi_req2_fmt or persona_librador["dpi"],
        "req2_cui_letras": cui_req2_letras or persona_librador["cui_letras"],
        # Cheque
        "cheque_numero": cheque_numero or "________",
        "cuenta_numero": cuenta_numero or "________",
        "cuenta_nombre": cuenta_nombre or persona_librador["nombre"],
        "cuenta_nombre_legal": persona_librador["nombre"],
        "cuenta_titular_dpi": dpi_req2_fmt or persona_librador["dpi"] or "________________",
        "banco_nombre": banco_nombre or "________________",
        "monto": monto_cheque,
    }

    if overrides and isinstance(overrides, dict):
        datos.update(overrides)

    return datos


def generar_acta_desde_solicitud(solicitud_o_id, overrides: dict | None = None, output_target=None):
    """
    Genera el Acta Notarial de Entrega de Cheque y Compromiso de Pago en Word (.docx)
    extrayendo automáticamente los datos desde una Solicitud (InvestmentPlan) o Crédito (Credit).
    """
    solicitud = resolver_solicitud_o_credito(solicitud_o_id)
    datos = extraer_datos_acta_desde_solicitud(solicitud, overrides=overrides)
    return generar_acta_word(datos, output_target=output_target)


generar_acta_desde_credito = generar_acta_desde_solicitud
