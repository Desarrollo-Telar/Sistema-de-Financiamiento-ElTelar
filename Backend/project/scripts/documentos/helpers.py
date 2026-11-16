
"""
Módulo de utilidades y formateadores para la generación de documentos legales
(Guatemala - El Telar S.A.).
Incluye conversiones de montos a letras en Quetzales, CUI/DPI a letras,
NIT a letras, cuentas bancarias, tasas de interés, plazos y fechas notariales.
"""

import calendar
import math
from decimal import Decimal
from datetime import date, datetime
from num2words import num2words

# Mapeo de dígitos a palabras en español
DIGITOS_LETRAS = {
    '0': 'cero',
    '1': 'uno',
    '2': 'dos',
    '3': 'tres',
    '4': 'cuatro',
    '5': 'cinco',
    '6': 'seis',
    '7': 'siete',
    '8': 'ocho',
    '9': 'nueve',
}

MESES = [
    '', 'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
    'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'
]


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


def numero_a_letras(numero: int, mayusculas: bool = False) -> str:
    """Convierte un número entero a letras en español."""
    try:
        texto = num2words(int(numero), lang='es')
        return texto.upper() if mayusculas else texto
    except Exception:
        return str(numero)


def formato_quetzales(monto) -> str:
    """Formatea un número decimal/float a formato monetario guatemalteco: Q.360,000.00"""
    try:
        val = float(monto)
        return f"Q.{val:,.2f}"
    except (ValueError, TypeError):
        return f"Q.{monto}"


def monto_a_letras_quetzales(monto, incluir_simbolo: bool = False) -> str:
    """
    Convierte un monto en Quetzales a texto en mayúsculas.
    Ejemplo: 360000.00 -> 'TRESCIENTOS SESENTA MIL QUETZALES EXACTOS'
             360000.50 -> 'TRESCIENTOS SESENTA MIL QUETZALES CON CINCUENTA CENTAVOS'
    """
    try:
        val = round(float(monto), 2)
        enteros = int(val)
        centavos = int(round((val - enteros) * 100))

        enteros_letras = num2words(enteros, lang='es').upper()
        # Ajuste común en num2words para 'uno' en lugar de 'un' cuando es exacto
        if enteros == 1:
            texto_moneda = "QUETZAL"
        else:
            texto_moneda = "QUETZALES"

        if centavos == 0:
            resultado = f"{enteros_letras} {texto_moneda} EXACTOS"
        else:
            centavos_letras = num2words(centavos, lang='es').upper()
            resultado = f"{enteros_letras} {texto_moneda} CON {centavos_letras} CENTAVOS"

        if incluir_simbolo:
            resultado += f" ({formato_quetzales(val)})"

        return resultado
    except Exception:
        return f"{monto} QUETZALES"


def cui_dpi_a_letras(cui_raw: str, con_espacio: bool = False) -> tuple[str, str]:
    """
    Formatea un CUI/DPI guatemalteco (13 dígitos) y lo convierte a palabras según
    el estándar notarial (4 - 5 - 4 dígitos).
    Si con_espacio=True, une con ' espacio ' en minúsculas:
    'dos mil ciento cincuenta y nueve espacio ochenta y tres mil ochocientos sesenta y seis espacio un mil ochocientos tres'
    Si con_espacio=False, une con coma:
    'Dos mil quinientos veintiséis, Veintidós mil noventa y siete, Mil seiscientos uno'
    """
    if not cui_raw:
        return ("", "")

    limpio = ''.join(c for c in str(cui_raw) if c.isdigit())

    if len(limpio) == 13:
        p1 = limpio[0:4]
        p2 = limpio[4:9]
        p3 = limpio[9:13]
        formateado = f"{p1} {p2} {p3}"

        try:
            if con_espacio:
                w1 = num2words(int(p1), lang='es').lower()
                w2 = num2words(int(p2), lang='es').lower()
                w3 = num2words(int(p3), lang='es').lower()
                if w1 == "mil":
                    w1 = "un mil"
                if w3 == "mil":
                    w3 = "un mil"
                elif w3.startswith("mil "):
                    w3 = "un " + w3
                texto = f"{w1} espacio {w2} espacio {w3}"
            else:
                w1 = num2words(int(p1), lang='es').capitalize()
                w2 = num2words(int(p2), lang='es').capitalize()
                w3 = num2words(int(p3), lang='es').capitalize()
                texto = f"{w1}, {w2}, {w3}"
            return (texto, formateado)
        except Exception:
            return (formateado, formateado)
    else:
        return (str(cui_raw), str(cui_raw))


def edad_a_letras(edad) -> str:
    """Convierte edad a palabras en minúsculas (ej. 33 -> 'treinta y tres', 41 -> 'cuarenta y un')."""
    try:
        n = int(edad)
        texto = num2words(n, lang='es').lower()
        if n > 1 and texto.endswith("veintiuno"):
            texto = texto[:-len("veintiuno")] + "veintiún"
        elif n > 1 and texto.endswith(" uno"):
            texto = texto[:-len("uno")] + "un"
        return texto
    except Exception:
        return str(edad)


def ordinal_masculino(n: int) -> str:
    """Convierte número a ordinal masculino (1 -> 'primer', 2 -> 'segundo', etc.)."""
    ordinales = {
        1: "primer",
        2: "segundo",
        3: "tercer",
        4: "cuarto",
        5: "quinto",
        6: "sexto",
        7: "séptimo",
        8: "octavo",
        9: "noveno",
        10: "décimo",
        11: "pago décimo primero",
        12: "décimo segundo",
    }
    if n in ordinales:
        return ordinales[n]
    try:
        return num2words(n, lang='es', to='ordinal').lower()
    except Exception:
        return f"pago número {n}"


def monto_en_palabras_simple(monto) -> str:
    """
    Convierte monto a palabras en minúsculas o capitalizado con sufijo quetzales.
    Ejemplo: 4334.00 -> 'Cuatro mil trescientos treinta y cuatro quetzales'
    """
    try:
        val = round(float(monto), 2)
        enteros = int(val)
        centavos = int(round((val - enteros) * 100))
        texto = num2words(enteros, lang='es').capitalize()
        moneda = "quetzal" if enteros == 1 else "quetzales"
        if centavos == 0:
            return f"{texto} {moneda}"
        else:
            cents_txt = num2words(centavos, lang='es')
            return f"{texto} {moneda} con {cents_txt} centavos"
    except Exception:
        return f"{monto} quetzales"



def nit_a_letras(nit_raw: str) -> str:
    """
    Convierte el NIT a su lectura dígito a dígito en minúsculas.
    Ejemplo: '1012084K' -> 'uno cero uno dos cero ocho cuatro K'
    """
    if not nit_raw:
        return ""
    nit_str = str(nit_raw).strip()
    partes = []
    for char in nit_str:
        if char in DIGITOS_LETRAS:
            partes.append(DIGITOS_LETRAS[char])
        elif char.isalnum():
            partes.append(char)
    return " ".join(partes)


def cuenta_a_letras(cuenta_raw: str) -> str:
    """
    Convierte un número de cuenta a su lectura dígito a dígito en mayúsculas.
    Ejemplo: '3696008759' -> 'TRES SEIS NUEVE SEIS CERO CERO OCHO SIETE CINCO NUEVE'
    """
    if not cuenta_raw:
        return ""
    cuenta_str = str(cuenta_raw).strip()
    partes = []
    for char in cuenta_str:
        if char in DIGITOS_LETRAS:
            partes.append(DIGITOS_LETRAS[char].upper())
        elif char.isalnum():
            partes.append(char.upper())
    return " ".join(partes)


def porcentaje_a_letras(tasa) -> str:
    """
    Convierte una tasa porcentual a palabras en mayúsculas.
    Ejemplo: 4.5 -> 'CUATRO PUNTO CINCO'
             12 -> 'DOCE'
    """
    try:
        val = float(tasa)
        if val.is_integer():
            return num2words(int(val), lang='es').upper()
        else:
            enteros = int(val)
            decimales_str = f"{val:.4f}".split('.')[1].rstrip('0')
            enteros_w = num2words(enteros, lang='es').upper()
            # Leer decimales
            decs_words = [DIGITOS_LETRAS.get(c, c).upper() for c in decimales_str]
            return f"{enteros_w} PUNTO {' '.join(decs_words)}"
    except Exception:
        return str(tasa).upper()


def plazo_a_letras(meses: int) -> str:
    """
    Convierte el plazo a texto formal.
    Ejemplo: 12 -> 'DOCE MESES (12)'
    """
    try:
        m = int(meses)
        letras = num2words(m, lang='es').upper()
        sufijo = "MES" if m == 1 else "MESES"
        return f"{letras} {sufijo} ({m})"
    except Exception:
        return f"{meses} MESES"


def cuotas_a_letras(num_cuotas: int) -> str:
    """
    Convierte cantidad de cuotas a texto formal.
    Ejemplo: 12 -> 'DOCE (12)'
    """
    try:
        c = int(num_cuotas)
        letras = num2words(c, lang='es').upper()
        return f"{letras} ({c})"
    except Exception:
        return f"{num_cuotas}"


def fecha_a_texto_estandar(d) -> str:
    """
    Convierte fecha a formato estándar: '08 de noviembre 2027'.
    Acepta objetos date/datetime o strings 'YYYY-MM-DD'.
    """
    if not d:
        return ""
    if isinstance(d, str):
        try:
            d = datetime.strptime(d[:10], "%Y-%m-%d").date()
        except Exception:
            return d

    dia = f"{d.day:02d}"
    mes = MESES[d.month] if 1 <= d.month <= 12 else str(d.month)
    return f"{dia} de {mes} {d.year}"


def fecha_a_texto_notarial(d) -> str:
    """
    Convierte fecha a formato notarial en letras completas.
    Ejemplo: date(2026, 10, 16) -> 'dieciséis de octubre del año dos mil veintiséis'
    """
    if not d:
        return ""
    if isinstance(d, str):
        try:
            d = datetime.strptime(d[:10], "%Y-%m-%d").date()
        except Exception:
            return d

    dia_letras = num2words(d.day, lang='es')
    mes = MESES[d.month] if 1 <= d.month <= 12 else str(d.month)
    anio_letras = num2words(d.year, lang='es')
    return f"{dia_letras} de {mes} del año {anio_letras}"


ORDINALES_MASC = [
    '', 'PRIMER', 'SEGUNDO', 'TERCER', 'CUARTO', 'QUINTO',
    'SEXTO', 'SÉPTIMO', 'OCTAVO', 'NOVENO', 'DÉCIMO',
    'DÉCIMO PRIMER', 'DÉCIMO SEGUNDO', 'DÉCIMO TERCER', 'DÉCIMO CUARTO', 'DÉCIMO QUINTO'
]

ORDINALES_FEM = [
    '', 'PRIMERA', 'SEGUNDA', 'TERCERA', 'CUARTA', 'QUINTA',
    'SEXTA', 'SÉPTIMA', 'OCTAVA', 'NOVENA', 'DÉCIMA',
    'DÉCIMA PRIMERA', 'DÉCIMA SEGUNDA', 'DÉCIMA TERCERA', 'DÉCIMA CUARTA', 'DÉCIMA QUINTA'
]


def ordinal(n: int, femenino: bool = False) -> str:
    """Retorna el número ordinal en español en mayúsculas."""
    lista = ORDINALES_FEM if femenino else ORDINALES_MASC
    if 1 <= n < len(lista):
        return lista[n]
    return f"{n}a." if femenino else f"{n}o."


def ordinal_pago_letras(n: int) -> str:
    """
    Convierte el número de cuota a su adjetivo ordinal masculino limpio en minúsculas
    para frases como 'el {ordinal} pago será por...' (1 -> 'primer', 11 -> 'décimo primer').
    """
    unidades = {
        1: "primer",
        2: "segundo",
        3: "tercer",
        4: "cuarto",
        5: "quinto",
        6: "sexto",
        7: "séptimo",
        8: "octavo",
        9: "noveno",
    }
    decenas = {
        1: "décimo",
        2: "vigésimo",
        3: "trigésimo",
        4: "cuadragésimo",
        5: "quincuagésimo",
        6: "sexagésimo",
    }
    if n < 1:
        return str(n)
    if n < 10:
        return unidades[n]
    dec = n // 10
    uni = n % 10
    if dec in decenas:
        if uni == 0:
            return decenas[dec]
        return f"{decenas[dec]} {unidades[uni]}"
    try:
        return num2words(n, lang='es', to='ordinal').lower()
    except Exception:
        return f"número {n}"


def sumar_meses_seguro(fecha_base, meses: int) -> date:
    """Suma meses a una fecha preservando el día de forma segura con o sin dateutil."""
    if not fecha_base:
        fecha_base = date.today()
    elif isinstance(fecha_base, str):
        try:
            fecha_base = datetime.strptime(fecha_base[:10], "%Y-%m-%d").date()
        except Exception:
            fecha_base = date.today()
    elif isinstance(fecha_base, datetime):
        fecha_base = fecha_base.date()

    meses = int(meses or 0)
    if meses == 0:
        return fecha_base

    try:
        from dateutil.relativedelta import relativedelta
        return fecha_base + relativedelta(months=meses)
    except ImportError:
        total_meses = fecha_base.month - 1 + meses
        nuevo_anio = fecha_base.year + total_meses // 12
        nuevo_mes = total_meses % 12 + 1
        ultimo_dia = calendar.monthrange(nuevo_anio, nuevo_mes)[1]
        nuevo_dia = min(fecha_base.day, ultimo_dia)
        return date(nuevo_anio, nuevo_mes, nuevo_dia)


def resolver_solicitud_o_credito(solicitud_o_id):
    """
    Si recibe un ID (int o str), resuelve la instancia desde InvestmentPlan
    (con respaldo en Credit). Si recibe un objeto, lo retorna directamente.
    """
    if not isinstance(solicitud_o_id, (int, str)):
        return solicitud_o_id

    solicitud = None
    try:
        from apps.InvestmentPlan.models import InvestmentPlan
        solicitud = (
            InvestmentPlan.objects
            .select_related("customer_id", "sucursal", "asesor_responsable")
            .filter(id=solicitud_o_id)
            .first()
        )
    except Exception:
        solicitud = None

    if solicitud is not None:
        return solicitud

    try:
        from apps.financings.models import Credit
        return (
            Credit.objects
            .select_related("customer_id", "sucursal", "destino_id")
            .get(id=solicitud_o_id)
        )
    except Exception as exc:
        raise RuntimeError(f"No se encontró Solicitud (InvestmentPlan) ni Crédito con ID: {solicitud_o_id}") from exc


def obtener_tasa_mensual_porcentaje(solicitud) -> float:
    """
    Obtiene la tasa de interés MENSUAL en porcentaje (ej. 10.0 para 10% mensual).
    En InvestmentPlan, tasa_interes suele almacenarse como tasa ANUAL (%) (ej. 120 -> 10% mensual).
    En Credit, tasa_interes suele almacenarse como decimal mensual (ej. 0.10 -> 10% mensual).
    """
    try:
        raw = float(getattr(solicitud, "tasa_interes", 0) or 0)
    except (ValueError, TypeError):
        raw = 0.0

    if raw <= 0:
        return 10.0

    es_solicitud = hasattr(solicitud, "total_value_of_the_product_or_service") or hasattr(solicitud, "investment_plan_code")
    if es_solicitud:
        if raw < 1:
            return round(raw * 100.0, 2)
        return round(raw / 12.0, 2)
    else:
        if raw < 1:
            return round(raw * 100.0, 2)
        return round(raw, 2)


def formatear_direccion_notarial(addr_obj) -> str:
    """Convierte un objeto Address (o diccionario/texto) en redacción notarial legible."""
    if not addr_obj:
        return ""
    if isinstance(addr_obj, str):
        return addr_obj.strip()

    street = str(getattr(addr_obj, "street", "") or "").strip()
    number = str(getattr(addr_obj, "number", "") or "").strip()
    state = str(getattr(addr_obj, "state", "") or "").strip()  # Municipio en Address
    city = str(getattr(addr_obj, "city", "") or "").strip()    # Departamento en Address

    partes = []
    if street:
        partes.append(street)
    if number and number.upper() not in ("", "0", "S/N", "N/A"):
        if not number.lower().startswith("zona"):
            partes.append(f"zona {number}")
        else:
            partes.append(number)
    if state:
        if "municipio" not in state.lower() and "jurisdicci" not in state.lower():
            partes.append(f"del municipio de {state}")
        else:
            partes.append(state)
    if city:
        if "departamento" not in city.lower():
            partes.append(f"del departamento de {city}")
        else:
            partes.append(city)

    if partes:
        return ", ".join(partes)
    if hasattr(addr_obj, "direccion") and callable(addr_obj.direccion):
        try:
            return str(addr_obj.direccion())
        except Exception:
            pass
    return str(addr_obj)


def _normalizar_estado_civil(raw_estado: str, genero: str) -> str:
    txt = str(raw_estado or "").strip().lower().replace("(a)", "").replace("(o)", "")
    es_fem = genero == "F"
    if "solter" in txt:
        return "soltera" if es_fem else "soltero"
    if "casad" in txt:
        return "casada" if es_fem else "casado"
    if "viud" in txt:
        return "viuda" if es_fem else "viudo"
    if "divorciad" in txt:
        return "divorciada" if es_fem else "divorciado"
    if "unid" in txt:
        return "unida" if es_fem else "unido"
    return txt or ("casada" if es_fem else "casado")


def _normalizar_nacionalidad(raw_nac: str, genero: str) -> str:
    txt = str(raw_nac or "").strip().lower()
    es_fem = genero == "F"
    if not txt or "guatemal" in txt:
        return "guatemalteca" if es_fem else "guatemalteco"
    if "mexic" in txt:
        return "mexicana" if es_fem else "mexicano"
    if "salvadore" in txt:
        return "salvadoreña" if es_fem else "salvadoreño"
    if "hondure" in txt:
        return "hondureña" if es_fem else "hondureño"
    if "nicarag" in txt:
        return "nicaragüense"
    if "costarric" in txt:
        return "costarricense"
    if "estadounid" in txt:
        return "estadounidense"
    if "colombian" in txt:
        return "colombiana" if es_fem else "colombiano"
    return txt


def extraer_persona_notarial(persona, default_genero: str = "F") -> dict:
    """
    Extrae las generales de ley y datos de identificación notarial de un Customer (o mock).
    """
    if not persona:
        return {
            "nombre": "--------",
            "genero": default_genero,
            "edad_num": "",
            "edad_letras": "mayor",
            "estado_civil": "casada" if default_genero == "F" else "casado",
            "nacionalidad": "guatemalteca" if default_genero == "F" else "guatemalteco",
            "profesion": "Comerciante",
            "domicilio": "de este domicilio",
            "dpi": "",
            "dpi_formateado": "",
            "cui_letras": "",
            "direccion": "--------",
        }

    if hasattr(persona, "get_full_name") and callable(persona.get_full_name):
        nombre_full = str(persona.get_full_name() or "").strip()
    else:
        fn = str(getattr(persona, "first_name", "") or "").strip()
        ln = str(getattr(persona, "last_name", "") or "").strip()
        nombre_full = f"{fn} {ln}".strip()
    nombre_full = nombre_full.upper() if nombre_full else "--------"

    gen_raw = str(getattr(persona, "gender", "") or "").strip().upper()
    if gen_raw.startswith("F") or "MUJ" in gen_raw:
        genero = "F"
    elif gen_raw.startswith("M") or "HOM" in gen_raw or "MASC" in gen_raw:
        genero = "M"
    else:
        genero = default_genero

    edad_num = None
    for metodo in ("get_age", "get_edad"):
        fn_edad = getattr(persona, metodo, None)
        if callable(fn_edad):
            try:
                edad_num = fn_edad()
                if edad_num is not None:
                    break
            except Exception:
                edad_num = None
    if edad_num is None:
        dob = getattr(persona, "date_birth", None)
        if isinstance(dob, str):
            try:
                dob = datetime.strptime(dob[:10], "%Y-%m-%d").date()
            except Exception:
                dob = None
        elif isinstance(dob, datetime):
            dob = dob.date()
        if isinstance(dob, date):
            hoy = date.today()
            edad_num = hoy.year - dob.year - ((hoy.month, hoy.day) < (dob.month, dob.day))

    edad_letras = edad_a_letras(edad_num) if edad_num is not None else "mayor"

    estado_raw = getattr(persona, "marital_status", "")
    if callable(getattr(persona, "get_estado_civil", None)):
        try:
            estado_raw = persona.get_estado_civil() or estado_raw
        except Exception:
            pass
    estado_civil = _normalizar_estado_civil(estado_raw, genero)

    nac_raw = getattr(persona, "nationality", "")
    if callable(getattr(persona, "get_nacionalidad", None)):
        try:
            nac_raw = persona.get_nacionalidad() or nac_raw
        except Exception:
            pass
    nacionalidad = _normalizar_nacionalidad(nac_raw, genero)

    profesion = str(getattr(persona, "profession_trade", "") or "").strip() or "Comerciante"

    dpi_raw = str(getattr(persona, "identification_number", "") or "").strip()
    cui_letras, dpi_formateado = cui_dpi_a_letras(dpi_raw, con_espacio=True) if dpi_raw else ("", "")

    addr_obj = getattr(persona, "_mock_address", None)
    if addr_obj is None:
        try:
            from apps.addresses.models import Address
            addr_obj = Address.objects.filter(customer_id=persona).first()
        except Exception:
            addr_obj = None
    if addr_obj is None and callable(getattr(persona, "get_direccion", None)):
        try:
            dir_res = persona.get_direccion()
            if dir_res:
                addr_obj = dir_res
        except Exception:
            addr_obj = None

    direccion = formatear_direccion_notarial(addr_obj)
    if not direccion:
        place_birth = str(getattr(persona, "place_birth", "") or "").strip()
        direccion = place_birth if place_birth else "Cobán, Alta Verapaz"

    return {
        "nombre": nombre_full,
        "genero": genero,
        "edad_num": edad_num if edad_num is not None else "",
        "edad_letras": edad_letras,
        "estado_civil": estado_civil,
        "nacionalidad": nacionalidad,
        "profesion": profesion,
        "domicilio": "de este domicilio",
        "dpi": dpi_formateado or dpi_raw,
        "dpi_formateado": dpi_formateado or dpi_raw,
        "cui_letras": cui_letras,
        "direccion": direccion,
    }


def construir_texto_garantia_item(tipo_garantia: str, specs: dict | None = None, descripcion: str = "") -> str:
   
    tipo = str(tipo_garantia or "MOBILIARIA").strip().upper()
    specs = specs if isinstance(specs, dict) else {}
    desc_extra = str(descripcion or "").strip()

    if tipo == "MOBILIARIA":
        bien = specs.get("DescripcionBien") or specs.get("descripcion") or specs.get("Descripcion") or desc_extra
        doc = specs.get("DocumentoAcredita") or specs.get("documento") or ""
        poliza = specs.get("NoPoliza") or ""
        partes = []
        if bien:
            partes.append(f"garantía mobiliaria sobre {bien}")
        else:
            partes.append("garantía mobiliaria sobre bienes muebles de mi propiedad")
        if doc:
            partes.append(f"bajo los siguientes datos registrales/documentales: {doc}")
        if poliza:
            partes.append(f"póliza número {poliza}")
        return ", ".join(partes)

    if tipo == "VEHICULO":
        marca = specs.get("Marca") or ""
        color = specs.get("Color") or ""
        placa = specs.get("Placa") or ""
        chasis = specs.get("NoChasis") or ""
        motor = specs.get("NoMotor") or ""
        tarjeta = specs.get("tarjeta_circulacion") or ""
        titulo = specs.get("titulo") or ""
        detalles = []
        if marca:
            detalles.append(f"marca {marca}")
        if color:
            detalles.append(f"color {color}")
        if placa:
            detalles.append(f"con placas de circulación {placa}")
        if chasis:
            detalles.append(f"chasis número {chasis}")
        if motor:
            detalles.append(f"motor número {motor}")
        if tarjeta:
            detalles.append(f"tarjeta de circulación {tarjeta}")
        if titulo:
            detalles.append(f"título de propiedad {titulo}")
        if detalles:
            return f"garantía mobiliaria sobre el vehículo automotor {', '.join(detalles)}"
        return f"garantía mobiliaria sobre vehículo automotor {desc_extra}".strip()

    if tipo == "HIPOTECA":
        finca = specs.get("finca") or specs.get("Finca") or ""
        folio = specs.get("folio") or specs.get("Folio") or ""
        libro = specs.get("libro") or specs.get("Libro") or ""
        ubic = specs.get("ubicacion") or specs.get("Ubicacion") or ""
        desc_h = ""
        area = specs.get("area") or specs.get("Area") or ""
        esc = specs.get("noEscritura") or specs.get("NoEscritura") or ""
        notario_h = specs.get("notario") or specs.get("Notario") or ""
        txt = "garantía hipotecaria sobre el bien inmueble"
        if desc_h:
            txt += f" consistente en {desc_h}"
        if ubic:
            txt += f", ubicado en {ubic}"
        if finca or folio or libro:
            reg = []
            if finca:
                reg.append(f"finca número {finca}")
            if folio:
                reg.append(f"folio {folio}")
            if libro:
                reg.append(f"del libro {libro}")
            txt += f", inscrito en el Registro General de la Propiedad bajo {', '.join(reg)}"
        if area:
            txt += f", con un área de {area} metros cuadrados"
        if esc:
            txt += f", según escritura pública número {esc}"
            if notario_h:
                txt += f" autorizada por el Notario {notario_h}"
        return txt

    if tipo == "DERECHO DE POSESION HIPOTECA":
        ubic = specs.get("Ubicacion") or specs.get("ubicacion") or ""
        desc_p = specs.get("Descripcion") or specs.get("descripcion") or desc_extra
        area = specs.get("Area") or specs.get("area") or ""
        esc = specs.get("NoEscritura") or specs.get("noEscritura") or ""
        notario_p = specs.get("Notario") or specs.get("notario") or ""
        txt = "garantía sobre los derechos de posesión de bien inmueble"
        if desc_p:
            txt += f" consistente en {desc_p}"
        if ubic:
            txt += f", ubicado en {ubic}"
        if area:
            txt += f", con un área de {area} metros cuadrados"
        if esc:
            txt += f", según escritura pública número {esc}"
            if notario_p:
                txt += f" autorizada por el Notario {notario_p}"
        return txt

    if tipo == "CHEQUE / PAGARE":
        no_cheque = specs.get("noCheque") or ""
        banco = specs.get("Banco") or ""
        cuenta = specs.get("NombreCuenta") or ""
        monto_ch = specs.get("Monto_cheque") or ""
        partes = ["título de garantía consistente en cheque"]
        if no_cheque:
            partes.append(f"número {no_cheque}")
        if banco:
            partes.append(f"del banco {banco}")
        if cuenta:
            partes.append(f"de la cuenta a nombre de {cuenta}")
        if monto_ch:
            try:
                partes.append(f"por la cantidad de {formato_quetzales(float(monto_ch))}")
            except Exception:
                pass
        return " ".join(partes)

    if tipo == "LABORAL":
        lugar = specs.get("lugar_trabajo") or specs.get("Lugar_de_Trabajo") or desc_extra or "la entidad donde laboro"
        return f"el sueldo y salario que devengo como empleado de {lugar}, así como con la totalidad de mis bienes presentes y futuros"

    if desc_extra:
        return desc_extra
    return "la totalidad de mis bienes presentes y futuros"


def generar_cuotas_para_contrato(solicitud) -> list[dict]:
    """
    Retorna lista de cuotas [{'mes': int, 'cuota': float, 'fecha_final': date}, ...]
    usando el motor PaymentPlan del proyecto o filas de BD, con fallback puro en Python.
    """
    plazo = int(getattr(solicitud, "plazo", 1) or 1)
    monto = float(getattr(solicitud, "total_value_of_the_product_or_service", None) or getattr(solicitud, "monto", 0) or 0)
    forma_pago = str(getattr(solicitud, "forma_de_pago", None) or "NIVELADA").upper()
    gracia = int(getattr(solicitud, "plazo_gracia", 0) or 0)
    tasa_mensual_pct = obtener_tasa_mensual_porcentaje(solicitud)

    fecha_inicio = getattr(solicitud, "fecha_inicio", None) or date.today()
    if isinstance(fecha_inicio, str):
        try:
            fecha_inicio = datetime.strptime(fecha_inicio[:10], "%Y-%m-%d").date()
        except Exception:
            fecha_inicio = date.today()
    elif isinstance(fecha_inicio, datetime):
        fecha_inicio = fecha_inicio.date()

    # 1. Si es instancia de Credit con cuotas guardadas en BD
    if not hasattr(solicitud, "total_value_of_the_product_or_service") and getattr(solicitud, "id", None):
        try:
            from apps.financings.models import PaymentPlan as CuotaModel
            qs = CuotaModel.objects.filter(credit_id=solicitud).order_by("mes", "start_date")
            if qs.exists():
                cuotas_db = []
                for idx, row in enumerate(qs, 1):
                    f_fin = row.due_date or row.fecha_limite or sumar_meses_seguro(fecha_inicio, idx)
                    if isinstance(f_fin, datetime):
                        f_fin = f_fin.date()
                    cuotas_db.append({
                        "mes": int(row.mes or idx),
                        "cuota": float(row.installment or 0),
                        "fecha_final": f_fin,
                    })
                if cuotas_db:
                    return cuotas_db
        except Exception:
            pass

    # 2. Motor oficial PaymentPlan + Credit del proyecto
    try:
        from apps.financings.clases.paymentplan import PaymentPlan as CalcPaymentPlan
        from apps.financings.clases.credit import Credit as CalcCredit
        cliente = getattr(solicitud, "customer_id", None)
        credito_sim = CalcCredit(
            "",
            Decimal(str(monto)),
            plazo,
            Decimal(str(tasa_mensual_pct)),
            forma_pago,
            "MENSUAL",
            fecha_inicio.strftime("%Y-%m-%d"),
            "CONSUMO",
            cliente,
            None,
            None,
            gracia,
        )
        plan_obj = CalcPaymentPlan(credito_sim)
        plan_calc = plan_obj.generar_plan()
        cuotas_calc = []
        for idx, item in enumerate(plan_calc, 1):
            f_fin = item.get("fecha_final") or sumar_meses_seguro(fecha_inicio, idx)
            if isinstance(f_fin, datetime):
                f_fin = f_fin.date()
            cuotas_calc.append({
                "mes": int(item.get("mes", idx)),
                "cuota": float(item.get("cuota", 0)),
                "fecha_final": f_fin,
            })
        if cuotas_calc:
            return cuotas_calc
    except Exception:
        pass

    # 3. Fallback puro en Python (compatible fuera de Django / entornos sin dateutil)
    r = Decimal(str(tasa_mensual_pct)) / Decimal("100")
    P = Decimal(str(monto))
    cuotas = []

    if forma_pago == "NIVELADA":
        if r > 0 and plazo > 0:
            factor = ((1 + r) ** plazo * r) / ((1 + r) ** plazo - 1)
            cuota_const = float(math.ceil(round(P * factor, 2)))
        else:
            cuota_const = float(math.ceil(round(P / Decimal(max(1, plazo)), 2)))
        for mes in range(1, plazo + 1):
            cuotas.append({
                "mes": mes,
                "cuota": cuota_const,
                "fecha_final": sumar_meses_seguro(fecha_inicio, mes),
            })

    elif forma_pago in ("INTERES MENSUAL Y CAPITAL AL VENCIMIENTO", "INTERES Y CAPITAL AL VENCIMIENTO"):
        active_plazo = max(1, plazo - gracia)
        cap_mes = math.ceil(round(P / Decimal(active_plazo), 2))
        saldo = P
        for mes in range(1, plazo + 1):
            interes_mes = math.ceil(round(saldo * r, 2))
            if mes > gracia:
                cuota_mes = float(interes_mes + cap_mes)
                saldo = max(Decimal("0"), saldo - Decimal(cap_mes))
            else:
                cuota_mes = float(interes_mes) if forma_pago == "INTERES MENSUAL Y CAPITAL AL VENCIMIENTO" else 0.0
            cuotas.append({
                "mes": mes,
                "cuota": cuota_mes,
                "fecha_final": sumar_meses_seguro(fecha_inicio, mes),
            })

    else:
        # AMORTIZACIONES A CAPITAL (por defecto cuando hay variación mensual)
        cap_mes = math.ceil(round(P / Decimal(max(1, plazo)), 2))
        for mes in range(1, plazo + 1):
            saldo = max(Decimal("0"), P - Decimal(cap_mes) * Decimal(mes - 1))
            interes_mes = math.ceil(round(saldo * r, 2))
            cuota_mes = float(interes_mes + cap_mes)
            cuotas.append({
                "mes": mes,
                "cuota": cuota_mes,
                "fecha_final": sumar_meses_seguro(fecha_inicio, mes),
            })

    return cuotas


def generar_desglose_cuotas_desde_solicitud(solicitud) -> tuple[str, str]:
    """
    Construye el texto legal completo de desglose de cuotas ('desglose_cuotas_texto')
    y la cantidad de cuotas en letras mayúsculas ('plazo_cuotas_letras').
    """
    cuotas = generar_cuotas_para_contrato(solicitud)
    plazo = len(cuotas) or int(getattr(solicitud, "plazo", 1) or 1)
    plazo_letras = numero_a_letras(plazo, mayusculas=True)

    if not cuotas:
        return ("un pago único al vencimiento del plazo.", plazo_letras)

    if len(cuotas) == 1:
        c = cuotas[0]
        val = round(float(c["cuota"]), 2)
        palabras = monto_en_palabras_simple(val).lower()
        fecha_txt = fecha_a_texto_notarial(c["fecha_final"])
        texto = (
            f"un único pago al vencimiento de la obligación que será por la cantidad de "
            f"{palabras} (Q. {val:,.2f}); debiendo hacer el pago el día {fecha_txt}."
        )
        return (texto, plazo_letras)

    partes_cuotas = []
    total = len(cuotas)
    for idx, c in enumerate(cuotas, 1):
        val = round(float(c["cuota"]), 2)
        palabras = monto_en_palabras_simple(val).lower()
        if idx < total:
            ord_txt = ordinal_pago_letras(idx)
            partes_cuotas.append(
                f"el {ord_txt} pago será por la cantidad de {palabras} (Q. {val:,.2f})"
            )
        else:
            partes_cuotas.append(
                f"y, un último pago al vencimiento de la obligación que será por la cantidad de {palabras} (Q. {val:,.2f})"
            )

    f1 = cuotas[0]["fecha_final"]
    f_last = cuotas[-1]["fecha_final"]
    f1_txt = fecha_a_texto_notarial(f1)
    f_last_txt = fecha_a_texto_notarial(f_last)
    dia_pago = f1.day if isinstance(f1, (date, datetime)) else 1
    dia_letras = numero_a_letras(dia_pago, mayusculas=False).lower()

    if total > 2:
        fechas_txt = (
            f"debiendo hacer el primer pago el día {f1_txt}; "
            f"y, los pagos mensuales subsiguientes los días {dia_letras} de cada mes calendario; "
            f"y, un último pago al vencimiento de la obligación el día {f_last_txt}."
        )
    else:
        fechas_txt = (
            f"debiendo hacer el primer pago el día {f1_txt}; "
            f"y, un último pago al vencimiento de la obligación el día {f_last_txt}."
        )

    texto_final = "; ".join(partes_cuotas) + "; " + fechas_txt
    return (texto_final, plazo_letras)


def extraer_datos_base_contrato_desde_solicitud(solicitud) -> dict:
    """
    Extrae las claves comunes compartidas por los contratos de Deudor Directo
    y Con Fiador(es) a partir de una instancia real (o mock) de InvestmentPlan o Credit.
    """
    cliente = getattr(solicitud, "customer_id", None)
    deudor = extraer_persona_notarial(cliente, default_genero="F")

    sucursal = getattr(solicitud, "sucursal", None)
    ciudad = "Cobán"
    departamento = "Alta Verapaz"
    empresa_direccion = (
        "octava avenida uno guion doce, zona uno, de la jurisdicción municipal de Cobán del departamento de Alta Verapaz"
    )
    empresa_cuenta = "3696008759"

    if sucursal is not None:
        cta = getattr(sucursal, "numero_de_cuenta_banco", None)
        if cta:
            empresa_cuenta = str(cta).strip()

        suc_addr = getattr(sucursal, "_mock_address", None)
        if suc_addr is None and callable(getattr(sucursal, "get_direc", None)):
            try:
                res_dir = sucursal.get_direc()
                if res_dir:
                    suc_addr = res_dir
            except Exception:
                suc_addr = None

        if suc_addr is not None and not isinstance(suc_addr, str):
            ciudad = str(getattr(suc_addr, "state", None) or getattr(sucursal, "city", None) or ciudad).strip()
            departamento = str(getattr(suc_addr, "city", None) or getattr(sucursal, "state", None) or departamento).strip()

            empresa_direccion = formatear_direccion_notarial(sucursal.get_direccion()) or empresa_direccion
        else:
            if getattr(sucursal, "city", None):
                ciudad = str(sucursal.city).strip()
            if getattr(sucursal, "state", None):
                departamento = str(sucursal.state).strip()
            if callable(getattr(sucursal, "get_direccion", None)):
                try:
                    gd = sucursal.get_direccion()
                    if gd:
                        empresa_direccion = str(gd).strip()
                except Exception:
                    pass

    f_ini = date.today()
    if isinstance(f_ini, str):
        try:
            f_ini = date.today()
        except Exception:
            f_ini = date.today()
    elif isinstance(f_ini, datetime):
        f_ini = f_ini.date()

    fecha_letras = fecha_a_texto_notarial(f_ini)

    capital = float(getattr(solicitud, "total_value_of_the_product_or_service", None) or getattr(solicitud, "monto", 0) or 0)
    monto_letras = monto_a_letras_quetzales(capital).replace(" EXACTOS", "")

    plazo_cuotas_letras_and_desc = generar_desglose_cuotas_desde_solicitud(solicitud)
    desglose_cuotas_texto, plazo_cuotas_letras = plazo_cuotas_letras_and_desc

    destino = (
        getattr(solicitud, "sub_destino", None)
        or getattr(solicitud, "investment_plan_description", None)
        or getattr(solicitud, "proposito", None)
        or getattr(solicitud, "type_of_product_or_service", None)
        or getattr(solicitud, "tipo_credito", None)
        or "comercio y capital de trabajo"
    )
    destino = str(destino).strip()

    tasa_mensual = obtener_tasa_mensual_porcentaje(solicitud)
    tasa_str = str(int(tasa_mensual)) if float(tasa_mensual).is_integer() else f"{tasa_mensual:g}"
    tasa_letras = f"{porcentaje_a_letras(tasa_mensual)} POR CIENTO"

    acta_numero, acta_fecha = _obtener_acta_solicitud(solicitud)

    mora_raw = getattr(solicitud, "tasa_mora", None)
    if mora_raw is not None:
        try:
            mora_f = float(mora_raw)
            mora_pct_num = mora_f * 100.0 if 0 < mora_f < 1 else mora_f
            multa_mora_pct = str(int(mora_pct_num)) if mora_pct_num.is_integer() else f"{mora_pct_num:g}"
        except Exception:
            multa_mora_pct = "10"
    else:
        multa_mora_pct = "10"

    return {
        "ciudad": ciudad,
        "departamento": departamento,
        "fecha_contrato_letras": fecha_letras,
        # Deudor Principal
        "deudor_nombre": deudor["nombre"],
        "deudor_edad_letras": deudor["edad_letras"],
        "deudor_estado_civil": deudor["estado_civil"],
        "deudor_nacionalidad": deudor["nacionalidad"],
        "deudor_profesion": deudor["profesion"],
        "deudor_domicilio": deudor["domicilio"],
        "deudor_dpi": deudor["dpi"],
        "deudor_cui_letras": deudor["cui_letras"],
        "deudor_direccion": deudor["direccion"],
        "deudor_genero": deudor["genero"],
        # Representante Legal El Telar
        "rep_legal_nombre": "EDGAR ARMANDO ALVARADO BERMÚDEZ",
        "rep_legal_edad_letras": "cuarenta y un",
        "rep_legal_edad_num": "41",
        "rep_legal_estado_civil": "soltero",
        "rep_legal_nacionalidad": "guatemalteco",
        "rep_legal_profesion": "Ingeniero Civil",
        "rep_legal_domicilio": "de este domicilio",
        "rep_legal_dpi": "1837 11882 1601",
        "rep_legal_cui_letras": "un mil ochocientos treinta y siete espacio once mil ochocientos ochenta y dos espacio un mil seiscientos uno",
        "rep_legal_cargo": "ADMINISTRADOR ÚNICO Y REPRESENTANTE LEGAL",
        # Empresa El Telar
        "empresa_nombre": "INVERSIONES INTEGRALES EL TELAR, SOCIEDAD ANÓNIMA",
        "empresa_cuenta_bancaria": empresa_cuenta,
        "empresa_direccion": empresa_direccion,
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
        "monto_capital": capital,
        "monto_capital_letras": monto_letras,
        "plazo_cuotas_letras": plazo_cuotas_letras,
        "tipo_pago_nombre": "ABONOS MENSUALES",
        "desglose_cuotas_texto": desglose_cuotas_texto,
        "destino_credito": destino,
        "tasa_interes_letras": tasa_letras,
        "tasa_interes_num": tasa_str,
        "multa_mora_pct": multa_mora_pct,
        "resolucion_ente": "------",
        "acta_numero": f" {acta_numero} de fecha {acta_fecha}" if acta_numero and acta_fecha else " ------",
        # Notario
        "notario_fecha_letras": fecha_letras,
    }
