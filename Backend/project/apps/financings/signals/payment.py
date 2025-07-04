from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.dispatch import receiver

# MODELOS
from apps.financings.models import Payment, Banco


# LOOGER
from apps.financings.clases.personality_logs import logger


# ENVIO DE EMAIL
from apps.financings.task import envio_mensaje_alerta, envio_mensaje_alerta_recibo,comparacion, comparacion_para_boletas_divididas

# REVISION
from apps.financings.functions_payment import revisar

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
            boleta = Banco.objects.filter(referencia = instance.numero_referencia).first()
            if boleta:
                revisar(boleta)


        

@receiver(post_save, sender=Payment)
def alerta(sender, instance, **kwargs):
    banco = None
    referencia_sin_d = None
    

    # Si la referencia termina en -D o -d
    if instance.numero_referencia.endswith(("-D", "-d")):
        referencia_sin_d = instance.numero_referencia[:-2]
        banco = Banco.objects.filter(referencia = referencia_sin_d).first()
     
    else:
        banco = Banco.objects.filter(referencia = instance.numero_referencia).first()

    if instance.estado_transaccion == 'FALLIDO':
        logger.info('DESDE SIGNALS PAYMENT: ENVIANDO MENSAJE')
        if banco:
            banco.status = False
            banco.save()
        # envio_mensaje_alerta(instance.descripcion_estado, 'FALLIDO', instance.id)
        
    if instance.estado_transaccion == 'PENDIENTE':
        logger.info('DESDE SIGNALS PAYMENT: ENVIANDO MENSAJE')
        envio_mensaje_alerta('Por favor, asegúrense de revisar los detalles de la boleta de pago pendiente y tomar cualquier acción necesaria.Saludos cordiales,', 'PENDIENTE', instance.id)

    if instance.estado_transaccion == 'COMPLETADO':
        logger.info('DESDE SIGNALS PAYMENT: ENVIANDO MENSAJE - COMPLETADO')
        
        if banco:
            banco.status = True
            banco.save()

        if instance.numero_referencia.endswith(("-D", "-d")):
            contador = 0
            listado = Payment.objects.filter(numero_referencia__regex=rf"^{referencia_sin_d}-D\d*$")
            
            for lista in listado:
                contador += 1
            
            instance.numero_referencia = f'{referencia_sin_d}-D{contador}'
            instance.save()
            

        envio_mensaje_alerta( 
                             '''La boleta de pago ha sido procesada exitosamente. No se requiere ninguna acción adicional. Saludos cordiales,''', 
                             'COMPLETADO',instance.id)

    