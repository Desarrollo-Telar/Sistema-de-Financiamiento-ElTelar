# models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.core.serializers import serialize, deserialize
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
import json

from apps.users.models import User

class ModelHistory(models.Model):
    ACTION_CHOICES = [
        ('create', 'Creación'),
        ('update', 'Actualización'),
        ('delete', 'Eliminación'),
    ]

    content_type = models.CharField(max_length=255)  # Nombre del modelo
    object_id = models.PositiveIntegerField()        # ID del objeto
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    data = models.JSONField()                        # Datos serializados del objeto
    changes = models.JSONField(null=True, blank=True)  # Campos modificados (solo para updates)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
        ]

    def __str__(self):
        return f"{self.content_type} #{self.object_id} - {self.action} - {self.timestamp}"

    def get_object_instance(self):
        """Devuelve una instancia del objeto a partir de los datos serializados"""
        from django.apps import apps
        model = apps.get_model(self.content_type)
        # Crear una instancia con los datos históricos
        instance = model(**self.data)
        instance.pk = self.object_id
        return instance

    def restore(self):
        """Restaura esta versión del objeto"""
        from django.apps import apps
        model = apps.get_model(self.content_type)
        instance = self.get_object_instance()
        instance.save()
        return instance