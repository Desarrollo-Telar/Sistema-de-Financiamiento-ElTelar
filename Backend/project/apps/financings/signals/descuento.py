from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.dispatch import receiver

# MODELOS
from apps.financings.models import Descuento, PaymentPlan, AccountStatement


@receiver(post_save, sender=Descuento)
def marcar_estado_cuenta(sender, instance, created, **kwargs):
    if created:
        Descuento.objects.filter(credit=instance.credit).exclude(id=instance.id).update(activo=False)
        # Obtener la cuota asociada al descuento
        cuota = instance.cuota
        mora = 0
        interes = 0

        if cuota.mora != instance.mora_por_cobrar:
            mora = -instance.mora_por_cobrar

        if cuota.interest != instance.interes_por_cobrar:
            interes = - instance.interes_por_cobrar


        
        AccountStatement.objects.create(
            credit= instance.credit,
            cuota=cuota,
            numero_referencia=instance.numero_referencia,
            description=f"Descuento aplicado: {instance.tipo_descuento}",
            saldo_pendiente= instance.saldo_capital_por_cobrar,
            late_fee_paid = mora,
            interest_paid = interes
        )

        cuota.saldo_pendiente = instance.saldo_capital_por_cobrar
        cuota.mora = instance.mora_por_cobrar  
        cuota.interest = instance.interes_por_cobrar
        cuota.save()
