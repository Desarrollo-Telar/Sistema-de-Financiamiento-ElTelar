from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.dispatch import receiver

# MODELOS
from apps.financings.models import Payment, Banco


# LOOGER
from apps.financings.clases.personality_logs import logger


# ENVIO DE EMAIL
from apps.financings.task import envio_mensaje_alerta, envio_mensaje_alerta_recibo,comparacion, comparacion_para_boletas_divididas

from project.settings import MEDIA_URL, STATIC_URL
from project.settings import MEDIA_ROOT
import os
import re

# Señales


@receiver(post_save, sender=Payment)
def generar_plan_pagos(sender, instance, created, **kwargs):
    if created:
        if instance.cliente is not None:
            Payment.objects.filter(id=instance.id).update(tipo_pago='CLIENTE')
        
        if instance.numero_referencia.endswith(("-D", "-d")):
            comparacion_para_boletas_divididas()
        else:
            comparacion()


        

@receiver(post_save, sender=Payment)
def alerta(sender, instance, **kwargs):
    banco = None
    referencia_sin_d = None

    # Si la referencia termina en -D o -d
    if re.match(r".*-D\d*$", instance.numero_referencia, re.IGNORECASE):
        referencia_sin_d = re.sub(r"-D\d*$", "", instance.numero_referencia, flags=re.IGNORECASE)
        banco = Banco.objects.filter(referencia=referencia_sin_d).first()

        pago_completados = Payment.objects.filter(numero_referencia__regex=rf"^{referencia_sin_d}(-D\d*)?$")
        monto_total = sum(pago.monto for pago in pago_completados)

        if banco and monto_total > (banco.credito or 0):
            instance.estado_transaccion = 'FALLIDO'
            instance.descripcion_estado = "ESTA BOLETA EXCEDE EL MONTO TOTAL DE TODAS LAS BOLETAS DIVIDAS CON RESPECTO A LA BOLETA ORIGINAL"
            instance.save()

    else:
        banco = Banco.objects.filter(referencia=instance.numero_referencia).first()

    if instance.estado_transaccion == 'FALLIDO':
        logger.info('DESDE SIGNALS PAYMENT: ENVIANDO MENSAJE')
        if banco:
            banco.status = False
            banco.save()
        # envio_mensaje_alerta(instance.descripcion_estado, 'FALLIDO', instance.id)

    elif instance.estado_transaccion == 'COMPLETADO':
        logger.info('DESDE SIGNALS PAYMENT: ENVIANDO MENSAJE')
        if banco:
            banco.status = True
            banco.save()

        if referencia_sin_d:
            contador = Payment.objects.filter(numero_referencia__regex=rf"^{referencia_sin_d}-D\d*$").count()
            instance.numero_referencia = f'{referencia_sin_d}-D{contador+1}'
            instance.save()

        # envio_mensaje_alerta(instance.descripcion_estado, 'COMPLETADO', instance.id)

    elif instance.estado_transaccion == 'PENDIENTE':
        logger.info('DESDE SIGNALS PAYMENT: ENVIANDO MENSAJE')
        # envio_mensaje_alerta('HAY UNA BOLETA DE PAGO CON ESTADO PENDIENTE', 'PENDIENTE', instance.id)