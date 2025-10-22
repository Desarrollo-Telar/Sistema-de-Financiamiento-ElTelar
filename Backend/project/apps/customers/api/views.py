# Serializador
from .serializers import CustomerSerializer, ImmigrationStatusSerializer, CreditCounselorSerializer, CobranzaSerializer, HistorialCobranzaSerializer

# API
from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response

# Models
from apps.customers.models import Customer, ImmigrationStatus, CreditCounselor, Cobranza, HistorialCobranza

from django.db.models import Q

from django.utils.timezone import datetime

# HISTORIAL Y BITACORA
from apps.actividades.utils import log_user_action, log_system_event
from scripts.conversion_datos import model_to_dict, cambios_realizados


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

class HistorialCobranzaViewSet(viewsets.ModelViewSet):
    serializer_class = HistorialCobranzaSerializer
    queryset = HistorialCobranza.objects.all()

class CreditCounselorSerializerViewSet(viewsets.ModelViewSet):
    serializer_class = CreditCounselorSerializer

    queryset = CreditCounselor.objects.filter(status=True)

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        request = self.request
        search_term = self.request.query_params.get('term', '')  # Obtener el parámetro 'term'

        # obteniendo la sucursal del usuario
        sucursal = getattr(request,'sucursal_actual',None)

        

        if sucursal:
            queryset = queryset.filter(Q(sucursal=sucursal)| Q(sucursal__isnull=True))


        if search_term:
            queryset = queryset.filter(
                Q(nombre__icontains=search_term) |
                Q(apellido__icontains=search_term) |
                Q(codigo_asesor__icontains=search_term) |
                Q(sucursal__isnull=True)
                )# Filtrar por el término de búsqueda
            
        return queryset
    
class CobranzaViewSet(viewsets.ModelViewSet):
    serializer_class = CobranzaSerializer

    def get_queryset(self):
        asesor_autenticado = CreditCounselor.objects.filter(usuario=self.request.user).first()

        if not asesor_autenticado:
            return Cobranza.objects.none()

        queryset = Cobranza.objects.filter(asesor_credito=asesor_autenticado)

        # Recoger parámetros de búsqueda
        search_term = self.request.query_params.get('term', '').strip()
        user_code = self.request.query_params.get('user_code', '').strip()

        if search_term:
            queryset = queryset.filter(
                Q(credito__customer_id__first_name__icontains=search_term) |
                Q(credito__customer_id__last_name__icontains=search_term) |
                Q(credito__codigo_credito__icontains=search_term) 
            )

        if user_code:            
            asesor_autenticado = CreditCounselor.objects.filter(usuario__user_code=user_code).first()
            queryset = Cobranza.objects.filter(asesor_credito=asesor_autenticado)

        return queryset

