from apps.financings.functions_payment import generar
from celery import shared_task

from apps.financings.functions import realizar_pago
# MODELOS
from apps.financings.models import Payment, Banco
from apps.accountings.models import Income, Egress
from django.shortcuts import get_object_or_404
from datetime import datetime

import re

@shared_task
def comparacion():
    generar()

@shared_task
def comparacion_para_boletas_divididas():
    try:
        # Filtrar pagos con referencias que terminan en "-D" o "-d"
        payments_with_d = Payment.objects.filter(numero_referencia__iendswith="-D", estado_transaccion="PENDIENTE")

        if payments_with_d is None:
            print('Sin encontrar')
            return

        for boletas_divididas in payments_with_d:
            referencia_sin_d = boletas_divididas.numero_referencia[:-2]

            boleta = Banco.objects.filter(referencia = referencia_sin_d).first()

            if boleta is None:
                continue

            cambiar_estado = False

            if boletas_divididas.fecha_emision.date() != boleta.fecha:
                cambiar_estado = True
                boletas_divididas.fecha_emision = boleta.fecha
                
            if boletas_divididas.estado_transaccion in ["PENDIENTE", "Pendiente"]:
               
                ingreso = Income.objects.filter(numero_referencia=boleta.referencia).first()
                egreso = Egress.objects.filter(numero_referencia=boleta.referencia).first()

                if ingreso:
                    ingreso.status = True
                    ingreso.save()
                    boletas_divididas.estado_transaccion = 'COMPLETADO'
                    
                
                if egreso:
                    egreso.status = True
                    egreso.save()
                    boletas_divididas.estado_transaccion = 'COMPLETADO'

                if boletas_divididas.tipo_pago == "EGRESO" or boletas_divididas.tipo_pago == "INGRESO": 
                    boletas_divididas.estado_transaccion = "COMPLETADO"
                    
                if boletas_divididas.credit or boletas_divididas.disbursement or boletas_divididas.cliente or boletas_divididas.acreedor or boletas_divididas.seguro:

                    print('procesando al estado de cuenta')
                    print(boleta.referencia)
                    if cambiar_estado:
                        boletas_divididas.save()
                    realizar_pago(boletas_divididas)


    except Exception as e:
        print(f'Error en funciones de boletas divididas: {e}')