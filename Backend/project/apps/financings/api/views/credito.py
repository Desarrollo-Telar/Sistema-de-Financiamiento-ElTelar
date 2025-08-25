# Serializador
from apps.financings.api.serializers import CreditSerializer
# MODELS
from apps.financings.models import Credit
from apps.customers.models import Customer, CreditCounselor, Cobranza
from apps.actividades.models import Informe, DetalleInformeCobranza

# API
from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from django.utils.timezone import datetime

from rest_framework.request import Request
from rest_framework.exceptions import NotFound

# Tiempo
from datetime import datetime, timedelta


class CreditViewSet(viewsets.ModelViewSet):
    serializer_class = CreditSerializer
    queryset = Credit.objects.all()


    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtro por término de búsqueda
        search_term = self.request.query_params.get('term', '')
        # Obtener el mes de creación opcional
        month = self.request.query_params.get('month', None)
        year = self.request.query_params.get('year', None)

        if search_term:
            queryset = queryset.filter(
                Q(customer_id__first_name__icontains=search_term) |
                Q(customer_id__last_name__icontains=search_term) |
                Q(codigo_credito__icontains=search_term)
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


class CreditVigentesViewSet(viewsets.ModelViewSet):
    serializer_class = CreditSerializer

    def get_queryset(self):
        queryset = Credit.objects.filter(is_paid_off=False)
        search_term = self.request.query_params.get('term', '').strip()

        # Obtener el asesor autenticado
        asesor_autenticado = CreditCounselor.objects.filter(usuario=self.request.user).first()
        roles = ['Administrador', 'Programador']

        if search_term:
            filters = (
                Q(customer_id__first_name__icontains=search_term) |
                Q(customer_id__last_name__icontains=search_term) |
                Q(codigo_credito__icontains=search_term)
            )

            if asesor_autenticado:
                if not self.request.user.rol.role_name in roles:
                    filters &= Q(customer_id__new_asesor_credito__id=asesor_autenticado.id)

            queryset = queryset.filter(filters)

        elif asesor_autenticado:
            # Si no hay término de búsqueda, pero sí asesor autenticado, filtrar por él
            if not self.request.user.rol.role_name in roles:
                queryset = queryset.filter(customer_id__new_asesor_credito__id=asesor_autenticado.id)

        return queryset


class CreditVigentesCobranzaViewSet(viewsets.ModelViewSet):
    serializer_class = CreditSerializer

    def get_queryset(self):
        base_qs = Credit.objects.filter(is_paid_off=False, estado_judicial=False)
        search_term = self.request.query_params.get('term', '').strip()

        asesor_autenticado = CreditCounselor.objects.filter(usuario=self.request.user).first()
        reporte_id = Informe.objects.filter(usuario=self.request.user, esta_activo=True).first()
        roles = ['Administrador', 'Programador']
        role_name = getattr(getattr(self.request.user, 'rol', None), 'role_name', None)

        if not asesor_autenticado or not reporte_id:
            raise NotFound("No se encontró información para este usuario.")

        informe_vigente = DetalleInformeCobranza.objects.filter(reporte_id=reporte_id)
        creditos_con_cobranza = Credit.objects.filter(
            id__in=informe_vigente.values_list("cobranza__credito_id", flat=True)
        )

        queryset = base_qs.filter(estados_fechas=False).exclude(id__in=creditos_con_cobranza)

        if search_term:
            filters = (
                Q(customer_id__first_name__icontains=search_term) |
                Q(customer_id__last_name__icontains=search_term) |
                Q(codigo_credito__icontains=search_term)
            )
            if role_name not in roles:
                filters &= Q(customer_id__new_asesor_credito__id=asesor_autenticado.id)
            queryset = queryset.filter(filters)
        elif role_name not in roles:
            queryset = queryset.filter(customer_id__new_asesor_credito__id=asesor_autenticado.id)

        return queryset
