from django.db import models

# Relacion
from apps.users.models import User
from apps.customers.models import Customer
from apps.financings.models import PaymentPlan, Payment
from apps.subsidiaries.models import Subsidiary

# UUID
import uuid

# TIEMPO
from datetime import datetime

from project.settings import MEDIA_URL, STATIC_URL

#
from datetime import timedelta
from project.database_store import minio_client  # asegúrate de que esté importado correctamente

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications", verbose_name="Para")
    title = models.CharField(max_length=255, verbose_name="Titulo")
    message = models.TextField(verbose_name="Mensaje", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    especificaciones = models.JSONField("Especificaciones", blank=True, null=True)
    read = models.BooleanField(default=False)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Notificacion'
        verbose_name_plural = 'Notificaciones'

    def __str__(self):
        return f"Notificación para {self.user.username}: {self.title}"

class NotificationCustomer(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="NotificationCustomer", verbose_name="Realizado por", blank=True, null=True)
    cliente = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="NotificationCustomer", verbose_name="Para", blank=True, null=True)
    cuota = models.ForeignKey(PaymentPlan, on_delete=models.CASCADE, related_name="NotificationCustomer", verbose_name="Cuota", blank=True, null=True)

    title = models.CharField(max_length=255, verbose_name="Titulo")
    message = models.TextField(verbose_name="Mensaje", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Notificacion para Cliente'
        verbose_name_plural = 'Notificaciones de Clientes'

    def __str__(self):
        return f"Notificación para {self.user.username}: {self.title}"

class DocumentoNotificacionCliente(models.Model):
    status = models.BooleanField( blank=True, null=True)
    cliente = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="DocumentoNotificacionCliente", verbose_name="Para", blank=True, null=True)
    cuota = models.ForeignKey(PaymentPlan, on_delete=models.CASCADE, related_name="DocumentoNotificacionCliente", verbose_name="Cuota", blank=True, null=True)
    document = models.FileField("Documento", upload_to='documents/boleta/cliente')
    description = models.TextField("Descripción",blank=True, null=True)
    created_at = models.DateTimeField("Fecha de Creación", auto_now_add=True)
    numero_referencia = models.CharField('Numero de Referencia', max_length=255, null=True, blank=True, default='3696008759')
    fecha_actualizacion = models.DateField("Fecha en que se actualizo el credito", default=datetime.now, null=True, blank=True)
    sucursal = models.ForeignKey(Subsidiary, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{self.status}'
    
    def fecha_de_emision_boleta(self):
        pago = Payment.objects.filter(numero_referencia=self.numero_referencia).first()
        
        if pago is not None:
            return pago.fechaEmision()
        
        return self.created_at
    
    def get_document(self):
        try:
            return minio_client.presigned_get_object(
                bucket_name='asiatrip',
                object_name=self.document.name,  # ejemplo: documents/archivo.pdf
                expires=timedelta(minutes=30)

            )
        except Exception as e:
            return '{}{}'.format(MEDIA_URL,self.document)
        
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Documento de Boleta de Cliente'
        verbose_name_plural = 'Documentos de Boletas de Clientes'