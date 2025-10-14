# Modelo
from apps.actividades.models import DocumentoNotificacionCliente
from apps.financings.models import Banco, Payment

# signals
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from project.database_store import minio_client  # asegúrate de que esté importado correctamente

# tiempo
from datetime import datetime
from django.utils import timezone

@receiver(post_save, sender=DocumentoNotificacionCliente)
def send_message_status_boleta(sender, instance, created, **kwargs):
    if not created:
        if instance.status is False:
            print('mandar mensaje al cliente')

        if instance.status is True:
            print('Guardando')
            if instance.numero_referencia is None:
                return

            if instance.numero_referencia == '3696008759':
                return

            banco = Banco.objects.filter(referencia=instance.numero_referencia).first()

            monto_pago = banco.credito if banco else 0
            fecha_emision = banco.fecha if banco else timezone.now()

            pago = Payment.objects.filter(numero_referencia=instance.numero_referencia).first()

            if pago is not None:
                return

            # Crear el pago y copiar el documento como boleta
            pago = Payment.objects.create(
                credit=instance.cuota.credit_id,
                monto=monto_pago,
                fecha_emision=fecha_emision,
                numero_referencia=instance.numero_referencia,
                descripcion=instance.description,
                boleta=instance.document,  
                sucursal = instance.sucursal
            )

            print(pago)






@receiver(post_delete, sender=DocumentoNotificacionCliente)
def eliminar_documento_minio(sender, instance, **kwargs):
    if instance.document:
        try:
            minio_client.remove_object("asiatrip", instance.document.name)
            print(f"Archivo eliminado: {instance.document.name}")
        except Exception as e:
            print(f"Error al eliminar el archivo: {e}")
