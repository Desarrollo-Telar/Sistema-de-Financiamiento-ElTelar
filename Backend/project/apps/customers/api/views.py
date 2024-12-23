# Serializador
from .serializers import CustomerSerializer, ImmigrationStatusSerializer

# API
from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response

# Models
from apps.customers.models import Customer, ImmigrationStatus

from django.db.models import Q

class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.query_params.get('term', '')  # Obtener el parámetro 'term'
        if search_term:
            queryset = queryset.filter(
                Q(first_name__icontains=search_term) |
                Q(last_name__icontains=search_term) |
                Q(customer_code__icontains=search_term)
                ) # Filtrar por el término de búsqueda
        return queryset

class CustomerAcceptViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.filter(status='Aprobado')
    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.query_params.get('term', '')  # Obtener el parámetro 'term'
        if search_term:
            queryset = queryset.filter(
                Q(first_name__icontains=search_term) |
                Q(last_name__icontains=search_term) |
                Q(customer_code__icontains=search_term)
                ) # Filtrar por el término de búsqueda
        return queryset

class ImmigrationStatusViewSet(viewsets.ModelViewSet):
    serializer_class = ImmigrationStatusSerializer
    queryset = ImmigrationStatus.objects.all()