from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.dispatch import receiver

# MODELOS
from apps.financings.models import  Invoice

# LOOGER
from apps.financings.clases.personality_logs import logger

# ENVIO DE EMAIL
from apps.financings.task import envio_mensaje_alerta, envio_mensaje_alerta_recibo,comparacion

# GENERACION DE NUMEROS DE RECIBO
@receiver(pre_save, sender=Invoice)
def generar_noFactura(sender, instance, **kwargs):
    if not instance.numero_factura or instance.numero_factura == 0:
        counter = 1
        while Invoice.objects.filter(numero_factura=counter).exists():
            counter += 1

        instance.numero_factura = counter
    # ENVIAR MENSAJES AL CLIENTE, ADMINISTRADORES Y SECRETARIA
    #envio_mensaje_alerta_recibo(instance.id)
    logger.info('DESDE SIGNALS DE FACUTRA: ENVIO DE MENSAJE DE RECIBO CARGADO')

