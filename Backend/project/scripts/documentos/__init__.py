"""
Módulo de generación de documentos de El Telar S.A.
Permite generar documentos legales en Word (.docx) como pagarés, contratos directos y contratos con fiador.
"""

from .pagare import (
    generar_pagare_word,
    generar_pagare_desde_credito,
    obtener_datos_ejemplo,
)
from .contrato import (
    generar_contrato_word,
    obtener_datos_ejemplo_contrato,
)
from .contrato_deudor_directo import (
    generar_contrato_deudor_directo_word,
    obtener_datos_ejemplo_deudor_directo,
)
from .contrato_con_fiador import (
    generar_contrato_con_fiador_word,
    obtener_datos_ejemplo_con_fiador,
)
from .helpers import (
    monto_a_letras_quetzales,
    cui_dpi_a_letras,
    edad_a_letras,
    ordinal_masculino,
    nit_a_letras,
    cuenta_a_letras,
    porcentaje_a_letras,
    plazo_a_letras,
    cuotas_a_letras,
    fecha_a_texto_estandar,
    fecha_a_texto_notarial,
    formato_quetzales,
    numero_a_letras,
)

__all__ = [
    # Pagaré
    "generar_pagare_word",
    "generar_pagare_desde_credito",
    "obtener_datos_ejemplo",
    # Contrato general / dispatcher
    "generar_contrato_word",
    "obtener_datos_ejemplo_contrato",
    # Contrato Deudor Directo (sin fiador)
    "generar_contrato_deudor_directo_word",
    "obtener_datos_ejemplo_deudor_directo",
    # Contrato con Fiador Solidario
    "generar_contrato_con_fiador_word",
    "obtener_datos_ejemplo_con_fiador",
    # Helpers
    "monto_a_letras_quetzales",
    "cui_dpi_a_letras",
    "edad_a_letras",
    "ordinal_masculino",
    "nit_a_letras",
    "cuenta_a_letras",
    "porcentaje_a_letras",
    "plazo_a_letras",
    "cuotas_a_letras",
    "fecha_a_texto_estandar",
    "fecha_a_texto_notarial",
    "formato_quetzales",
    "numero_a_letras",
]
