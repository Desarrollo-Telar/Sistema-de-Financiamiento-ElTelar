from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.dispatch import receiver

# MODELOS
from apps.financings.models import  Recibo

# LOOGER
from apps.financings.clases.personality_logs import logger

# ENVIO DE EMAIL
from apps.financings.task import envio_mensaje_alerta, envio_mensaje_alerta_recibo,comparacion

# GENERACION DE NUMEROS DE RECIBO
@receiver(pre_save, sender=Recibo)
def generar_noRecibo(sender, instance, **kwargs):
    if not instance.recibo or instance.recibo == 0:
        counter = 1
        while Recibo.objects.filter(recibo=counter).exists():
            counter += 1

        instance.recibo = counter
    # ENVIAR MENSAJES AL CLIENTE, ADMINISTRADORES Y SECRETARIA
    #envio_mensaje_alerta_recibo(instance.id)
    logger.info('DESDE SIGNALS DE RECIBO: ENVIO DE MENSAJE DE RECIBO CARGADO')





