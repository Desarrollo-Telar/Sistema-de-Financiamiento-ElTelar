from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.dispatch import receiver

# MODELOS
from apps.financings.models import Payment, Banco


# LOOGER
from apps.financings.clases.personality_logs import logger


# ENVIO DE EMAIL
from apps.financings.task import envio_mensaje_alerta, envio_mensaje_alerta_recibo,comparacion

from project.settings import MEDIA_URL, STATIC_URL
from project.settings import MEDIA_ROOT
import os

# Señales


@receiver(post_save, sender=Payment)
def generar_plan_pagos(sender, instance, created, **kwargs):
    if created:
        if instance.cliente is not None:
            Payment.objects.filter(id=instance.id).update(tipo_pago='CLIENTE')
        comparacion()


        


# ENVIO DE ALERTA PARA EL ESTATUS DE LA BOLETA
@receiver(post_save, sender=Payment)
def alerta(sender, instance, **kwargs):
    banco = Banco.objects.filter(referencia = instance.numero_referencia).first()
    if instance.estado_transaccion == 'FALLIDO':
        logger.info('DESDE SIGNALS PAYMENT: ENVIANDO MENSAJE')
        banco.status = False
        banco.save()
        #envio_mensaje_alerta(instance.descripcion_estado, 'FALLIDO',instance.id)
    elif instance.estado_transaccion == 'COMPLETADO':
        logger.info('DESDE SIGNALS PAYMENT: ENVIANDO MENSAJE')
        
        banco.status = True
        banco.save()
        #envio_mensaje_alerta(instance.descripcion_estado, 'COMPLETADO',instance.id)
    elif instance.estado_transaccion == 'PENDIENTE':
        #comparacion()
        logger.info('DESDE SIGNALS PAYMENT: ENVIANDO MENSAJE')
        #envio_mensaje_alerta('HAY UNA BOLETA DE PAGO CON ESTADO PENDIENTE', 'PENDIENTE',instance.id)


#JKDSJAKDJSA
