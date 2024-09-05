from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

# MODELOS
from .models import Payment, AccountStatement, Credit, PaymentPlan

# FUNCIONALIDADES
from .functions import realizar_pago

""" 
@receiver(post_save, sender=Payment)
def registrar_pago_en_estado_de_cuenta(sender, instance, created, **kwargs):
    
    if created:
        realizar_pago(instance.credit, instance.fecha_emision, instance.monto, instance)

"""