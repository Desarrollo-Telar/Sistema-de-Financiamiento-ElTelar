"""
Módulo de utilidades y formateadores para la generación de documentos legales
(Guatemala - El Telar S.A.).
Incluye conversiones de montos a letras en Quetzales, CUI/DPI a letras,
NIT a letras, cuentas bancarias, tasas de interés, plazos y fechas notariales.
"""

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
    """Convierte edad a palabras en minúsculas (ej. 33 -> 'treinta y tres')."""
    try:
        return num2words(int(edad), lang='es').lower()
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
