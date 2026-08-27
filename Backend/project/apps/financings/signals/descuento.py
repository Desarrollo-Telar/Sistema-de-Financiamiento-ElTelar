from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.financings.models import Descuento, AccountStatement
from scripts.conversion_datos import model_to_dict

@receiver(post_save, sender=Descuento)
def marcar_estado_cuenta(sender, instance, created, **kwargs):
    if not created:
        return

    with transaction.atomic():
        # 1. Desactivar otros descuentos del crédito
        Descuento.objects.filter(credit=instance.credit).exclude(id=instance.id).update(activo=False)

        cuota = instance.cuota

        # 2. Tomar SNAPSHOT del estado ORIGINAL de la cuota usando tu model_to_dict
        #    (Pasamos la instancia directamente, no hace falta volver a consultar a la BD con .get())
        data_cuota_original = model_to_dict(cuota)

        # 3. Guardar snapshot en el registro de Descuento
        Descuento.objects.filter(id=instance.id).update(data_cuota=data_cuota_original)

        # 4. Calcular diferencias para el Estado de Cuenta
        mora = -instance.mora_por_cobrar if cuota.mora != instance.mora_por_cobrar else 0
        interes = -instance.interes_por_cobrar if cuota.interest != instance.interes_por_cobrar else 0

        # 5. Registrar en Estado de Cuenta
        AccountStatement.objects.create(
            credit=instance.credit,
            cuota=cuota,
            numero_referencia=instance.numero_referencia,
            description=f"Descuento aplicado: {instance.tipo_descuento}\nPor: {instance.usuario_descuento.username}",
            saldo_pendiente=instance.saldo_capital_por_cobrar,
            late_fee_paid=mora,
            interest_paid=interes
        )

        # 6. Actualizar la cuota con los montos con descuento
        cuota.saldo_pendiente = instance.saldo_capital_por_cobrar
        cuota.mora = instance.mora_por_cobrar  
        cuota.interest = instance.interes_por_cobrar
        cuota.save(update_fields=['saldo_pendiente', 'mora', 'interest'])