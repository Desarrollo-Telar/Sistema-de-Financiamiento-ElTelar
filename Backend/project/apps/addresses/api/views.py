from rest_framework import generics

# Serializador
from .serializers import AddressSerializaer, MuniciopioSerializaer, DepartamentoSerializaer

# API
from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response

# Model
from apps.addresses.models import Address, Municiopio, Departamento

class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializaer
    queryset = Address.objects.all()

class MuniciopioViewSet(viewsets.ModelViewSet):
    serializer_class = MuniciopioSerializaer
    queryset = Municiopio.objects.all()

class DepartamentoViewSet(viewsets.ModelViewSet):
    serializer_class = DepartamentoSerializaer
    queryset = Departamento.objects.all()