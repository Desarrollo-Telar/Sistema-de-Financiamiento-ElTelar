
# CON RELACION A CLIENTES
from .correos_para_clientes import send_email_welcome_customer, send_email_new_customer

# CON RELACION A USUARIOS
from .correos_para_usuarios import send_email_code_verification, send_email_user_conect_or_disconect

# CON RELACION A LAS BOLETAS DE PAGO Y RECIBOS
from .correos_para_pagos import send_email_alert, send_email_recibo

# CON RELACION A LOS CREDITOS, ACREEDORES Y SEGUROS
from .correos_para_creditos import send_email_new_credit, send_email_update_of_quotas, send_email_quotas_for_change, send_email_next_update_of_quotas