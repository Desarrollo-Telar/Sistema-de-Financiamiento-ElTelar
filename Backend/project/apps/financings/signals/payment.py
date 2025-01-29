from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.dispatch import receiver

# MODELOS
from apps.financings.models import Payment


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
        comparacion()
        


# ENVIO DE ALERTA PARA EL ESTATUS DE LA BOLETA
@receiver(post_save, sender=Payment)
def alerta(sender, instance, **kwargs):
    if instance.estado_transaccion == 'FALLIDO':
        logger.info('DESDE SIGNALS PAYMENT: ENVIANDO MENSAJE')
        #envio_mensaje_alerta(instance.descripcion_estado, 'FALLIDO',instance.id)
    elif instance.estado_transaccion == 'COMPLETADO':
        logger.info('DESDE SIGNALS PAYMENT: ENVIANDO MENSAJE')
        #envio_mensaje_alerta(instance.descripcion_estado, 'COMPLETADO',instance.id)
    elif instance.estado_transaccion == 'PENDIENTE':
        #comparacion()
        logger.info('DESDE SIGNALS PAYMENT: ENVIANDO MENSAJE')
        #envio_mensaje_alerta('HAY UNA BOLETA DE PAGO CON ESTADO PENDIENTE', 'PENDIENTE',instance.id)


#JKDSJAKDJSA
