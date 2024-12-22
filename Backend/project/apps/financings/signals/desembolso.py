from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.dispatch import receiver

# MODELOS
from apps.financings.models import AccountStatement, Disbursement


import uuid


# EL DESEMBOLSO REALIZADO SE REFLEJA EN EL ESTADO DE CUENTAS DEL CLIENTE
@receiver(post_save, sender=Disbursement)
def reflejar_estado_cuenta(sender, instance, created, **kwargs):
    if created:
        referencia = str(uuid.uuid4())[:8]
        
        # Si `numero_referencia` es único, manejamos colisión con try/except
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


