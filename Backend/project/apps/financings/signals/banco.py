from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.dispatch import receiver

# MODELOS
from apps.financings.models import Banco

from apps.accountings.models import Creditor, Insurance, Income, Egress

# ENVIO DE EMAIL
from apps.financings.task import envio_mensaje_alerta, envio_mensaje_alerta_recibo,comparacion

@receiver(post_save, sender=Banco)
def generar_comparacion(sender, instance, created, **kwargs):
    if created:
        comparacion()

    if instance.status:
        egreso_pago = Egress.objects.filter(numero_referencia = instance.referencia).first()
        seguro_pago = Insurance.objects.filter(numero_referencia = instance.referencia).first()
        ingreso_pago = Income.objects.filter(numero_referencia = instance.referencia).first()
        acreedor_pago = Creditor.objects.filter(numero_referencia = instance.referencia).first()

        if egreso_pago:
            egreso_pago.status = True
            egreso_pago.save()

        if seguro_pago:
            seguro_pago.status = True
            seguro_pago.save()
        
        if ingreso_pago:
            ingreso_pago.status = True
            ingreso_pago.save()
        
        if acreedor_pago:
            acreedor_pago.status = True
            acreedor_pago.save()


