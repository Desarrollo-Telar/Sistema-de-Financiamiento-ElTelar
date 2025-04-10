# MODELOS
from apps.financings.models import PaymentPlan, Payment, Banco

# TIEMPO
from datetime import datetime
from django.utils.timezone import now

from apps.financings.functions import realizar_pago
from apps.financings.functions_payment import generar
from apps.financings.task import comparacion_para_boletas_divididas

from asgiref.sync import sync_to_async

def cargar_boletas_estado():
    pagos_estado_completado = Payment.objects.filter(estado_transaccion = "COMPLETADO")
    for pago in pagos_estado_completado:
        boleta = Banco.objects.filter(referencia=pago.numero_referencia).first()
        if boleta :
            

            boleta.status = True
            boleta.save()
    return 'Cargado'


def ver_cuotas_no_cargadas():
    #generar()
    
    #comparacion_para_boletas_divididas()

    cargar_boletas_estado()
    return 'Listo'