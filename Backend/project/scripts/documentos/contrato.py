"""
Módulo unificado para la generación del CONTRATO DE RECONOCIMIENTO DE DEUDA en formato Word (.docx).
Permite seleccionar automáticamente entre:
- Contrato con Deudor Directo (sin fiador): 2 comparecientes, 3 cláusulas.
- Contrato con Fiador Solidario: 3 comparecientes, 4 cláusulas.
"""

from .contrato_deudor_directo import (
    generar_contrato_deudor_directo_word,
    obtener_datos_ejemplo_deudor_directo,
)
from .contrato_con_fiador import (
    generar_contrato_con_fiador_word,
    obtener_datos_ejemplo_con_fiador,
)


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
    - Si 'fiador_nombre' tiene valor o 'tiene_fiador' es True, utiliza la plantilla con Fiador Solidario (3 partes, 4 cláusulas).
    - En caso contrario, genera la plantilla de Deudor Directo (2 partes, 3 cláusulas).
    """
    if datos_entrada is None:
        datos_entrada = {}

    tiene_fiador = datos_entrada.get("tiene_fiador")
    fiador_nombre = datos_entrada.get("fiador_nombre")

    if tiene_fiador is True or (tiene_fiador is not False and bool(fiador_nombre)):
        return generar_contrato_con_fiador_word(datos_entrada, output_target=output_target)
    else:
        return generar_contrato_deudor_directo_word(datos_entrada, output_target=output_target)
