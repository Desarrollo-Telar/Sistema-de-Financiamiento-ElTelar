# MODELOS
from apps.financings.models import PaymentPlan, Payment, Banco
from apps.accountings.models import Creditor, Insurance, Income, Egress
# TIEMPO
from datetime import datetime
from django.utils.timezone import now

from apps.financings.functions import realizar_pago
from apps.financings.functions_payment import generar
from apps.financings.task import comparacion_para_boletas_divididas, comparacion

from asgiref.sync import sync_to_async

def cargar_boletas_estado():
    pagos_estado_completado = Payment.objects.filter(estado_transaccion = "COMPLETADO")
    for pago in pagos_estado_completado:
        boleta = Banco.objects.filter(referencia=pago.numero_referencia).first()
        if boleta :
            if not boleta.status:
                boleta.status = True
                boleta.save()
    return 'Cargado'

def boletas_ver():
    bancos_status_true = Banco.objects.filter(status=True)
    for banco in bancos_status_true:
        boleta_pago = Payment.objects.filter(numero_referencia = banco.referencia).first()
        egreso_pago = Egress.objects.filter(numero_referencia = banco.referencia).first()
        seguro_pago = Insurance.objects.filter(numero_referencia = banco.referencia).first()
        ingreso_pago = Income.objects.filter(numero_referencia = banco.referencia).first()
        acreedor_pago = Creditor.objects.filter(numero_referencia = banco.referencia).first()

        if boleta_pago:
            boleta_pago.estado_transaccion = 'COMPLETADO'
            boleta_pago.save()
        
        if egreso_pago:
            egreso_pago.status = True
            egreso_pago.save()

        if seguro_pago:
            seguro_pago.status = True
            seguro_pago.save()
        
        if ingreso_pago:
            ingreso_pago.status = True
            ingreso_pago.save()
        
        if acreedor_pago:
            acreedor_pago.status = True
            acreedor_pago.save()


def ver_cuotas_no_cargadas():
    comparacion.delay()
    
    #comparacion_para_boletas_divididas()

    cargar_boletas_estado()
    #boletas_ver()
    return 'Listo'