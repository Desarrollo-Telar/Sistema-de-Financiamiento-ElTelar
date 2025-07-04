# Serializador
from rest_framework import serializers

# Models
from apps.actividades.models import Notification

class NotificationSerializaer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
    
    def to_representation(self, instance):
        return {
            'id':instance.id,
            'title':instance.title,
            "message": instance.message,
            "created_at": instance.created_at.date(),
            "read": instance.read,
            "user": instance.user.id,
            'especificaciones':instance.especificaciones,
            'uuid':instance.uuid
        }