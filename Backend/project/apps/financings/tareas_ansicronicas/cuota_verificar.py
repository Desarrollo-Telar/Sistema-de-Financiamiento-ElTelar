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

def ver_caso_de_gastos():
    print('viendo')
    gastos = Egress.objects.filter(status=False)

    for gasto in gastos:
        numero_referencia = gasto.numero_referencia

        boleta = Payment.objects.filter(numero_referencia=numero_referencia).first()
        banco = Banco.objects.filter(referencia = numero_referencia).first()

        if boleta is not None:
            
            print(f'BOLETA: {boleta},Estado de la boleta: {boleta.estado_transaccion}, Gatos: {gasto.numero_referencia}, Banco: {banco}, Estado en banco: {banco.status}')
            
            if boleta.estado_transaccion == 'COMPLETADO' and banco.status:
                gasto.status = True
                gasto.save()

            if boleta.estado_transaccion == 'PENDIENTE' and banco.status:
                boleta.estado_transaccion = 'COMPLETADO'
                boleta.save()

            if boleta.estado_transaccion == 'COMPLETADO' and banco.status == False:
                banco.status = True
                banco.save()
        
        else:
            boletas = Payment(
                    fecha_emision=gasto.fecha,
                    numero_referencia=numero_referencia,
                    tipo_pago='EGRESO', 
                    boleta = gasto.boleta,
                    monto=gasto.monto,
                    descripcion=gasto.observaciones
                    )  
            boletas.save()
            print('se creo una boleta')




def cargar_boletas_estado():
    pagos_estado_completado = Payment.objects.filter(estado_transaccion = "COMPLETADO")
    for pago in pagos_estado_completado:
        boleta = Banco.objects.filter(referencia=pago.numero_referencia).first()
        if boleta :
            if not boleta.status:
                boleta.status = True
                boleta.save()
    return 'Cargado'

def boletas_ver(estado):
    bancos_status_true = Banco.objects.filter(status=estado)
    for banco in bancos_status_true:
        boleta_pago = Payment.objects.filter(numero_referencia = banco.referencia).first()
        egreso_pago = Egress.objects.filter(numero_referencia = banco.referencia).first()
        seguro_pago = Insurance.objects.filter(numero_referencia = banco.referencia).first()
        ingreso_pago = Income.objects.filter(numero_referencia = banco.referencia).first()
        acreedor_pago = Creditor.objects.filter(numero_referencia = banco.referencia).first()

        if boleta_pago:
            if boleta_pago.estado_transaccion != 'COMPLETADO':
                boleta_pago.estado_transaccion = 'COMPLETADO'
                boleta_pago.save()
            banco.status = True
            banco.save()
        
        if egreso_pago:
            if not egreso_pago.status:
                egreso_pago.status = True
                egreso_pago.save()
            banco.status = True
            banco.save()

        if seguro_pago:
            if not seguro_pago.status:
                seguro_pago.status = True
                seguro_pago.save()
            banco.status = True
            banco.save()
        
        if ingreso_pago:
            if not ingreso_pago.status:
                ingreso_pago.status = True
                ingreso_pago.save()
            banco.status = True
            banco.save()
        
        if acreedor_pago:
            if not acreedor_pago.status:
                acreedor_pago.status = True
                acreedor_pago.save()
            banco.status = True
            banco.save()

from django.db import transaction

def ver_cuotas_no_cargadas():
    try:
        with transaction.atomic():
            comparacion()
            
            comparacion_para_boletas_divididas()

            cargar_boletas_estado()
            boletas_ver(True)
            boletas_ver(False)
            return 'Listo'
    except Exception as e:
        print(f'ERROR: {e}')