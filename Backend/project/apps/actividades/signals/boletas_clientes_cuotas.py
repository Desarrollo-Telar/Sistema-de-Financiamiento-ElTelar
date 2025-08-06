# Modelo
from apps.actividades.models import DocumentoNotificacionCliente

# signals
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from project.database_store import minio_client  # asegúrate de que esté importado correctamente

@receiver(post_save, sender=DocumentoNotificacionCliente)
def send_message_status_boleta(sender, instance, created, **kwargs):

    if not created:
        if instance.status == False:
            print('mandar mensaje al cliente')

        if instance.status == True:
            print("Eliminar este registro")





@receiver(post_delete, sender=DocumentoNotificacionCliente)
def eliminar_documento_minio(sender, instance, **kwargs):
    if instance.document:
        try:
            minio_client.remove_object("asiatrip", instance.document.name)
            print(f"Archivo eliminado: {instance.document.name}")
        except Exception as e:
            print(f"Error al eliminar el archivo: {e}")
