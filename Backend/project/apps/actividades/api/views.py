from rest_framework import generics


# Model
from apps.actividades.models import Notification, DetalleInformeCobranza, Informe

# Serializador
from .serializers import NotificationSerializaer, DetalleInformeCobranzaSerializer

# API
from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response



class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializaer
    queryset = Notification.objects.all()

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user, read=False).order_by('-created_at')

class DetalleInformeCobranzaViewSet(viewsets.ModelViewSet):
    serializer_class = DetalleInformeCobranzaSerializer

    def get_queryset(self):
        # Filtrar informes del usuario actual
        informes = Informe.objects.filter(usuario=self.request.user)
        if not informes.exists():
            return DetalleInformeCobranza.objects.none()

        # Si viene parámetro 'reporte'
        reporte_id = self.request.query_params.get('reporte', '').strip()
        if reporte_id:
            informe = informes.filter(id=reporte_id).first()
            if not informe:
                return DetalleInformeCobranza.objects.none()
            return DetalleInformeCobranza.objects.filter(reporte=informe)

        # Si no hay reporte específico, devolver todos los detalles de los informes del usuario
        return DetalleInformeCobranza.objects.filter(reporte__in=informes)


