from rest_framework import generics

# Serializador
from .serializers import NotificationSerializaer

# API
from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response

# Model
from apps.actividades.models import Notification

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializaer
    queryset = Notification.objects.all()

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user, read=False).order_by('-created_at')