# Serializador
from .serializers import CustomerSerializer, ImmigrationStatusSerializer, CreditCounselorSerializer

# API
from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response

# Models
from apps.customers.models import Customer, ImmigrationStatus, CreditCounselor

from django.db.models import Q

from django.utils.timezone import datetime

class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()

        # Obtener el término de búsqueda opcional
        search_term = self.request.query_params.get('term', '')

        # Obtener el mes de creación opcional
        month = self.request.query_params.get('month', None)
        year = self.request.query_params.get('year', None)

        # Filtrar por término de búsqueda si existe
        if search_term:
            queryset = queryset.filter(
                Q(first_name__icontains=search_term) |
                Q(last_name__icontains=search_term) |
                Q(customer_code__icontains=search_term)
            )

        # Filtrar por mes y año si se proporcionan
        if month and year:
            try:
                # Validar que el mes y el año son valores válidos
                month = int(month)
                year = int(year)
                queryset = queryset.filter(
                    created_at__year=year,
                    created_at__month=month
                )
            except ValueError:
                # Si los valores no son válidos, se ignora el filtro de mes/año
                pass

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

class CreditCounselorSerializerViewSet(viewsets.ModelViewSet):
    serializer_class = CreditCounselorSerializer

    queryset = CreditCounselor.objects.filter(status=True)

    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.query_params.get('term', '')  # Obtener el parámetro 'term'
        if search_term:
            queryset = queryset.filter(
                Q(nombre__icontains=search_term) |
                Q(apellido__icontains=search_term) |
                Q(codigo_asesor__icontains=search_term)
                ) # Filtrar por el término de búsqueda
        return queryset