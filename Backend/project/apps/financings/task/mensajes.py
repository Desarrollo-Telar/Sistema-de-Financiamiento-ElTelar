
from celery import shared_task

from apps.financings.models import PaymentPlan, Payment, Recibo,AccountStatement, Credit

# EMAILS
from project.send_mail import send_email_alert, send_email_recibo
from django.shortcuts import render, get_object_or_404, redirect

import logging
logger = logging.getLogger(__name__)






@shared_task
def envio_mensaje_alerta(mensaje, estado, modelo=None):
    logger.info('ENVIANDO MENSAJE...')
    
    pago = Payment.objects.filter(id=modelo).first()
    
    
    send_email_alert(mensaje, estado, pago)

@shared_task
def envio_mensaje_alerta_recibo( modelo):
    try:
        pago = get_object_or_404(Recibo, id=modelo)
    except Recibo.DoesNotExist:
        logger.error(f'No se encontró el objeto Recibo con ID {modelo}')
        return
    send_email_recibo(pago)