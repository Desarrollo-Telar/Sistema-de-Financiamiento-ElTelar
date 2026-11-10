# AUTENTICACION
from .autenticacion import logout_view, login_view, verification

# BUSCADOR
from .buscador import Search

# SISTEMA
from .sistema import generate_qr, index, list_reportes_modulos, agradecimeinto, check_list_customer, cambio_oficina

# API FUNCIONALIDADS
from .generacion_mensaje_whatsapp import GenerarMensajePagoAPIView, GenerandoMensajeSaldoApi

# DOCUMENTOS WORD
from .documentos_views import (
    descargar_pagare_ejemplo,
    descargar_pagare_credito,
    descargar_contrato_ejemplo,
    descargar_contrato_directo_ejemplo,
    descargar_contrato_fiador_ejemplo,
    panel_descarga_pagare,
)