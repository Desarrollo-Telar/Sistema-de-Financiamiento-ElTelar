# Serializador
from .serializers import CreditSerializer, GuaranteesSerializer, DetailsGuaranteesSerializer, DisbursementSerializer, FacturaSerializer, ReciboSerializer
from .serializers import PaymentSerializer, PaymentPlanSerializer, EstadoCuentaSerializer
from .serializers import PaymentPlanSerializerSeguro,PaymentPlanSerializerAcreedor
# MODELS
from apps.financings.models import Credit, Guarantees, DetailsGuarantees, Disbursement, Payment, Invoice, Recibo
from apps.financings.models import PaymentPlan, AccountStatement, Banco

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
    queryset = Credit.objects.filter(is_paid_off=False)

    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.query_params.get('term', '')  # Obtener el parámetro 'term'
        if search_term:
            queryset = queryset.filter(
                Q(customer_id__first_name__icontains =search_term)|
                Q(customer_id__last_name__icontains =search_term)|
                Q(codigo_credito__icontains =search_term)
            )  # Filtrar por el término de búsqueda
        return queryset

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
   
class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.query_params.get('term', '')  # Obtener el parámetro 'term'
        if search_term:
            queryset = queryset.filter(
                
                Q(numero_referencia__icontains =search_term)
            )  # Filtrar por el término de búsqueda
        return queryset

class FacturaViewSet(viewsets.ModelViewSet):
    serializer_class = FacturaSerializer
    queryset = Invoice.objects.all()



class ReciboViewSet(viewsets.ModelViewSet):
    serializer_class = ReciboSerializer
    queryset = Recibo.objects.all()

    def get_queryset(self):
        # Obtener parámetros de la solicitud
        request = self.request
        query_params = request.query_params

        # Valores predeterminados
        mes = query_params.get('mes', datetime.now().month)
        anio = query_params.get('anio', datetime.now().year)
        filtro_seleccionado = query_params.get('filtro', 'mora_pagada')

        try:
            mes = int(mes)
            anio = int(anio)
        except ValueError:
            mes = datetime.now().month
            anio = datetime.now().year

        # Filtros por fecha
        filters = Q(fecha__year=anio, fecha__month=mes)

        # Filtros dinámicos según selección del usuario
        filtros_validos = {
            'mora_pagada': 'mora_pagada__gt',
            'interes_pagado': 'interes_pagado__gt',
            'aporte_capital': 'aporte_capital__gt',
        }

        if filtro_seleccionado in filtros_validos:
            filtro_dinamico = {filtros_validos[filtro_seleccionado]: 0}
            return Recibo.objects.filter(filters, **filtro_dinamico)

        return Recibo.objects.filter(filters)



class PaymentPlanViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentPlanSerializer
    queryset = PaymentPlan.objects.all()

class PaymentPlanUltimoViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentPlanSerializer
    queryset = PaymentPlan.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        search_term = self.request.query_params.get('term', '')

        if search_term:
            queryset = queryset.filter(
                Q(id__icontains=search_term) 
            )

        last_item = queryset.order_by('-id').first()
        if last_item:
            serializer = self.get_serializer(last_item)
            return Response(serializer.data)
        return Response([])  # Si no hay datos que coincidan, devolver una lista vacía

class PaymentPlanAmpliacion(viewsets.ModelViewSet):
    serializer_class = PaymentPlanSerializer
    queryset = PaymentPlan.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.query_params.get('term', '')  # Obtener el parámetro 'term'

        if search_term:
            dia = datetime.now().date()
            dia_mas_uno = dia + timedelta(days=1)

            siguiente_pago = PaymentPlan.objects.filter(
                credit_id__id=search_term,
                start_date__lte=dia,
                fecha_limite__gte=dia_mas_uno
            ).first()

            if siguiente_pago is None:
                siguiente_pago = PaymentPlan.objects.filter(
                    credit_id__id=search_term
                ).order_by('-id').first()

            if siguiente_pago:
                return PaymentPlan.objects.filter(id=siguiente_pago.id)
            else:
                return PaymentPlan.objects.none()  # Devuelve un queryset vacío

        return queryset

class PaymentPlanAcreedorUltimoViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentPlanSerializerAcreedor
    queryset = PaymentPlan.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        search_term = self.request.query_params.get('term', '')
        if search_term:
            queryset = queryset.filter(
                Q(id__icontains=search_term) 
            )
        last_item = queryset.order_by('-id').first()
        if last_item:
            serializer = self.get_serializer(last_item)
            return Response(serializer.data)
        return Response([])  # Si no hay datos que coincidan, devolver una lista vacía

class PaymentPlanSeguroUltimoViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentPlanSerializerSeguro
    queryset = PaymentPlan.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        search_term = self.request.query_params.get('term', '')
        if search_term:
            queryset = queryset.filter(
                Q(seguro__id__icontains=search_term) 
            )
        last_item = queryset.order_by('-id').first()
        if last_item:
            serializer = self.get_serializer(last_item)
            return Response(serializer.data)
        return Response([])  # Si no hay datos que coincidan, devolver una lista vacía