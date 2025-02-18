# FUNCIONES PARA CREAR
from .create import create_credit, create_disbursement, create_guarantee

# FUNCIONES PARA LISTAR
from .read import list_bank, list_credit, list_disbursement, list_guarantee, list_payment,PaymentSearch,BankSearch
from .read import CreditSearch

# FUNCIONES PARA ACTUALIZAR
from .update import update_pago, update_cuota, generar_factura

# FUNCIONES PARA DETALLAR
from .detail import detail_credit, detallar_recibo, detalle_boleta, detallar_desembolso,detalle_factura, detalle_estado_cuenta, clasificacion_detallar
from .detail import boleta, detallar_garantia
# FUNCIONES PARA GENERAR PDFS
from .generar_pdf import render_pdf_factura, render_pdf_estado_cuenta, render_pdf_calculos_credito, render_pdf_plan_pagos, render_pdf_plan_pagos_acreedor, render_pdf_plan_pagos_seguro
from .generar_pdf import render_pdf_calculos_credito_acreedor, render_pdf_calculos_credito_seguro
# REPORTES
from .reportes import reportes_generales

# Funcion para eliminar
from .delete import delete_credit


# ORGANIZACION DEL CODIGO
# PAGOS
from .payment import create_payment

# Filtros
from .filtros import filter_credito_cancelado, filter_credito_en_atraso, filter_credito_en_falta_aportacion, filter_credito_reciente, filter_list_payment_pendiente, filter_list_payment_completados
from .filtros import filter_list_bank_no_vinculado, filter_list_bank_vinculado