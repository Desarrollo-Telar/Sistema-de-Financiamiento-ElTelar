# API
from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from django.utils.timezone import datetime
from datetime import datetime
from rest_framework.request import Request

# MODELOS
from apps.accountings.models import Creditor, Insurance

# SERIALIZAERS
from .serializers import AcreedorSerializers, SeguroSerializers

class AcreedoresVigentesViewSet(viewsets.ModelViewSet):
    serializer_class = AcreedorSerializers
    queryset = Creditor.objects.filter(is_paid_off=False)

    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.query_params.get('term', '')  # Obtener el parámetro 'term'
        if search_term:
            queryset = queryset.filter(
                Q(codigo_acreedor__icontains =search_term) |
                Q(nombre_acreedor__icontains=search_term)
            )  # Filtrar por el término de búsqueda
        return queryset

class SegurosVigentesViewSet(viewsets.ModelViewSet):
    serializer_class = SeguroSerializers
    queryset = Insurance.objects.filter(is_paid_off=False)

    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.query_params.get('term', '')  # Obtener el parámetro 'term'
        if search_term:
            queryset = queryset.filter(
                Q(codigo_seguro__icontains =search_term) |
                Q(nombre_acreedor__icontains=search_term)
            )  # Filtrar por el término de búsqueda
        return queryset