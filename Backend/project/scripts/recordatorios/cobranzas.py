
# TIEMPO
from datetime import datetime, time, timedelta, date
from django.utils.timezone import now

# Modelos
from apps.customers.models import CreditCounselor, Cobranza
from django.db.models import Q

# Correos Electronicos
from project.send_mail import send_email_recordatorio_cobranza

def fechas_cobranzas():
    hoy = date.today()
    hasta = hoy + timedelta(days=7)

    cobranzas = Cobranza.objects.filter(
        fecha_promesa_pago__range=[hoy, hasta]
    ).filter(
        Q(resultado__icontains='Promesa de pago')|
        ~Q(estado_cobranza__icontains='COMPLETADO')
    )
    print('informe de cobranza')

    for cobrar in cobranzas:
        print('Enviando Recordatorio')
        send_email_recordatorio_cobranza(cobrar)