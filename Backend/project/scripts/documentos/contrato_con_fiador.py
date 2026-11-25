"""
Módulo para la generación del CONTRATO DE RECONOCIMIENTO DE DEUDA - CON FIADORES SOLIDARIOS
en formato Word (.docx).
Diseñado para Inversiones Integrales El Telar S.A.
Soporta de forma 100% DINÁMICA cualquier cantidad de fiadores (1, 2, 3, 5 o N fiadores solidarios).
Cada fiador cuenta con su comparecencia individual, cláusula de garantía mancomunada y solidaria,
renuncia al fuero de su domicilio, firma respectiva y legalización notarial en el acta de firmas.
"""

import io
from datetime import date, datetime
from decimal import Decimal

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

from .helpers import (
    FECHA_NACIMIENTO_EDGAR_ALVARADO,
    numero_a_letras,
    formato_quetzales,
    monto_a_letras_quetzales,
    cui_dpi_a_letras,
    edad_a_letras,
    edad_notarial_desde_fecha,
    fecha_a_texto_notarial,
    ordinal,
    resolver_solicitud_o_credito,
    extraer_persona_notarial,
    construir_texto_garantia_item,
    extraer_datos_base_contrato_desde_solicitud,
    _obtener_acta_solicitud,
)


def obtener_datos_ejemplo_con_fiador(cantidad_fiadores: int = 1) -> dict:
    """
    Retorna un diccionario con datos de ejemplo para el contrato con fiador(es).
    Soporta generar 1 o múltiples fiadores solidarios de ejemplo (ej. 2, 3 o 5 fiadores).
    """
    # Fiadores predefinidos con datos notariales completos
    fiadores_catalogo = [
        {
            "nombre": "FREDY JOEL GARCÍA MOSCOSO",
            "edad_letras": "veintiséis",
            "edad_num": 26,
            "estado_civil": "soltero",
            "nacionalidad": "guatemalteco",
            "profesion": "Bachiller en Ciencias y Letras",
            "domicilio": "de este domicilio",
            "dpi": "3268 85188 1604",
            "cui_letras": "tres mil doscientos sesenta y ocho espacio ochenta y cinco mil ciento ochenta y ocho espacio un mil seiscientos cuatro",
            "direccion": "Lotificación Villas del Carmen, zona tres, de la jurisdicción municipal de Tactic del departamento de Alta Verapaz",
            "tipo_garantia": "MOBILIARIA",
            "garantia_texto": (
                "garantía mobiliaria sobre la empresa mercantil de mi propiedad bajo los siguientes datos registrales: "
                "Empresa mercantil de nombre Comercial Agrícola W&A, inscrita en el Registro Mercantil bajo el número 1002212; "
                "folio 401; del libro 1182, de Empresas Mercantiles"
            ),
        },
        {
            "nombre": "CARLOS HUMBERTO XOL CAAL",
            "edad_letras": "treinta y cuatro",
            "edad_num": 34,
            "estado_civil": "casado",
            "nacionalidad": "guatemalteco",
            "profesion": "Perito Contador",
            "domicilio": "de este domicilio",
            "dpi": "2456 78123 1601",
            "cui_letras": "dos mil cuatrocientos cincuenta y seis espacio setenta y ocho mil ciento veintitrés espacio un mil seiscientos uno",
            "direccion": "quinta calle dos guion cuarenta, zona dos, del municipio de Cobán del departamento de Alta Verapaz",
            "tipo_garantia": "LABORAL",
            "lugar_trabajo": "Instituto Nacional de Electrificación INDE",
            "garantia_texto": (
                "el sueldo y salario que devengo como empleado del Instituto Nacional de Electrificación INDE, "
                "en la Planta Hidroeléctrica Chixoy, así como con la totalidad de mis bienes presentes y futuros"
            ),
        },
        {
            "nombre": "MARÍA ELENA POP CHEN",
            "edad_letras": "treinta y un",
            "edad_num": 31,
            "estado_civil": "soltera",
            "nacionalidad": "guatemalteca",
            "profesion": "Maestra de Educación Primaria",
            "domicilio": "de este domicilio",
            "dpi": "1987 65432 1601",
            "cui_letras": "un mil novecientos ochenta y siete espacio sesenta y cinco mil cuatrocientos treinta y dos espacio un mil seiscientos uno",
            "direccion": "Barrio San Sebastián, zona uno, del municipio de San Pedro Carchá del departamento de Alta Verapaz",
            "tipo_garantia": "PERSONAL",
            "garantia_texto": (
                "los ingresos salariales que percibo mensualmente en el ejercicio de mi profesión docente, "
                "así como con la totalidad de mis bienes presentes y futuros"
            ),
        },
        {
            "nombre": "JOSÉ LUIS HERNÁNDEZ MORÁN",
            "edad_letras": "cuarenta",
            "edad_num": 40,
            "estado_civil": "casado",
            "nacionalidad": "guatemalteco",
            "profesion": "Comerciante",
            "domicilio": "de este domicilio",
            "dpi": "1765 43210 1602",
            "cui_letras": "un mil setecientos sesenta y cinco espacio cuarenta y tres mil doscientos diez espacio un mil seiscientos dos",
            "direccion": "cantón Las Casas, sector Las Flores, municipio de Santa Cruz Verapaz del departamento de Alta Verapaz",
            "tipo_garantia": "MOBILIARIA",
            "garantia_texto": (
                "garantía mobiliaria sobre el inventario y mercaderías de mi establecimiento comercial denominado "
                "Variedades Morán, así como con mis bienes presentes y futuros"
            ),
        },
        {
            "nombre": "GLADYS ESPERANZA SIERRA PACAY",
            "edad_letras": "veintiocho",
            "edad_num": 28,
            "estado_civil": "soltera",
            "nacionalidad": "guatemalteca",
            "profesion": "Licenciada en Administración de Empresas",
            "domicilio": "de este domicilio",
            "dpi": "2890 12345 1601",
            "cui_letras": "dos mil ochocientos noventa espacio doce mil trescientos cuarenta y cinco espacio un mil seiscientos uno",
            "direccion": "séptima avenida tres guion doce, zona cuatro, del municipio de Cobán del departamento de Alta Verapaz",
            "tipo_garantia": "LABORAL",
            "garantia_texto": (
                "el sueldo que devengo como administradora de operaciones, así como con mis bienes muebles presentes y futuros"
            ),
        },
    ]

    cant = max(1, min(cantidad_fiadores, len(fiadores_catalogo)))
    lista_fiadores_elegidos = fiadores_catalogo[:cant]
    rep_edad_num, rep_edad_letras = edad_notarial_desde_fecha(FECHA_NACIMIENTO_EDGAR_ALVARADO)

    return {
        "ciudad": "Cobán",
        "departamento": "Alta Verapaz",
        "fecha_contrato_letras": "dieciséis de octubre del año dos mil veintiséis",
        # Deudor Principal
        "deudor_nombre": "ESTEFANY YUSELA LÓPEZ RUIZ",
        "deudor_edad_letras": "veintinueve",
        "deudor_estado_civil": "casada",
        "deudor_nacionalidad": "guatemalteca",
        "deudor_profesion": "Bachiller en Ciencias y Letras",
        "deudor_domicilio": "de este domicilio",
        "deudor_dpi": "3511 13304 1601",
        "deudor_cui_letras": "tres mil quinientos once espacio trece mil trescientos cuatro espacio un mil seiscientos uno",
        "deudor_direccion": "Lotificación Villas del Carmen, zona tres, de la jurisdicción municipal de Tactic del departamento de Alta Verapaz",
        "deudor_genero": "F",
        # Fiadores Solidarios Dinámicos
        "fiadores": lista_fiadores_elegidos,
        # Claves heredadas para retrocompatibilidad directa
        "fiador_nombre": lista_fiadores_elegidos[0]["nombre"],
        "fiador_edad_letras": lista_fiadores_elegidos[0]["edad_letras"],
        "fiador_estado_civil": lista_fiadores_elegidos[0]["estado_civil"],
        "fiador_nacionalidad": lista_fiadores_elegidos[0]["nacionalidad"],
        "fiador_profesion": lista_fiadores_elegidos[0]["profesion"],
        "fiador_domicilio": lista_fiadores_elegidos[0]["domicilio"],
        "fiador_dpi": lista_fiadores_elegidos[0]["dpi"],
        "fiador_cui_letras": lista_fiadores_elegidos[0]["cui_letras"],
        "fiador_direccion": lista_fiadores_elegidos[0]["direccion"],
        "tipo_garantia": lista_fiadores_elegidos[0]["tipo_garantia"],
        "garantia_texto": lista_fiadores_elegidos[0]["garantia_texto"],
        # Representante Legal El Telar
        "rep_legal_nombre": "EDGAR ARMANDO ALVARADO BERMÚDEZ",
        "rep_legal_edad_letras": rep_edad_letras,
        "rep_legal_edad_num": str(rep_edad_num),
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
        "reg_doc_numero_rm": "quinientos veintisiete mil cuatrocientos noventa y tres (527493)",
        "reg_sociedad_numero": "CIENTO SESENTA Y SEIS MIL CIENTO VEINTE (166120)",
        "reg_sociedad_folio": "OCHOCIENTOS CINCUENTA Y NUEVE (859)",
        "reg_sociedad_libro": "CUATROCIENTOS NOVENTA Y DOS (492), de Sociedades Mercantiles",
        # Condiciones del Crédito
        "monto_capital": 13504.00,
        "monto_capital_letras": "TRECE MIL QUINIENTOS CUATRO QUETZALES",
        "plazo_cuotas_letras": "SEIS",
        "tipo_pago_nombre": "BONOS MENSUALES",
        "desglose_cuotas_texto": (
            "el primer pago será por la cantidad de dos mil seiscientos sesenta y siete (Q. 2,667.00); "
            "el segundo pago será por la cantidad de dos mil quinientos uno (Q. 2,501.00); "
            "el tercer pago será por la cantidad de dos mil trescientos treinta y cuatro (Q. 2.334.00); "
            "el cuarto pago será por la cantidad de dos mil ciento sesenta y siete (Q. 2,167.00); "
            "el quinto pago será por la cantidad de dos mil con un quetzal (Q. 2,001.00); "
            "y, un último pago al vencimiento de la obligación que será por la cantidad de mil ochocientos treinta y cuatro (Q. 1,834.00); "
            "debiendo hacer el primer pago el día nueve de enero del año dos mil veintiséis; "
            "y, los pagos mensuales subsiguientes los días nueve de cada mes calendario; "
            "y, un último abono al vencimiento de la obligación el día nueve de junio del año dos mil veintiséis."
        ),
        "destino_credito": "comercio y capital de trabajo",
        "tasa_interes_letras": "DIEZ POR CIENTO",
        "tasa_interes_num": "10",
        "multa_mora_pct": "10",
        "resolucion_ente": "------",
        "acta_numero": "--- guion de fecha -----",
        # Notario
        "notario_fecha_letras": "dieciséis de octubre del año dos mil veintiséis",
    }


def _construir_texto_garantias_lista(garantias_lista: list | None) -> tuple[str | None, str]:
    """
    Construye (tipo_principal, texto_unido) a partir de una lista de garantías
    usando construir_texto_garantia_item (misma dinámica que contrato_deudor_directo).
    """
    if not isinstance(garantias_lista, list) or not garantias_lista:
        return (None, "")

    textos = []
    tipo_principal = None
    for g in garantias_lista:
        if not isinstance(g, dict):
            continue
        tg = str(g.get("tipo") or g.get("tipo_garantia") or "").strip().upper()
        if tg == "FIADOR":
            continue
        if not tipo_principal and tg:
            tipo_principal = tg
        specs = g.get("especificaciones") if isinstance(g.get("especificaciones"), dict) else {}
        desc = g.get("descripcion") or ""
        txt_g = construir_texto_garantia_item(tg or "MOBILIARIA", specs, desc)
        if txt_g:
            textos.append(txt_g)

    if not textos:
        return (tipo_principal, "")
    return (tipo_principal or "MOBILIARIA", "; y con ".join(textos))


def _preparar_un_fiador(f: dict, default_deudor_nombre: str = "") -> dict:
    """
    Normaliza y enriquece los datos de un fiador individual:
    genera letras de edad, convierte CUI/DPI a letras notariales y construye
    el texto formal de garantía desde sus garantías registradas o, en su defecto,
    usando la modalidad LABORAL de helpers.construir_texto_garantia_item.
    """
    item = dict(f)
    nombre = item.get("nombre") or item.get("fiador_nombre") or "FIADOR SOLIDARIO"
    item["nombre"] = nombre.strip()

    # Edad
    if not item.get("edad_letras"):
        edad_num = item.get("edad_num") or item.get("edad")
        if edad_num:
            item["edad_letras"] = edad_a_letras(edad_num)
        else:
            item["edad_letras"] = "mayor"

    # Generales con valores por defecto
    item["estado_civil"] = item.get("estado_civil") or item.get("fiador_estado_civil") or "soltero"
    item["nacionalidad"] = item.get("nacionalidad") or item.get("fiador_nacionalidad") or "guatemalteco"
    item["profesion"] = item.get("profesion") or item.get("fiador_profesion") or "Bachiller en Ciencias y Letras"
    item["domicilio"] = item.get("domicilio") or item.get("fiador_domicilio") or "de este domicilio"
    item["direccion"] = item.get("direccion") or item.get("fiador_direccion") or "municipio de Cobán del departamento de Alta Verapaz"

    # DPI / CUI en letras y formateado
    dpi_raw = item.get("dpi") or item.get("fiador_dpi") or ""
    if dpi_raw:
        cui_letras, dpi_form = cui_dpi_a_letras(dpi_raw, con_espacio=True)
        if not item.get("cui_letras"):
            item["cui_letras"] = cui_letras
        if not item.get("dpi_formateado"):
            item["dpi_formateado"] = dpi_form
    else:
        item["cui_letras"] = item.get("cui_letras") or ""
        item["dpi_formateado"] = item.get("dpi_formateado") or ""

    # Texto de Garantía
    if not item.get("garantia_texto"):
        tipo_desde_lista, texto_desde_lista = _construir_texto_garantias_lista(item.get("garantias"))
        if texto_desde_lista:
            item["tipo_garantia"] = tipo_desde_lista or "MOBILIARIA"
            item["garantia_texto"] = texto_desde_lista
        else:
            tipo_g = (item.get("tipo_garantia") or "LABORAL").upper()
            if tipo_g == "MOBILIARIA" and item.get("datos_mobiliaria"):
                item["tipo_garantia"] = "MOBILIARIA"
                item["garantia_texto"] = f"garantía mobiliaria sobre {item['datos_mobiliaria']}"
            else:
                lugar = str(item.get("lugar_trabajo") or item.get("Lugar_de_Trabajo") or "").strip()
                item["tipo_garantia"] = "LABORAL"
                item["garantia_texto"] = construir_texto_garantia_item(
                    "LABORAL",
                    {"lugar_trabajo": lugar} if lugar else {},
                )
    else:
        item["tipo_garantia"] = (item.get("tipo_garantia") or "LABORAL").upper()

    return item


def _preparar_datos_con_fiador(datos_entrada: dict | None) -> dict:
    """
    Combina los datos base con los datos proporcionados y procesa la lista dinámica de fiadores.
    Soporta recibir la lista 'fiadores' o campos individuales tradicionales ('fiador_nombre', etc.).
    """
    datos = obtener_datos_ejemplo_con_fiador()
    if datos_entrada:
        datos.update(datos_entrada)

    # Formatos de capital
    cap = datos.get("monto_capital", 13504.00)
    try:
        cap_val = float(cap)
    except (ValueError, TypeError):
        cap_val = 0.0
    datos["monto_capital_formato"] = formato_quetzales(cap_val)
    if "monto_capital_letras" not in datos or not datos["monto_capital_letras"]:
        datos["monto_capital_letras"] = monto_a_letras_quetzales(cap_val).replace(" EXACTOS", "")

    # DPI Deudora
    cui_raw = datos.get("deudor_dpi", "")
    if cui_raw:
        letras_cui, form_cui = cui_dpi_a_letras(cui_raw, con_espacio=True)
        if "deudor_cui_letras" not in datos or not datos["deudor_cui_letras"]:
            datos["deudor_cui_letras"] = letras_cui
        if "deudor_dpi_formateado" not in datos:
            datos["deudor_dpi_formateado"] = form_cui
    else:
        datos["deudor_dpi_formateado"] = ""

    # PROCESAMIENTO DINÁMICO DE FIADORES
    fiadores_finales = []
    deudor_nom = datos.get("deudor_nombre", "")

    if "fiadores" in datos and isinstance(datos["fiadores"], list) and len(datos["fiadores"]) > 0:
        for f in datos["fiadores"]:
            if isinstance(f, dict):
                fiadores_finales.append(_preparar_un_fiador(f, deudor_nom))
    elif datos.get("fiador_nombre"):
        # Retrocompatibilidad: Si pasaron los campos sueltos individuales
        single_f = {
            "nombre": datos.get("fiador_nombre"),
            "edad_letras": datos.get("fiador_edad_letras"),
            "edad_num": datos.get("fiador_edad_num"),
            "estado_civil": datos.get("fiador_estado_civil"),
            "nacionalidad": datos.get("fiador_nacionalidad"),
            "profesion": datos.get("fiador_profesion"),
            "domicilio": datos.get("fiador_domicilio"),
            "dpi": datos.get("fiador_dpi"),
            "cui_letras": datos.get("fiador_cui_letras"),
            "dpi_formateado": datos.get("fiador_dpi_formateado"),
            "direccion": datos.get("fiador_direccion"),
            "tipo_garantia": datos.get("tipo_garantia"),
            "garantia_texto": datos.get("garantia_texto"),
        }
        fiadores_finales.append(_preparar_un_fiador(single_f, deudor_nom))
    else:
        # Fiador por defecto
        fiadores_finales = [_preparar_un_fiador(obtener_datos_ejemplo_con_fiador()["fiadores"][0], deudor_nom)]

    datos["fiadores"] = fiadores_finales

    # Sincronizar campos retrocompatibles con el primer fiador
    if fiadores_finales:
        primer = fiadores_finales[0]
        datos["fiador_nombre"] = primer["nombre"]
        datos["fiador_edad_letras"] = primer["edad_letras"]
        datos["fiador_estado_civil"] = primer["estado_civil"]
        datos["fiador_nacionalidad"] = primer["nacionalidad"]
        datos["fiador_profesion"] = primer["profesion"]
        datos["fiador_domicilio"] = primer["domicilio"]
        datos["fiador_dpi"] = primer["dpi"]
        datos["fiador_cui_letras"] = primer["cui_letras"]
        datos["fiador_dpi_formateado"] = primer.get("dpi_formateado", "")
        datos["fiador_direccion"] = primer["direccion"]
        datos["tipo_garantia"] = primer["tipo_garantia"]
        datos["garantia_texto"] = primer["garantia_texto"]

    return datos


def generar_contrato_con_fiador_word(datos_entrada: dict | None = None, output_target=None):
    """
    Genera el archivo Word (.docx) del Contrato de Reconocimiento de Deuda con Fiadores Solidarios.
    Soporta de manera 100% DINÁMICA cualquier número de fiadores (1, 2, 3, 5, ... N).

    Parámetros:
    -----------
    datos_entrada: dict
        Diccionario con datos del crédito. Puede contener la lista 'fiadores' con N diccionarios
        de fiadores o las claves individuales 'fiador_nombre', etc.
    output_target: io.BytesIO | str | None
        Si se pasa un buffer o string de ruta de archivo, se guarda allí. Si es None, retorna un io.BytesIO.

    Retorno:
    --------
    io.BytesIO | str
    """
    datos = _preparar_datos_con_fiador(datos_entrada)
    fiadores = datos["fiadores"]
    num_fiadores = len(fiadores)

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
    # 1. COMPARECENCIA Y ANTECEDENTES (DINÁMICO: DEUDOR + N FIADORES + REP LEGAL)
    # =========================================================================
    p_intro = doc.add_paragraph()
    p_intro.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_intro.paragraph_format.line_spacing = 1.15
    p_intro.paragraph_format.space_after = Pt(8)

    p_intro.add_run(
        f"En la ciudad de {datos['ciudad']} del departamento de {datos['departamento']}, a {datos['fecha_contrato_letras']}. "
    )
    p_intro.add_run("NOSOTROS: ").bold = False

    # Parte Deudora
    p_intro.add_run("por una parte Yo, ")
    p_intro.add_run(f"{datos['deudor_nombre']}, ").bold = True

    p_intro.add_run(
        f"de {datos['deudor_edad_letras']} años de edad, "
        f"{datos['deudor_estado_civil']}, {datos['deudor_nacionalidad']}, {datos['deudor_profesion']}, {datos['deudor_domicilio']}, "
        "me identifico con el Documento Personal de Identificación –DPI- Código Único de Identificación número "
        f"{datos['deudor_cui_letras']} ({datos['deudor_dpi_formateado'] or datos['deudor_dpi']}); extendido por el "
        "Registro Nacional de las Personas –RENAP-, de la República de Guatemala; "
    )

    # Cada uno de los Fiadores Solidarios (Dinámico)
    for idx, f in enumerate(fiadores, 1):
        prefijo_ordinal = ""
        if num_fiadores > 1:
            ord_txt = ordinal(idx, femenino=False)
            prefijo_ordinal = f"en mi calidad de {ord_txt} FIADOR SOLIDARIO "

        p_intro.add_run(
            f"Yo, {f['nombre']}, ").bold = True

        p_intro.add_run(
            f"{prefijo_ordinal}de {f['edad_letras']} años de edad, {f['estado_civil']}, "
            f"{f['nacionalidad']}, {f['profesion']}, {f['domicilio']}, "
            "me identifico con el Documento Personal de Identificación –DPI- Código Único de Identificación número "
            f"{f['cui_letras']} ({f.get('dpi_formateado') or f['dpi']}); extendido por el "
            "Registro Nacional de las Personas –RENAP-, de la República de Guatemala; "
        )

    # Parte Acreedora (Representante Legal El Telar)
    p_intro.add_run(
        f"y por la otra parte Yo, ")
    
    p_intro.add_run(f"{datos['rep_legal_nombre']}, ").bold = True

    p_intro.add_run(f"de {datos['rep_legal_edad_letras']} ({datos.get('rep_legal_edad_num') or edad_notarial_desde_fecha(FECHA_NACIMIENTO_EDGAR_ALVARADO)[0]}) "
        f"años de edad, {datos['rep_legal_estado_civil']}, {datos['rep_legal_nacionalidad']}, {datos['rep_legal_profesion']}, {datos['rep_legal_domicilio']}, "
        "me identifico con el Documento Personal de Identificación –DPI- Código Único de Identificación número "
        f"{datos['rep_legal_cui_letras']} ({datos['rep_legal_dpi']}) ; extendido por el Registro Nacional de las Personas –RENAP- "
        f"de la República de Guatemala; actúo en mi calidad de ")
    p_intro.add_run(
        f"{datos['rep_legal_cargo']} ").bold = True
    
    p_intro.add_run(f"de la entidad denominada ")
    p_intro.add_run( f"{datos['empresa_nombre']}, ").bold = True

    p_intro.add_run("calidad que acredito con mi nombramiento, el cual está contenido en el acta notarial "
        f"que contiene mi nombramiento, autorizada en la ciudad de Cobán Alta Verapaz, de fecha {datos['reg_acta_nombramiento_fecha']}, "
        f"por el Notario {datos['reg_notario_nombramiento']}, la que se encuentra debidamente inscrita en el Registro Mercantil "
        f"bajo el número ")
    p_intro.add_run(f"{datos['reg_numero_nombramiento']}, folio {datos['reg_folio_nombramiento']}, del libro {datos['reg_libro_nombramiento']}, ").bold = True
    p_intro.add_run(f"según expediente número ")
    p_intro.add_run(f"{datos['reg_expediente_nombramiento']}, ").bold = True
    p_intro.add_run(f"según inscripción de fecha {datos['reg_fecha_inscripcion_nombramiento']}; "
        f"según documento emitido por el Registro Mercantil con número {datos['reg_doc_numero_rm']}; documento en el que hago constar "
        f"que la empresa denominada ")
    p_intro.add_run(f"{datos['empresa_nombre']}, ").bold = True
    p_intro.add_run(f"se encuentra debidamente inscrita en el Registro Mercantil, "
        f"bajo el número ")
    p_intro.add_run(f"{datos['reg_sociedad_numero']}, folio {datos['reg_sociedad_folio']}, del libro {datos['reg_sociedad_libro']}, "
        "manifiesto en la calidad en la que actúo que en el curso del presente documento mi representada será denominada simplemente "
        "como la parte acreedora o la entidad acreedora. ").bold = True
    
    p_intro.add_run(f"Todos aseguramos ser de las generales consignadas, hallarnos en el libre ejercicio "
        "de nuestros derechos civiles y que por el presente acto celebramos "
    )
    p_intro.add_run("CONTRATO DE RECONOCIMIENTO DE DEUDA").bold = True
    p_intro.add_run(", contenido en las cláusulas siguientes:")

    # =========================================================================
    # 2. CLÁUSULA PRIMERA (CONDICIONES DE DEUDA Y GARANTÍAS DE N FIADORES)
    # =========================================================================
    p_primera = doc.add_paragraph()
    p_primera.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_primera.paragraph_format.line_spacing = 1.15
    p_primera.paragraph_format.space_after = Pt(8)

    es_mujer = datos.get("deudor_genero", "F") == "F"
    calidad_deudor = "LISA Y LLANA DEUDORA" if es_mujer else "LISO Y LLANO DEUDOR"
    instruida_txt = "instruida" if es_mujer else "instruido"
    rol_deudor_txt = "DEUDORA" if es_mujer else "DEUDOR"

    p_primera.add_run("PRIMERA: ").bold = True
    p_primera.add_run("Yo, ")
    p_primera.add_run(f"{datos['deudor_nombre']}, ").bold = True
    
    p_primera.add_run(f"declaro que me reconozco {calidad_deudor}, de la entidad acreedora, por la cantidad de ")
    p_primera.add_run(f"{datos['monto_capital_letras']} ({datos['monto_capital_formato']}). ").bold = True
    p_primera.add_run("El reconocimiento se regirá bajo las condiciones siguientes: ")
    p_primera.add_run("a) LA FORMA DE PAGO: ").bold = True

    p_primera.add_run("El pago de la deuda será a través de ")
    p_primera.add_run(f"{datos['plazo_cuotas_letras']} {datos.get('tipo_pago_nombre', 'BONOS MENSUALES')}, ").bold = True
    
    p_primera.add_run(
        f"distribuidos de la siguiente manera: {datos['desglose_cuotas_texto']} "
        f"los pagos deberán efectuarse mediante deposito a la cuenta monetaria número {datos['empresa_cuenta_bancaria']} a nombre de la empresa denominada ")
    p_primera.add_run(
        f"{datos['empresa_nombre']}, ").bold = True
    
    p_primera.add_run(f"empresa ubicada en la {datos['empresa_direccion']}, sin necesidad de requerimiento o cobro alguno; ")

    p_primera.add_run("b) Manifiesto yo, ")
    p_primera.add_run(f"{datos['deudor_nombre']}, ").bold = True

    p_primera.add_run("que la cantidad que me fue otorgada por la ")
    p_primera.add_run("entidad acreedora, ").bold = True

    p_primera.add_run(
        f"la invertiré exclusivamente en: {datos['destino_credito']}, tal y como consta en mi solicitud de crédito; "
        f"c) Comprometiéndome desde ya a pagar una tasa de interés del {datos['tasa_interes_letras']} ({datos['tasa_interes_num']}%), mensual, sin que estos se capitalicen, "
        "pudiendo variar en el transcurso del plazo, si el pago de los intereses y capital no se efectúa en la fecha establecida en este contrato "
        f"de reconocimiento de deuda la entidad acreedora, tendrá derecho de cobrar en concepto de multa la cantidad del {datos['multa_mora_pct']}%, sobre el monto de "
        "intereses vencidos, iniciando el día inmediato posterior a la fecha de pago acordada, la multa por morosidad permanecerá constante "
        f"hasta que el saldo quede al día tal como se me indicó previamente en la empresa ")
    p_primera.add_run(f"{datos['empresa_nombre']}; ").bold = True
    p_primera.add_run("d) Autorizo que este crédito sea cedible o negociable, sin necesidad que la empresa ")
    p_primera.add_run(f"{datos['empresa_nombre']}, ").bold = True
    p_primera.add_run(
        "me de aviso previo o posterior notificación; "
        "e) La falta de pago de la cantidad adeudada, dará derecho a la entidad: "
    )
    p_primera.add_run(f"{datos['empresa_nombre']}, ").bold = True
    p_primera.add_run("por medio de su ")
    p_primera.add_run(f"{datos['rep_legal_cargo']}, representada por el señor {datos['rep_legal_nombre']}, ").bold = True

    p_primera.add_run(
        "a dar por vencido el plazo y al cobro de la cantidad adeudada, intereses y costas procesales "
        "y el presente documento debidamente legalizado por Notario en sus firmas servirá de título ejecutivo para iniciar el juicio correspondiente "
        "y en esta forma se podrá dar por vencido el plazo si se da el dinero mutuado un destino diferente para el que fue concedido según la solicitud "
        f"de crédito y la resolución emitida por {datos['resolucion_ente']} de la empresa ")
    p_primera.add_run(f"{datos['empresa_nombre']}, ").bold = True

    p_primera.add_run(
        f"contenida en Acta número {datos['acta_numero']} mediante la cual fue autorizado el presente Crédito; "
    ).bold = True
    
    p_primera.add_run("f) Para los efectos legales, yo, ")
    p_primera.add_run(f"{datos['deudor_nombre']}, ").bold = True
    p_primera.add_run(
        "renuncio al fuero de mi domicilio y me sujeto expresamente a los tribunales que la entidad acreedora elija, "
        "señalando desde ya como lugar para recibir citaciones, notificaciones y emplazamientos en la siguiente dirección: ")
    p_primera.add_run(f"{datos['deudor_direccion']}, ").bold = True

    p_primera.add_run(
        "casa plenamente conocida, lugar donde resido actualmente; y acepto como buenas, exactas, de plazo vencido, líquidas y exigibles las cantidades "
        "que a consecuencia de este crédito se me presenten en caso de incumplimiento a cualquiera de las estipulaciones de este contrato, y si cambiará de dirección "
        "tengo la obligación de comunicarlo a la entidad acreedora, caso contrario las citaciones, notificaciones y emplazamientos se me harán en la dirección antes indicada y se tendrán como válidas; "
    )

    # Cláusula de Garantía(s) Dinámica (Deudor si registró garantías propias + Fiador(es))
    deudor_garantias_texto = str(datos.get("deudor_garantias_texto") or "").strip()

    if not deudor_garantias_texto and num_fiadores == 1:
        f = fiadores[0]
        p_primera.add_run("g) DE LA GARANTÍA: ").bold = True
        p_primera.add_run("Yo, ")
        p_primera.add_run(f"{f['nombre']}, ").bold = True

        p_primera.add_run("manifiesto que para el fiel cumplimiento de la obligación que contrae la parte deudora, por este acto me constituyo en ")
        p_primera.add_run(
            f"FIADOR, SOLIDARIO y MANCOMUNADO de {datos['deudor_nombre']}, ").bold = True
        
        p_primera.add_run(f"garantizando la deuda, intereses, multa por morosidad y costas procesales con {f['garantia_texto']}. ")
        p_primera.add_run("Yo: ")
        p_primera.add_run(f"{f['nombre']}, ").bold = True
        p_primera.add_run(
            "renuncio al fuero de mi domicilio y me someto expresamente a los tribunales que la Entidad Acreedora elija, "
            "señalando desde ya como lugar para recibir citaciones, notificaciones y emplazamientos, en la siguiente dirección: ")
        p_primera.add_run(f"{f['direccion']}.").bold = True

    else:
        p_primera.add_run(
            "g) DE LAS GARANTÍAS Y FIADORES SOLIDARIOS Y MANCOMUNADOS: ").bold = True
        p_primera.add_run(
            "Para el fiel y estricto cumplimiento de todas y cada una de las obligaciones derivadas del presente contrato, "
            "se constituyen las siguientes garantías:\n"
        )

        sub_idx = 0
        if deudor_garantias_texto:
            sub_idx += 1
            p_primera.add_run(f"g.{sub_idx}) DE LA GARANTÍA DE LA PARTE DEUDORA: Yo, ")
            p_primera.add_run(f"{datos['deudor_nombre']}, ").bold = True
            p_primera.add_run(
                f"garantizo la deuda, intereses, multa por morosidad y costas procesales con {deudor_garantias_texto}.\n"
            )

        for idx, f in enumerate(fiadores, 1):
            sub_idx += 1
            ord_fem = ordinal(idx, femenino=True)
            etiqueta_fiaduria = (
                "DE LA FIADURÍA SOLIDARIA" if num_fiadores == 1
                else f"DE LA {ord_fem} FIADURÍA SOLIDARIA"
            )
            p_primera.add_run(f"g.{sub_idx}) {etiqueta_fiaduria}: Yo, ")
            p_primera.add_run(f"{f['nombre']}, ").bold = True
            p_primera.add_run(
                "manifiesto que para el fiel cumplimiento de la obligación que contrae la parte deudora, por este acto me constituyo en "
                "FIADOR, SOLIDARIO y MANCOMUNADO de ")
            p_primera.add_run(f"{datos['deudor_nombre']}, ").bold = True

            p_primera.add_run(
                f"garantizando la deuda, intereses, multa por morosidad y costas procesales con {f['garantia_texto']}. "
                "Yo, ")
            p_primera.add_run(f"{f['nombre']}, ").bold = True

            p_primera.add_run(
                "renuncio al fuero de mi domicilio y me someto expresamente a los tribunales que la Entidad Acreedora elija, "
                "señalando desde ya como lugar para recibir citaciones, notificaciones y emplazamientos en la siguiente dirección: ")
            p_primera.add_run(f"{f['direccion']}.").bold = True
            if idx < num_fiadores:
                p_primera.add_run("\n")

    # =========================================================================
    # 3. CLÁUSULA SEGUNDA (DECLARACIÓN DE INSTRUCCIÓN PREVIA)
    # =========================================================================
    p_segunda = doc.add_paragraph()
    p_segunda.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_segunda.paragraph_format.line_spacing = 1.15
    p_segunda.paragraph_format.space_after = Pt(8)
    p_segunda.add_run("SEGUNDA: ").bold = True
    p_segunda.add_run(
        "Yo, ") 
    p_segunda.add_run(f"{datos['deudor_nombre']}, ").bold = True

    p_segunda.add_run(
        f"manifiesto que en su momento fui plenamente {instruida_txt} de las condiciones en las cuales se me otorgó el crédito anteriormente descrito, "
        "para el otorgamiento del presente crédito por parte de la empresa ") 
    p_segunda.add_run(f"{datos['empresa_nombre']}."
    ).bold = True

    # =========================================================================
    # 4. CLÁUSULA TERCERA (ACEPTACIÓN REPRESENTANTE LEGAL)
    # =========================================================================
    p_tercera = doc.add_paragraph()
    p_tercera.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_tercera.paragraph_format.line_spacing = 1.15
    p_tercera.paragraph_format.space_after = Pt(8)
    p_tercera.add_run("TERCERA: ").bold = True
    p_tercera.add_run("Por mi parte Yo, ")
    p_tercera.add_run(
        f"{datos['rep_legal_nombre']}, en mi calidad de {datos['rep_legal_cargo']} de la entidad denominada "
        f"{datos['empresa_nombre']}, "
    ).bold = True
    
    p_tercera.add_run(
        "expreso que en los términos relacionados ACEPTO EXPRESAMENTE, para mi representada el contenido íntegro del presente contrato."
    )

    # =========================================================================
    # 5. CLÁUSULA CUARTA (RATIFICACIÓN DE TODAS LAS PARTES)
    # =========================================================================
    p_cuarta = doc.add_paragraph()
    p_cuarta.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_cuarta.paragraph_format.line_spacing = 1.15
    p_cuarta.paragraph_format.space_after = Pt(14)
    p_cuarta.add_run("CUARTA: ").bold = True
    p_cuarta.add_run(
        "Todos los que intervenimos en este contrato, en las calidades en que actuamos declaramos que ACEPTAMOS EXPRESAMENTE, "
        "el contenido íntegro del presente. Leemos lo escrito y bien impuestos de su contenido, objeto, valor y demás efectos legales, "
        "lo aceptamos, ratificamos y firmamos."
    )

    # =========================================================================
    # 6. TABLA DE FIRMAS DINÁMICA (DEUDOR + N FIADORES + REP LEGAL)
    # =========================================================================
    firmantes = []
    firmantes.append({
        "rol": rol_deudor_txt,
        "nombre": datos["deudor_nombre"],
    })

    for idx, f in enumerate(fiadores, 1):
        rol_fiador = "FIADOR SOLIDARIO" if num_fiadores == 1 else f"FIADOR SOLIDARIO {idx}"
        firmantes.append({
            "rol": rol_fiador,
            "nombre": f["nombre"],
        })

    firmantes.append({
        "rol": f"REPRESENTANTE LEGAL\n{datos['empresa_nombre']}",
        "nombre": datos["rep_legal_nombre"],
    })

    num_filas = (len(firmantes) + 1) // 2
    tabla_firmas = doc.add_table(rows=num_filas, cols=2)
    tabla_firmas.alignment = WD_TABLE_ALIGNMENT.CENTER
    tabla_firmas.autofit = False
    tabla_firmas.columns[0].width = Inches(3.2)
    tabla_firmas.columns[1].width = Inches(3.2)

    for i, s in enumerate(firmantes):
        r_idx = i // 2
        c_idx = i % 2
        celda = tabla_firmas.cell(r_idx, c_idx).paragraphs[0]
        celda.paragraph_format.space_after = Pt(14)
        celda.add_run("f.____________________________\n").bold = True
        celda.add_run(f"{s['rol']}\n{s['nombre']}")

    # =========================================================================
    # 7. ACTA NOTARIAL DE LEGALIZACIÓN DE FIRMAS (DINÁMICA PARA N COMPARECIENTES)
    # =========================================================================
    p_notario = doc.add_paragraph()
    p_notario.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_notario.paragraph_format.line_spacing = 1.15
    p_notario.paragraph_format.space_before = Pt(16)
    p_notario.paragraph_format.space_after = Pt(14)

    p_notario.add_run(
        f"En la ciudad de {datos['ciudad']} del departamento de {datos['departamento']}, a {datos['notario_fecha_letras']}. "
        "Como Notario en ejercicio "
    )
    p_notario.add_run("DOY FE: ").bold = True
    p_notario.add_run("Que las firmas que anteceden son ")
    p_notario.add_run("AUTENTICAS").bold = True
    p_notario.add_run(
        ", por haber sido puestas en el CONTRATO DE RECONOCIMIENTO DE DEUDA, el día de hoy a mi presencia por los señores: "
    )

    partes_acta = []
    partes_acta.append(
        f"{datos['deudor_nombre']} ({rol_deudor_txt}), quien se identifica con el Documento Personal de Identificación –DPI– "
        f"Código Único de Identificación número {datos['deudor_cui_letras']}, extendido por el Registro Nacional de las Personas –RENAP–, "
        "de la República de Guatemala"
    )

    for idx, f in enumerate(fiadores, 1):
        etiqueta_acta = "FIADOR" if num_fiadores == 1 else f"FIADOR SOLIDARIO {idx}"
        partes_acta.append(
            f"{f['nombre']} ({etiqueta_acta}), quien se identifica con el Documento Personal de Identificación –DPI– "
            f"Código Único de Identificación número {f['cui_letras']}, extendido por el Registro Nacional de las Personas –RENAP–, "
            "de la República de Guatemala"
        )

    partes_acta.append(
        f"y, {datos['rep_legal_nombre']}, en la calidad en que actúa como {datos['rep_legal_cargo']} de la entidad denominada "
        f"{datos['empresa_nombre']}, quien se identifica con el Documento Personal de Identificación –DPI– Código Único de Identificación "
        f"número {datos['rep_legal_cui_letras']}, extendidos por el Registro Nacional de las Personas –RENAP–, de la República de Guatemala"
    )

    p_notario.add_run("; ".join(partes_acta))
    p_notario.add_run(", quienes vuelven a firmar junto conmigo la presente acta de legalización de firmas.")

    # Firmas del Acta Notarial (Misma estructura de 2 columnas)
    tabla_not = doc.add_table(rows=num_filas, cols=2)
    tabla_not.alignment = WD_TABLE_ALIGNMENT.CENTER
    tabla_not.autofit = False
    tabla_not.columns[0].width = Inches(3.2)
    tabla_not.columns[1].width = Inches(3.2)

    for i, s in enumerate(firmantes):
        r_idx = i // 2
        c_idx = i % 2
        celda_not = tabla_not.cell(r_idx, c_idx).paragraphs[0]
        celda_not.paragraph_format.space_after = Pt(14)
        celda_not.add_run("f.____________________________\n").bold = True
        celda_not.add_run(f"{s['rol']}\n{s['nombre']}")

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


def _construir_fiador_notarial_desde_customer(
    cust_obj,
    specs_extra: dict | None = None,
    asset_guarantees: list | None = None,
    fiador_garantias: list | None = None,
) -> dict:
    """
    Construye el diccionario exacto de un fiador a partir de una instancia de Customer,
    priorizando sus garantías propias (fiador["garantias"]) mediante construir_texto_garantia_item;
    si el fiador no registra garantías propias, aplica la modalidad LABORAL de helpers.
    """
    persona = extraer_persona_notarial(cust_obj, default_genero="M")
    specs_extra = specs_extra if isinstance(specs_extra, dict) else {}
    fiador_garantias = fiador_garantias if isinstance(fiador_garantias, list) else []

    tipo_garantia = None
    garantia_texto = specs_extra.get("garantia_texto") or ""
    lugar_trabajo = str(specs_extra.get("Lugar_de_Trabajo") or specs_extra.get("lugar_trabajo") or "").strip()
    if lugar_trabajo.upper() in ("N/A", "---", "NONE"):
        lugar_trabajo = ""

    # Buscar WorkingInformation real o mock
    wi = getattr(cust_obj, "_mock_working_info", None)
    if wi is None:
        try:
            from apps.FinancialInformation.models import WorkingInformation
            wi = WorkingInformation.objects.filter(customer_id=cust_obj).first()
        except Exception:
            wi = None

    empresa_lab = ""
    if wi is not None:
        empresa_lab = str(getattr(wi, "company_name", "") or "").strip()
        if empresa_lab and empresa_lab.upper() not in ("N/A", "---") and not lugar_trabajo:
            lugar_trabajo = empresa_lab

    # 1. Prioridad: garantías registradas directamente en el fiador (fiador = [{"id": ..., "garantias": [...]}])
    if not garantia_texto and fiador_garantias:
        tipo_desde_f, texto_desde_f = _construir_texto_garantias_lista(fiador_garantias)
        if texto_desde_f:
            tipo_garantia = tipo_desde_f
            garantia_texto = texto_desde_f

    # 2. Respaldo retrocompatible: garantía de activo cuyo Titular coincida explícitamente con este fiador
    if not garantia_texto and asset_guarantees:
        nom_norm = persona["nombre"].strip().upper()
        for ag in asset_guarantees:
            ag_specs = ag.get("especificaciones") if isinstance(ag, dict) else {}
            if not isinstance(ag_specs, dict):
                ag_specs = {}
            titular = str(
                ag_specs.get("Titular")
                or ag_specs.get("titular")
                or ag.get("propietario")
                or ""
            ).strip().upper()
            if titular and (titular == nom_norm or nom_norm in titular or titular in nom_norm):
                tg_ag = str(ag.get("tipo") or ag.get("tipo_garantia") or "MOBILIARIA").strip().upper()
                tipo_garantia = tg_ag
                garantia_texto = construir_texto_garantia_item(tg_ag, ag_specs, ag.get("descripcion") or "")
                break

    # 3. Si el fiador no registró garantías propias, se utiliza el formato LABORAL de helpers.construir_texto_garantia_item
    if not garantia_texto:
        tipo_garantia = "LABORAL"
        specs_laboral = {"lugar_trabajo": lugar_trabajo} if lugar_trabajo else {}
        garantia_texto = construir_texto_garantia_item("LABORAL", specs_laboral)

    item = {
        "nombre": persona["nombre"],
        "edad_letras": persona["edad_letras"],
        "edad_num": persona["edad_num"],
        "estado_civil": persona["estado_civil"],
        "nacionalidad": persona["nacionalidad"],
        "profesion": persona["profesion"],
        "domicilio": persona["domicilio"],
        "dpi": persona["dpi"],
        "cui_letras": persona["cui_letras"],
        "direccion": persona["direccion"],
        "tipo_garantia": tipo_garantia or "LABORAL",
        "garantia_texto": garantia_texto,
        "garantias": fiador_garantias,
    }
    if lugar_trabajo:
        item["lugar_trabajo"] = lugar_trabajo
    return item


def extraer_datos_contrato_con_fiador_desde_solicitud(solicitud, overrides: dict | None = None) -> dict:
    """
    Extrae toda la información real desde una Solicitud (InvestmentPlan) o Crédito (Credit),
    siguiendo exactamente la estructura de obtener_datos_ejemplo_con_fiador() con soporte
    dinámico para 1, 2, 3, 5 o N fiadores solidarios.
    """
    datos = extraer_datos_base_contrato_desde_solicitud(solicitud)

    garantias_raw = getattr(solicitud, "garantias", None)
    if not garantias_raw and getattr(solicitud, "destino_id", None) is not None:
        garantias_raw = getattr(solicitud.destino_id, "garantias", None)
    if not isinstance(garantias_raw, list):
        garantias_raw = []

    garantias_activos = [
        g for g in garantias_raw
        if isinstance(g, dict) and str(g.get("tipo") or g.get("tipo_garantia") or "").upper() != "FIADOR"
    ]
    garantias_fiadores = [
        g for g in garantias_raw
        if isinstance(g, dict) and str(g.get("tipo") or g.get("tipo_garantia") or "").upper() == "FIADOR"
    ]

    # Mapa auxiliar de specs en garantias FIADOR por codigo o nombre
    specs_por_codigo = {}
    specs_por_nombre = {}
    for g in garantias_fiadores:
        sp = g.get("especificaciones") if isinstance(g.get("especificaciones"), dict) else {}
        cod = str(sp.get("Codigo_de_Cliente") or "").strip()
        nom = str(sp.get("Nombre") or sp.get("nombre") or "").strip().upper()
        if cod:
            specs_por_codigo[cod] = sp
        if nom:
            specs_por_nombre[nom] = sp

    fiadores_lista = []
    vistos_ids = set()
    vistos_nombres = set()

    def _registrar_fiador(item_dict: dict, cust_id=None):
        nom_key = item_dict["nombre"].strip().upper()
        if cust_id is not None:
            if cust_id in vistos_ids:
                return
            vistos_ids.add(cust_id)
        if nom_key and nom_key in vistos_nombres:
            return
        if nom_key:
            vistos_nombres.add(nom_key)
        fiadores_lista.append(item_dict)

    # 1. Extraer de solicitud.fiador (soporta list de {id}, list de objetos Customer, dict único o int)
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
        dict_specs = {}
        f_garantias = []
        f_id = None

        if isinstance(f_entry, dict):
            f_id = f_entry.get("id") or f_entry.get("customer_id")
            if isinstance(f_entry.get("garantias"), list):
                f_garantias = f_entry.get("garantias") or []
            if f_entry.get("first_name") or f_entry.get("identification_number"):
                # Diccionario con datos directos de fiador (sin requerir consulta ORM)
                dict_specs = f_entry
            elif f_entry.get("nombre"):
                dict_specs = f_entry
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
            # Objeto Customer (real o mock) pasado directamente
            cust_obj = f_entry
            f_id = getattr(f_entry, "id", None)

        if cust_obj is not None:
            cod_c = str(getattr(cust_obj, "customer_code", "") or "").strip()
            nom_c = (
                cust_obj.get_full_name() if callable(getattr(cust_obj, "get_full_name", None))
                else f"{getattr(cust_obj, 'first_name', '')} {getattr(cust_obj, 'last_name', '')}"
            ).strip().upper()
            sp_extra = specs_por_codigo.get(cod_c) or specs_por_nombre.get(nom_c) or dict_specs
            fiador_item = _construir_fiador_notarial_desde_customer(
                cust_obj,
                specs_extra=sp_extra,
                asset_guarantees=garantias_activos,
                fiador_garantias=f_garantias,
            )
            _registrar_fiador(fiador_item, cust_id=f_id)
        elif dict_specs and (dict_specs.get("nombre") or dict_specs.get("first_name")):
            nom_d = dict_specs.get("nombre") or f"{dict_specs.get('first_name', '')} {dict_specs.get('last_name', '')}".strip()
            dpi_d = dict_specs.get("dpi") or dict_specs.get("identification_number") or ""
            cui_l, dpi_f = cui_dpi_a_letras(dpi_d, con_espacio=True) if dpi_d else ("", "")
            edad_n = dict_specs.get("edad_num") or dict_specs.get("edad") or ""
            tipo_d, gar_txt_d = _construir_texto_garantias_lista(f_garantias)
            if not gar_txt_d:
                gar_txt_d = dict_specs.get("garantia_texto") or ""
            if not gar_txt_d:
                lugar_d = str(dict_specs.get("lugar_trabajo") or dict_specs.get("Lugar_de_Trabajo") or "").strip()
                tipo_d = "LABORAL"
                gar_txt_d = construir_texto_garantia_item("LABORAL", {"lugar_trabajo": lugar_d} if lugar_d else {})
            fiador_item = {
                "nombre": str(nom_d).strip().upper(),
                "edad_letras": dict_specs.get("edad_letras") or (edad_a_letras(edad_n) if edad_n else "mayor"),
                "edad_num": edad_n,
                "estado_civil": dict_specs.get("estado_civil") or "soltero",
                "nacionalidad": dict_specs.get("nacionalidad") or "guatemalteco",
                "profesion": dict_specs.get("profesion") or "Comerciante",
                "domicilio": dict_specs.get("domicilio") or "de este domicilio",
                "dpi": dpi_f or dpi_d,
                "cui_letras": dict_specs.get("cui_letras") or cui_l,
                "direccion": dict_specs.get("direccion") or "Cobán, Alta Verapaz",
                "tipo_garantia": tipo_d or dict_specs.get("tipo_garantia") or "LABORAL",
                "garantia_texto": gar_txt_d,
                "garantias": f_garantias,
            }
            _registrar_fiador(fiador_item, cust_id=f_id)

    # 2. Complementar con garantias de tipo FIADOR en solicitud.garantias
    for g in garantias_fiadores:
        specs = g.get("especificaciones") if isinstance(g.get("especificaciones"), dict) else {}
        cod = str(specs.get("Codigo_de_Cliente") or "").strip()
        nom = str(specs.get("Nombre") or specs.get("nombre") or "").strip()
        cust_obj = None

        if cod:
            try:
                from apps.customers.models import Customer
                cust_obj = Customer.objects.filter(customer_code=cod).first()
            except Exception:
                cust_obj = None

        if cust_obj is not None:
            fiador_item = _construir_fiador_notarial_desde_customer(cust_obj, specs_extra=specs, asset_guarantees=garantias_activos)
            _registrar_fiador(fiador_item, cust_id=getattr(cust_obj, "id", None))
        elif nom:
            dpi_raw = str(specs.get("DPI") or specs.get("dpi") or "").strip()
            cui_l, dpi_f = cui_dpi_a_letras(dpi_raw, con_espacio=True) if dpi_raw else ("", "")
            edad_n = specs.get("edad_num") or specs.get("edad") or ""
            lugar_t = str(specs.get("Lugar_de_Trabajo") or specs.get("lugar_trabajo") or "").strip()
            if lugar_t.upper() in ("N/A", "---"):
                lugar_t = ""
            gar_txt = specs.get("garantia_texto") or ""
            if not gar_txt:
                tipo_g = "LABORAL"
                gar_txt = construir_texto_garantia_item(
                    "LABORAL",
                    {"lugar_trabajo": lugar_t} if lugar_t else {},
                )
            else:
                tipo_g = str(specs.get("tipo_garantia") or "LABORAL").upper()

            fiador_item = {
                "nombre": nom.upper(),
                "edad_letras": specs.get("edad_letras") or (edad_a_letras(edad_n) if edad_n else "mayor"),
                "edad_num": edad_n,
                "estado_civil": specs.get("estado_civil") or "soltero",
                "nacionalidad": specs.get("nacionalidad") or "guatemalteco",
                "profesion": specs.get("profesion") or "Comerciante",
                "domicilio": specs.get("domicilio") or "de este domicilio",
                "dpi": dpi_f or dpi_raw,
                "cui_letras": cui_l,
                "direccion": specs.get("Domicilio") or specs.get("direccion") or "Cobán, Alta Verapaz",
                "tipo_garantia": tipo_g,
                "garantia_texto": gar_txt,
            }
            if lugar_t:
                fiador_item["lugar_trabajo"] = lugar_t
            _registrar_fiador(fiador_item)

    # 3. Si es instancia real de Credit, complementar desde DetailsGuarantees
    if not hasattr(solicitud, "total_value_of_the_product_or_service") and getattr(solicitud, "id", None):
        try:
            from apps.financings.models import DetailsGuarantees
            from apps.customers.models import Customer
            det_fiadores = DetailsGuarantees.objects.filter(
                garantia_id__credit_id=solicitud,
                tipo_garantia="FIADOR",
            ).order_by("pk")
            for det in det_fiadores:
                sp = det.especificaciones if isinstance(det.especificaciones, dict) else {}
                cod = str(sp.get("Codigo_de_Cliente") or "").strip()
                cust_obj = Customer.objects.filter(customer_code=cod).first() if cod else None
                if cust_obj is not None:
                    f_item = _construir_fiador_notarial_desde_customer(cust_obj, specs_extra=sp, asset_guarantees=garantias_activos)
                    _registrar_fiador(f_item, cust_id=cust_obj.id)
                elif sp.get("Nombre"):
                    dpi_r = str(sp.get("DPI") or sp.get("dpi") or "").strip()
                    cui_l, dpi_f = cui_dpi_a_letras(dpi_r, con_espacio=True) if dpi_r else ("", "")
                    lugar_t = str(sp.get("Lugar_de_Trabajo") or "").strip()
                    if lugar_t.upper() in ("N/A", "---", "NONE"):
                        lugar_t = ""
                    f_item = {
                        "nombre": str(sp.get("Nombre")).strip().upper(),
                        "edad_letras": "mayor",
                        "edad_num": "",
                        "estado_civil": "soltero",
                        "nacionalidad": "guatemalteco",
                        "profesion": "Comerciante",
                        "domicilio": "de este domicilio",
                        "dpi": dpi_f or dpi_r,
                        "cui_letras": cui_l,
                        "direccion": sp.get("Domicilio") or "Cobán, Alta Verapaz",
                        "tipo_garantia": "LABORAL",
                        "garantia_texto": construir_texto_garantia_item(
                            "LABORAL",
                            {"lugar_trabajo": lugar_t} if lugar_t else {},
                        ),
                    }
                    if lugar_t:
                        f_item["lugar_trabajo"] = lugar_t
                    _registrar_fiador(f_item)
        except Exception:
            pass

    # 4. Placeholder seguro si aún no se han registrado fiadores en la solicitud
    if not fiadores_lista:
        fiadores_lista.append({
            "nombre": "FIADOR SOLIDARIO PENDIENTE",
            "edad_letras": "____",
            "edad_num": "",
            "estado_civil": "____",
            "nacionalidad": "guatemalteco",
            "profesion": "____",
            "domicilio": "de este domicilio",
            "dpi": "________________",
            "cui_letras": "________________",
            "direccion": "________________",
            "tipo_garantia": "PERSONAL",
            "garantia_texto": "el salario y la totalidad de mis bienes presentes y futuros",
        })

    # Garantías propias de la parte deudora (solicitud.garantias excluyendo FIADOR y las asignadas por Titular a un fiador)
    nombres_fiadores_norm = {f["nombre"].strip().upper() for f in fiadores_lista if f.get("nombre")}
    garantias_deudor_filtradas = []
    for ag in garantias_activos:
        ag_specs = ag.get("especificaciones") if isinstance(ag.get("especificaciones"), dict) else {}
        titular = str(
            ag_specs.get("Titular")
            or ag_specs.get("titular")
            or ag.get("propietario")
            or ""
        ).strip().upper()
        pertenece_a_fiador = bool(
            titular and any(titular == fn or fn in titular or titular in fn for fn in nombres_fiadores_norm)
        )
        if not pertenece_a_fiador:
            garantias_deudor_filtradas.append(ag)

    _, deudor_garantias_texto = _construir_texto_garantias_lista(garantias_deudor_filtradas)
    if deudor_garantias_texto:
        datos["deudor_garantias_texto"] = deudor_garantias_texto

    datos["fiadores"] = fiadores_lista
    primer = fiadores_lista[0]
    datos["fiador_nombre"] = primer["nombre"]
    datos["fiador_edad_letras"] = primer["edad_letras"]
    datos["fiador_estado_civil"] = primer["estado_civil"]
    datos["fiador_nacionalidad"] = primer["nacionalidad"]
    datos["fiador_profesion"] = primer["profesion"]
    datos["fiador_domicilio"] = primer["domicilio"]
    datos["fiador_dpi"] = primer["dpi"]
    datos["fiador_cui_letras"] = primer["cui_letras"]
    datos["fiador_direccion"] = primer["direccion"]
    datos["tipo_garantia"] = primer["tipo_garantia"]
    datos["garantia_texto"] = primer["garantia_texto"]

    if overrides and isinstance(overrides, dict):
        if "monto_capital" in overrides and "monto_capital_letras" not in overrides:
            try:
                datos["monto_capital_letras"] = monto_a_letras_quetzales(float(overrides["monto_capital"])).replace(" EXACTOS", "")
            except Exception:
                pass
        if "deudor_dpi" in overrides and "deudor_cui_letras" not in overrides:
            cui_l, dpi_f = cui_dpi_a_letras(overrides["deudor_dpi"], con_espacio=True)
            datos["deudor_cui_letras"] = cui_l
            datos["deudor_dpi_formateado"] = dpi_f
        datos.update(overrides)

    return datos


def generar_contrato_con_fiador_desde_solicitud(solicitud_o_id, overrides: dict | None = None, output_target=None):
    """
    Genera el Contrato de Reconocimiento de Deuda con Fiador(es) Solidario(s) en Word (.docx)
    extrayendo los datos reales y la lista dinámica de fiadores desde una Solicitud (InvestmentPlan)
    o Crédito (Credit).
    """
    solicitud = resolver_solicitud_o_credito(solicitud_o_id)
    datos = extraer_datos_contrato_con_fiador_desde_solicitud(solicitud, overrides=overrides)
    return generar_contrato_con_fiador_word(datos, output_target=output_target)


generar_contrato_con_fiador_desde_credito = generar_contrato_con_fiador_desde_solicitud
