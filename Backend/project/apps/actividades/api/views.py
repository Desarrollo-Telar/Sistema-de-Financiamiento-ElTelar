from rest_framework import generics


# Model
from apps.actividades.models import Notification, DetalleInformeCobranza, Informe

# Serializador
from .serializers import NotificationSerializaer, DetalleInformeCobranzaSerializer

# API
from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination

class NotificationPagination(PageNumberPagination):
    page_size = 10  # Solo trae las 10 más recientes por petición

class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationSerializaer
    pagination_class = NotificationPagination

    def get_queryset(self):
        # Muestra solo las no leídas del usuario autenticado
        return Notification.objects.filter(
            user=self.request.user, 
            read=False
        ).order_by('-created_at')

    # Endpoint ultraligero solo para el badge/conteo
    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        # .count() ejecuta un 'SELECT COUNT(*)' directo en BD sin cargar objetos a la RAM
        count = self.get_queryset().count()
        return Response({'unread_count': count})

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
            informe = Informe.objects.filter(id=reporte_id).first()
            if not informe:
                return DetalleInformeCobranza.objects.none()
            return DetalleInformeCobranza.objects.filter(reporte=informe)

        # Si no hay reporte específico, devolver todos los detalles de los informes del usuario
        return DetalleInformeCobranza.objects.filter(reporte__in=informes)

class DetalleInformeCobranzaPorcentajesViewSet(viewsets.ModelViewSet):
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
            return DetalleInformeCobranza.objects.filter(reporte=informe).order_by('-id').first()

        # Si no hay reporte específico, devolver todos los detalles de los informes del usuario
        return DetalleInformeCobranza.objects.filter(reporte__in=informes).order_by('-id').first()
