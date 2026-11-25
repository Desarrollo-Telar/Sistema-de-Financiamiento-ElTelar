"""
Módulo de generación de documentos de El Telar S.A.
Permite generar documentos legales en Word (.docx) como pagarés, contratos directos y contratos con fiador.
"""

from .pagare import (
    generar_pagare_word,
    generar_pagare_desde_credito,
    generar_pagare_desde_solicitud,
    extraer_datos_pagare_desde_solicitud,
    obtener_datos_ejemplo,
)
from .contrato import (
    generar_contrato_word,
    generar_contrato_desde_solicitud,
    generar_contrato_desde_credito,
    obtener_datos_ejemplo_contrato,
)
from .contrato_deudor_directo import (
    generar_contrato_deudor_directo_word,
    generar_contrato_deudor_directo_desde_solicitud,
    generar_contrato_deudor_directo_desde_credito,
    extraer_datos_contrato_deudor_directo_desde_solicitud,
    obtener_datos_ejemplo_deudor_directo,
)
from .contrato_con_fiador import (
    generar_contrato_con_fiador_word,
    generar_contrato_con_fiador_desde_solicitud,
    generar_contrato_con_fiador_desde_credito,
    extraer_datos_contrato_con_fiador_desde_solicitud,
    obtener_datos_ejemplo_con_fiador,
)
from .resolucion import (
    generar_resolucion_word,
    generar_resolucion_desde_solicitud,
    generar_resolucion_desde_credito,
    extraer_datos_resolucion_desde_solicitud,
    obtener_datos_ejemplo_resolucion,
)
from .acta import (
    generar_acta_word,
    generar_acta_desde_solicitud,
    generar_acta_desde_credito,
    extraer_datos_acta_desde_solicitud,
    obtener_datos_ejemplo_acta,
    hora_a_texto_notarial,
    cui_dpi_a_letras_acta,
    digitos_a_letras_minusculas,
)
from .helpers import (
    FECHA_NACIMIENTO_EDGAR_ALVARADO,
    FECHA_NACIMIENTO_GRECIA_RODRIGUEZ,
    calcular_edad_desde_fecha,
    edad_notarial_desde_fecha,
    monto_a_letras_quetzales,
    cui_dpi_a_letras,
    edad_a_letras,
    ordinal_masculino,
    ordinal_pago_letras,
    sumar_meses_seguro,
    nit_a_letras,
    cuenta_a_letras,
    porcentaje_a_letras,
    plazo_a_letras,
    cuotas_a_letras,
    fecha_a_texto_estandar,
    fecha_a_texto_notarial,
    formato_quetzales,
    numero_a_letras,
    resolver_solicitud_o_credito,
    extraer_persona_notarial,
    extraer_datos_base_contrato_desde_solicitud,
)

__all__ = [
    # Pagaré
    "generar_pagare_word",
    "generar_pagare_desde_credito",
    "generar_pagare_desde_solicitud",
    "extraer_datos_pagare_desde_solicitud",
    "obtener_datos_ejemplo",
    # Contrato general / dispatcher
    "generar_contrato_word",
    "generar_contrato_desde_solicitud",
    "generar_contrato_desde_credito",
    "obtener_datos_ejemplo_contrato",
    # Contrato Deudor Directo (sin fiador)
    "generar_contrato_deudor_directo_word",
    "generar_contrato_deudor_directo_desde_solicitud",
    "generar_contrato_deudor_directo_desde_credito",
    "extraer_datos_contrato_deudor_directo_desde_solicitud",
    "obtener_datos_ejemplo_deudor_directo",
    # Contrato con Fiador Solidario
    "generar_contrato_con_fiador_word",
    "generar_contrato_con_fiador_desde_solicitud",
    "generar_contrato_con_fiador_desde_credito",
    "extraer_datos_contrato_con_fiador_desde_solicitud",
    "obtener_datos_ejemplo_con_fiador",
    # Resolución Comité Técnico de Créditos
    "generar_resolucion_word",
    "generar_resolucion_desde_solicitud",
    "generar_resolucion_desde_credito",
    "extraer_datos_resolucion_desde_solicitud",
    "obtener_datos_ejemplo_resolucion",
    # Acta Notarial (Entrega de Cheque y Compromiso de Pago)
    "generar_acta_word",
    "generar_acta_desde_solicitud",
    "generar_acta_desde_credito",
    "extraer_datos_acta_desde_solicitud",
    "obtener_datos_ejemplo_acta",
    "hora_a_texto_notarial",
    "cui_dpi_a_letras_acta",
    "digitos_a_letras_minusculas",
    # Helpers
    "FECHA_NACIMIENTO_EDGAR_ALVARADO",
    "FECHA_NACIMIENTO_GRECIA_RODRIGUEZ",
    "calcular_edad_desde_fecha",
    "edad_notarial_desde_fecha",
    "monto_a_letras_quetzales",
    "cui_dpi_a_letras",
    "edad_a_letras",
    "ordinal_masculino",
    "ordinal_pago_letras",
    "sumar_meses_seguro",
    "nit_a_letras",
    "cuenta_a_letras",
    "porcentaje_a_letras",
    "plazo_a_letras",
    "cuotas_a_letras",
    "fecha_a_texto_estandar",
    "fecha_a_texto_notarial",
    "formato_quetzales",
    "numero_a_letras",
    "resolver_solicitud_o_credito",
    "extraer_persona_notarial",
    "extraer_datos_base_contrato_desde_solicitud",
]
