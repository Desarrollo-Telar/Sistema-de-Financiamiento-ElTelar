# Serializador
from .serializers import CreditSerializer, GuaranteesSerializer, DetailsGuaranteesSerializer, DisbursementSerializer, FacturaSerializer, ReciboSerializer
from .serializers import PaymentSerializer, PaymentPlanSerializer, EstadoCuentaSerializer
# MODELS
from apps.financings.models import Credit, Guarantees, DetailsGuarantees, Disbursement, Payment, Invoice, Recibo
from apps.financings.models import PaymentPlan, AccountStatement, Banco

# API
from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q

class EstadoCuentaViewSet(viewsets.ModelViewSet):
    serializer_class = EstadoCuentaSerializer
    queryset = AccountStatement.objects.all()

class CreditViewSet(viewsets.ModelViewSet):
    serializer_class = CreditSerializer
    queryset = Credit.objects.all()

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

class FacturaViewSet(viewsets.ModelViewSet):
    serializer_class = FacturaSerializer
    queryset = Invoice.objects.all()

class ReciboViewSet(viewsets.ModelViewSet):
    serializer_class = ReciboSerializer
    queryset = Recibo.objects.all()

from rest_framework.response import Response
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
                Q(credit_id__id__icontains=search_term) 
            )
        last_item = queryset.order_by('-id').first()
        if last_item:
            serializer = self.get_serializer(last_item)
            return Response(serializer.data)
        return Response([])  # Si no hay datos que coincidan, devolver una lista vacía
