from django.db import models

# Relacion
from apps.users.models import User
from apps.customers.models import Customer
from apps.financings.models import PaymentPlan

# UUID
import uuid

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

    def __str__(self):
        return f'{self.status}'
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Documento de Boleta de Cliente'
        verbose_name_plural = 'Documentos de Boletas de Clientes'