from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

# MODELOS
from apps.financings.models import (
    Descuento,
    PaymentPlan,
    AccountStatement,
)

from scripts.conversion_datos import model_to_dict


@receiver(post_save, sender=Descuento)
def marcar_estado_cuenta(sender, instance, created, **kwargs):

    # Solo ejecutar la lógica cuando el descuento
    # se está creando por primera vez.
    if not created:
        return

    with transaction.atomic():

        # ---------------------------------------------------------
        # 1. Desactivar descuentos anteriores del mismo crédito
        # ---------------------------------------------------------
        Descuento.objects.filter(
            credit=instance.credit
        ).exclude(
            pk=instance.pk
        ).update(
            activo=False
        )

        # ---------------------------------------------------------
        # 2. Obtener la cuota asociada
        # ---------------------------------------------------------
        cuota = instance.cuota

        # ---------------------------------------------------------
        # 3. Guardar una copia del estado de la cuota
        #    antes de aplicar el descuento
        # ---------------------------------------------------------
        data_cuota = model_to_dict(cuota)

        instance.data_cuota = data_cuota

        # Guardamos solamente data_cuota.
        # Este save volverá a disparar post_save, pero como
        # created=False, el signal terminará inmediatamente.
        instance.save(
            update_fields=["data_cuota"]
        )

        # ---------------------------------------------------------
        # 4. Calcular los valores del descuento
        # ---------------------------------------------------------

        # Valor de mora que se está descontando
        mora = 0

        # Valor de interés que se está descontando
        interes = 0

        if cuota.mora != instance.mora_por_cobrar:
            mora = cuota.mora - instance.mora_por_cobrar

        if cuota.interest != instance.interes_por_cobrar:
            interes = cuota.interest - instance.interes_por_cobrar

        # ---------------------------------------------------------
        # 5. Crear el movimiento en el estado de cuenta
        # ---------------------------------------------------------
        AccountStatement.objects.create(
            credit=instance.credit,
            cuota=cuota,
            numero_referencia=instance.numero_referencia,
            description=f"Descuento aplicado: {instance.tipo_descuento}",
            saldo_pendiente=instance.saldo_capital_por_cobrar,
            late_fee_paid=-mora,
            interest_paid=-interes,
        )

        # ---------------------------------------------------------
        # 6. Actualizar la cuota con los nuevos valores
        # ---------------------------------------------------------
        cuota.saldo_pendiente = instance.saldo_capital_por_cobrar
        cuota.mora = instance.mora_por_cobrar
        cuota.interest = instance.interes_por_cobrar

        cuota.save(
            update_fields=[
                "saldo_pendiente",
                "mora",
                "interest",
            ]
        )