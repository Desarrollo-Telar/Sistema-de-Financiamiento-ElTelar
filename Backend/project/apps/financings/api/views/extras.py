# Serializador
from apps.financings.api.serializers import  GuaranteesSerializer, DetailsGuaranteesSerializer, DisbursementSerializer, EstadoCuentaSerializer

# MODELS
from apps.financings.models import Guarantees, DetailsGuarantees, Disbursement, AccountStatement


# API
from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from django.utils.timezone import datetime

from rest_framework.request import Request

# Tiempo
from datetime import datetime, timedelta

class EstadoCuentaViewSet(viewsets.ModelViewSet):
    serializer_class = EstadoCuentaSerializer
    queryset = AccountStatement.objects.all()

class GuaranteesViewSet(viewsets.ModelViewSet):
    serializer_class = GuaranteesSerializer
    queryset = Guarantees.objects.all()

class DetailsGuaranteesViewSet(viewsets.ModelViewSet):
    serializer_class = DetailsGuaranteesSerializer
    queryset = DetailsGuarantees.objects.all()

class DisbursementViewSet(viewsets.ModelViewSet):
    serializer_class = DisbursementSerializer
    queryset = Disbursement.objects.all()
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.query_params.get('term', '')  # Obtener el parámetro 'term'
        if search_term:
            queryset = queryset.filter(
                #Q(credit_id__id__icontains=search_term) |
                #Q(credit_id__customer_id__last_name__icontains =search_term)|
                Q(credit_id__codigo_credito__icontains =search_term)
            )  # Filtrar por el término de búsqueda
        return queryset