# Serializador
from rest_framework import serializers

# Models
from apps.actividades.models import Notification

import locale
from django.utils.timezone import localtime

class NotificationSerializaer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
    
    def to_representation(self, instance):
         # Asegúrate de que la fecha esté en tu zona horaria local
        fecha = localtime(instance.created_at)

        # Formato personalizado: 8 de julio de 2025 a las 11:15
        meses = [
            "enero", "febrero", "marzo", "abril", "mayo", "junio",
            "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
        ]
        fecha_formateada = f"{fecha.day} de {meses[fecha.month - 1]} de {fecha.year} a las {fecha.strftime('%H:%M')}"

        return {
            'id':instance.id,
            'title':instance.title,
            "message": instance.message,
            'created_at': fecha_formateada,
            "read": instance.read,
            "user": instance.user.id,
            'especificaciones':instance.especificaciones,
            'uuid':instance.uuid
        }