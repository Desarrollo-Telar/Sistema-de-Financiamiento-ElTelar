# Serializador
from .serializers import CustomerSerializer, ImmigrationStatusSerializer

# API
from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response

# Models
from apps.customers.models import Customer, ImmigrationStatus

class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()

class ImmigrationStatusViewSet(viewsets.ModelViewSet):
    serializer_class = ImmigrationStatusSerializer
    queryset = ImmigrationStatus.objects.all()