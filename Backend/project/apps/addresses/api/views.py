from rest_framework import generics

# Serializador
from .serializers import AddressSerializaer, CoordinateSerializer

# API
from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response

# Model
from apps.addresses.models import Address, Coordinate

class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializaer
    queryset = Address.objects.all()

class CoordinateViewSet(viewsets.ModelViewSet):
    serializer_class = CoordinateSerializer
    queryset = Coordinate.objects.all()