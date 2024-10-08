# Serializador
from .serializers import CreditSerializer, GuaranteesSerializer, DetailsGuaranteesSerializer, DisbursementSerializer
from .serializers import PaymentSerializer
# MODELS
from apps.financings.models import Credit, Guarantees, DetailsGuarantees, Disbursement, Payment

# API
from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response

class CreditViewSet(viewsets.ModelViewSet):
    serializer_class = CreditSerializer
    queryset = Credit.objects.all()

class GuaranteesViewSet(viewsets.ModelViewSet):
    serializer_class = GuaranteesSerializer
    queryset = Guarantees.objects.all()

class DetailsGuaranteesViewSet(viewsets.ModelViewSet):
    serializer_class = DetailsGuaranteesSerializer
    queryset = DetailsGuarantees.objects.all()

class DisbursementViewSet(viewsets.ModelViewSet):
    serializer_class = DisbursementSerializer
    queryset = Disbursement.objects.all()

class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()