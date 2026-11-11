"""
Módulo unificado para la generación del CONTRATO DE RECONOCIMIENTO DE DEUDA en formato Word (.docx).
Permite seleccionar automáticamente entre:
- Contrato con Deudor Directo (sin fiador): 2 comparecientes, 3 cláusulas.
- Contrato con Fiador Solidario: 3 comparecientes, 4 cláusulas.
"""

from .contrato_deudor_directo import (
    generar_contrato_deudor_directo_word,
    generar_contrato_deudor_directo_desde_solicitud,
    obtener_datos_ejemplo_deudor_directo,
)
from .contrato_con_fiador import (
    generar_contrato_con_fiador_word,
    generar_contrato_con_fiador_desde_solicitud,
    obtener_datos_ejemplo_con_fiador,
)
from .helpers import resolver_solicitud_o_credito


def obtener_datos_ejemplo_contrato(con_fiador: bool = False) -> dict:
    """
    Retorna datos de ejemplo según la modalidad solicitada:
    con_fiador=True: Plantilla Estefany Yusela López Ruiz / Fredy Joel García Moscoso
    con_fiador=False: Plantilla Candy Claramaría Cantoral Caal de Papa
    """
    if con_fiador:
        return obtener_datos_ejemplo_con_fiador()
    return obtener_datos_ejemplo_deudor_directo()


def generar_contrato_word(datos_entrada: dict | None = None, output_target=None):
    """
    Genera el Contrato de Reconocimiento de Deuda en formato Word.
    Detecta automáticamente si se incluye Fiador Solidario en el diccionario de datos:
    - Si 'fiadores' (lista), 'fiador_nombre' tiene valor o 'tiene_fiador' es True, utiliza la plantilla con Fiador(es) Solidario(s).
    - En caso contrario, genera la plantilla de Deudor Directo (2 partes, 3 cláusulas).
    """
    if datos_entrada is None:
        datos_entrada = {}

    tiene_fiador = datos_entrada.get("tiene_fiador")
    fiador_nombre = datos_entrada.get("fiador_nombre")
    fiadores = datos_entrada.get("fiadores")

    if tiene_fiador is True or (tiene_fiador is not False and (bool(fiador_nombre) or bool(fiadores))):
        return generar_contrato_con_fiador_word(datos_entrada, output_target=output_target)
    else:
        return generar_contrato_deudor_directo_word(datos_entrada, output_target=output_target)


def generar_contrato_desde_solicitud(solicitud_o_id, con_fiador: bool | None = None, overrides: dict | None = None, output_target=None):
    """
    Genera el Contrato de Reconocimiento de Deuda en Word (.docx) a partir de una Solicitud (InvestmentPlan)
    o Crédito (Credit), seleccionando automáticamente la modalidad con o sin fiadores solidarios.
    """
    solicitud = resolver_solicitud_o_credito(solicitud_o_id)

    if con_fiador is None:
        tiene_fiador_campo = bool(getattr(solicitud, "fiador", None))
        if not tiene_fiador_campo:
            garantias = getattr(solicitud, "garantias", None) or []
            if isinstance(garantias, list):
                tiene_fiador_campo = any(
                    isinstance(g, dict) and str(g.get("tipo") or g.get("tipo_garantia") or "").upper() == "FIADOR"
                    for g in garantias
                )
        con_fiador = tiene_fiador_campo

    if con_fiador:
        return generar_contrato_con_fiador_desde_solicitud(solicitud, overrides=overrides, output_target=output_target)
    return generar_contrato_deudor_directo_desde_solicitud(solicitud, overrides=overrides, output_target=output_target)


generar_contrato_desde_credito = generar_contrato_desde_solicitud
