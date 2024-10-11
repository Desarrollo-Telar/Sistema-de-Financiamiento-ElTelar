from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.dispatch import receiver

# MODELOS
from apps.financings.models import AccountStatement, Disbursement


import uuid
from django.db import transaction, IntegrityError


# EL DESEMBOLSO REALIZADO SE REFLEJA EN EL ESTADO DE CUENTAS DEL CLIENTE
@receiver(post_save, sender=Disbursement)
def reflejar_estado_cuenta(sender, instance, created, **kwargs):
    if created:
        desembolso_credito = Disbursement.objects.filter(
            credit_id_id=instance.credit_id.id, 
            forma_desembolso='APLICACIÓN GASTOS'
        )

        if desembolso_credito.count() > 1:
            instance.delete()
        else:
            referencia = str(uuid.uuid4())[:8]
            
            # Usar una transacción atómica para asegurar la consistencia
            with transaction.atomic():
                estado_cuenta = AccountStatement(
                    credit=instance.credit_id,
                    disbursement=instance,
                    disbursement_paid=instance.monto_total_desembolso,
                    numero_referencia=referencia,
                    description=f'{instance.forma_desembolso}'
                )

                try:
                    estado_cuenta.save()
                except IntegrityError:
                    # En caso de colisión, generar una nueva referencia y volver a intentar
                    referencia = str(uuid.uuid4())[:8]
                    estado_cuenta.numero_referencia = referencia
                    estado_cuenta.save()


