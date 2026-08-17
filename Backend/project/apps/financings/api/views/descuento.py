# Serializador
from apps.financings.api.serializers import  DescuentoSerializer
# MODELS
from apps.financings.models import Descuento

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

import traceback
from rest_framework import status
from rest_framework.exceptions import ValidationError


class DescuenntoViewSet(viewsets.ModelViewSet):
    serializer_class = DescuentoSerializer
    queryset = Descuento.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.query_params.get('term', '')  # Obtener el parámetro 'term'

        if search_term:
            queryset = Descuento.objects.filter(
                Q(id__icontains=search_term) 
            ).first()


        
        return queryset 