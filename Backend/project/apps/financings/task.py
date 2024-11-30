from celery import shared_task

# TIEMPO
from datetime import datetime
from time import sleep
# MODELOS
from .models import PaymentPlan, Payment, Recibo,AccountStatement, Credit
from decimal import Decimal
from django.shortcuts import render, get_object_or_404

# CALCULOS
from apps.financings.calculos import calculo_mora, calculo_interes

# EMAILS
from project.send_mail import send_email_alert, send_email_recibo

import logging
logger = logging.getLogger(__name__)

from apps.financings.functions_payment import generar
@shared_task
def comparacion():
    generar()


@shared_task
def envio_mensaje_alerta(mensaje, estado, modelo=None):
    logger.info('ENVIANDO MENSAJE...')
    
    pago = None
    if modelo:
        try:
            pago = get_object_or_404(Payment, id=modelo)
        except Payment.DoesNotExist:
            logger.error(f'No se encontró el objeto Payment con ID {modelo}')
            return
    
    #send_email_alert(mensaje, estado, pago)

@shared_task
def envio_mensaje_alerta_recibo( modelo):
    try:
        pago = get_object_or_404(Recibo, id=modelo)
    except Recibo.DoesNotExist:
        logger.error(f'No se encontró el objeto Recibo con ID {modelo}')
        return
    #send_email_recibo(pago)


@shared_task
def envio_mensaje_alerta(mensaje, estado, modelo=None):
    logger.info('ENVIANDO MENSAJE...')
    
    pago = None
    if modelo:
        try:
            pago = get_object_or_404(Payment, id=modelo)
        except Payment.DoesNotExist:
            logger.error(f'No se encontró el objeto Payment con ID {modelo}')
            return
    
    #send_email_alert(mensaje, estado, pago)

@shared_task
def envio_mensaje_alerta_recibo( modelo):
    try:
        pago = get_object_or_404(Recibo, id=modelo)
    except Recibo.DoesNotExist:
        logger.error(f'No se encontró el objeto Recibo con ID {modelo}')
        return
    #send_email_recibo(pago)


import uuid
from django.db import transaction

@shared_task
def cambiar_plan():
    print("CAMBIANDO")
    
    planes = PaymentPlan.objects.filter(fecha_limite__date=datetime.now().date(), cuota_vencida=False)
    print(planes)
    if planes:
        for pago in planes:
            
            
            
            # Validar si hay algún pago registrado para este crédito y plan
            boleta = Payment.objects.filter(credit=pago.credit_id, id=pago.id )
          
            if not boleta and not pago.credit_id.is_paid_off:
                with transaction.atomic():
                    #pago.status = True     
                    # Calcular la mora acumulada solo si hay atraso (después de 15 días)
                    #mora = calculo_mora(pago.saldo_pendiente, pago.credit_id.tasa_interes)
                    mora = Decimal(pago.interest) * Decimal(0.1)
                    
                    #mora_acumulada = pago.mora + mora
                    if not pago.status:
                        pago.cuota_vencida = True
                    #pago.mora = mora_acumulada   
                    pago.mora = mora
                    interes = calculo_interes(pago.saldo_pendiente,pago.credit_id.tasa_interes)

                    pago.mora_generado = Decimal(interes) * Decimal(0.1)
                
                    

                    pago.save()

                    estado_cuenta = AccountStatement(credit=pago.credit_id,numero_referencia=str(uuid.uuid4())[:8],description="CUOTA VENCIDA",cuota=pago)
                    estado_cuenta.save()


                    
                    interes_acumulado = pago.interest + interes
                
                    
                
                    siguiente_cuota = PaymentPlan.objects.filter(
                        credit_id_id=pago.credit_id.id,  
                        fecha_limite__gt=pago.fecha_limite  # Filtramos por fecha límite
                    ).order_by('fecha_limite').first()
                    

                    if siguiente_cuota:
                        siguiente_cuota.saldo_pendiente =pago.saldo_pendiente
                        siguiente_cuota.credit_id =pago.credit_id
                        siguiente_cuota.start_date =pago.due_date
                        siguiente_cuota.mora =pago.mora
                        siguiente_cuota.outstanding_balance =pago.saldo_pendiente
                        siguiente_cuota.interest =interes_acumulado

                        siguiente_cuota.interes_generado = interes
                        siguiente_cuota.interes_acumulado_generado = pago.interest
                        
                        siguiente_cuota.save()
                    else:
                        # CARGAR UNA NUEVA CUOTA CON POSIBLE ACUMULO DE INTERES Y DE MORA
                        nuevo_plan = PaymentPlan(
                            saldo_pendiente=pago.saldo_pendiente, 
                            credit_id= pago.credit_id, 
                            start_date=pago.due_date,
                            mora=pago.mora, 
                            outstanding_balance=pago.saldo_pendiente,
                            interest=interes_acumulado,
                            interes_generado=interes,
                            interes_acumulado_generado=pago.interest,
                            mora_acumulado_generado=pago.mora,
                            
                            )
                        nuevo_plan.save()