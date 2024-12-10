from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.dispatch import receiver

# MODELOS
from apps.financings.models import Banco

# ENVIO DE EMAIL
from apps.financings.task import envio_mensaje_alerta, envio_mensaje_alerta_recibo,comparacion

@receiver(post_save, sender=Banco)
def generar_comparacion(sender, instance, created, **kwargs):
    if created:
        comparacion()