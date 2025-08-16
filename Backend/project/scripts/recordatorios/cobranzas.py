
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
    hora_actual = datetime.now().time()    
    hora_fin = time(9, 0)      # 09:00 AM

    for cobrar in cobranzas:
        print('Enviando Recordatorio')
        if hora_actual <= hora_fin:
            send_email_recordatorio_cobranza(cobrar)
        else:
            print("Fuera del horario permitido para enviar correos.")