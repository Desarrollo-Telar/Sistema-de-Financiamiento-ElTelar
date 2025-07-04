from rest_framework import generics

# Serializador
from .serializers import AddressSerializaer, MunicipioSerializaer, DepartamentoSerializaer

# API
from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response

# Model
from apps.addresses.models import Address, Municiopio, Departamento

class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializaer
    queryset = Address.objects.all()

class MunicipioViewSet(viewsets.ModelViewSet):
    serializer_class = MunicipioSerializaer
    queryset = Municiopio.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.query_params.get('term', '')  # Obtener el parámetro 'term'
        if search_term:
            queryset = queryset.filter(nombre__icontains=search_term)  # Filtrar por el término de búsqueda
        return queryset

class DepartamentoViewSet(viewsets.ModelViewSet):
    serializer_class = DepartamentoSerializaer
    queryset = Departamento.objects.all()
    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.query_params.get('term', '')  # Obtener el parámetro 'term'
        if search_term:
            queryset = queryset.filter(nombre__icontains=search_term)  # Filtrar por el término de búsqueda
        return queryset