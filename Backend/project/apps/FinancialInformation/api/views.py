# Serializador
from .serializers import WorkingInformationSerializer, OtherSourcesOfIncomeSerializer, ReferenceSerializer

# API
from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response

# MODELS
from apps.FinancialInformation.models import WorkingInformation, OtherSourcesOfIncome, Reference

class WorkingInformationViewSet(viewsets.ModelViewSet):
    serializer_class = WorkingInformationSerializer
    queryset = WorkingInformation.objects.all()

class OtherSourcesOfIncomeViewSet(viewsets.ModelViewSet):
    serializer_class = OtherSourcesOfIncomeSerializer
    queryset = OtherSourcesOfIncome.objects.all()

class ReferenceViewSet(viewsets.ModelViewSet):
    serializer_class = ReferenceSerializer
    queryset = Reference.objects.all()