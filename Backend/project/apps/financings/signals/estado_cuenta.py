import uuid
from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.dispatch import receiver

# LOOGER
from apps.financings.clases.personality_logs import logger

# MODELOS
from apps.financings.models import AccountStatement, Disbursement, Credit, PaymentPlan

@receiver(post_save, sender=AccountStatement)
def set_numero_referencia_estado_cuenta(sender, instance, created, **kwargs):
    if created:
        if not instance.numero_referencia or instance.numero_referencia == '':
            # Generar un código de referencia único
            referencia = str(uuid.uuid4())[:8]
            while AccountStatement.objects.filter(numero_referencia=referencia).exists():
                referencia = str(uuid.uuid4())[:8]

            # Asignar el código de referencia
            instance.numero_referencia = referencia 
            
            # Guardar la instancia para que los cambios se apliquen
            instance.save()

            # Registrar el evento en los logs
            logger.info('DESDE SIGNALS DE ESTADO DE CUENTA: CARGANDO UN CODIGO DE REFERENCIA')