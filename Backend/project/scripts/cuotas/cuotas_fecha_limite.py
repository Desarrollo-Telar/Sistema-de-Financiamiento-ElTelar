# MODELS
from apps.financings.models import PaymentPlan
from django.db.models import Q

# TIEMPO
from datetime import datetime, time
from django.utils.timezone import now

# SCRIPTS
from scripts.cuotas.accion_sobre_cuotas import recorrido_de_cuotas

# MENSAJE EMAIL
from project.send_mail import send_email_update_of_quotas

def verificador_de_cuotas_fecha_limite(dia):
    print('ANALISIS SOBRE FECHA_LIMITE')
    planes = PaymentPlan.objects.filter(fecha_limite__date=dia, cuota_vencida=False).filter( 
        Q(credit_id__is_paid_off = False) | 
        Q(acreedor__is_paid_off = False ) | 
        Q(seguro__is_paid_off = False)|
        Q(credit_id__estado_judicial = False)
        )
    
    if not planes.exists():
        print("No hay registro")
        return
    recorrido_de_cuotas(planes, 'FECHA_LIMITE')
    for cuota in planes:
        print(cuota)

    
    hora_actual = datetime.now().time()    
    hora_fin = time(9, 0)      # 09:00 AM

    
    if hora_actual <= hora_fin:
        # AQUI SE DEBE DE ENVIAR MENSAJES PARA DECIR QUE LOS CREDITOS YA VENCIERON
        send_email_update_of_quotas(planes)
    else:
        print("Fuera del horario permitido para enviar correos.")
    
    
    