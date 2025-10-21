
# Serializador
from apps.financings.api.serializers import PaymentSerializer

# MODELS
from apps.financings.models import Payment

# API
from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from django.utils.timezone import datetime

from rest_framework.request import Request

# Tiempo
from datetime import datetime, timedelta

# HISTORIAL Y BITACORA
from apps.actividades.utils import log_user_action, log_system_event
from scripts.conversion_datos import model_to_dict, cambios_realizados

class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.query_params.get('term', '')  # Obtener el parámetro 'term'
        sucursal = getattr(self.request,'sucursal_actual',None)

        if sucursal:
            queryset = queryset.filter(Q(sucursal=sucursal))

        if search_term:
            queryset = queryset.filter(
                
                Q(numero_referencia__icontains =search_term)
            )  # Filtrar por el término de búsqueda
        return queryset
    
    