# MODELS
from apps.financings.models import PaymentPlan

# TIEMPO
from datetime import datetime, time, timedelta
from django.utils.timezone import now

# SCRIPTS
from scripts.cuotas.accion_sobre_cuotas import recorrido_de_cuotas

# MENSAJE EMAIL
from project.send_mail import send_email_quotas_for_change


def cuotas_por_vencerse_alerta():
    hoy = datetime.now() 
    hasta = hoy + timedelta(days=7)

    planes = PaymentPlan.objects.filter(due_date__range=[hoy, hasta], status=False).order_by('due_date')
    print(planes)
    send_email_quotas_for_change(planes, hoy.date(), hasta.date())