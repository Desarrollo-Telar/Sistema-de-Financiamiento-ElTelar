# Serializador
from .serializers import ImagenAddressSerializer, ImagenSerializer, ImagenCustomerSerializer, ImagenOtherSerializer, ImagenGuaranteeSerializer

# Models
from apps.pictures.models import Imagen, ImagenAddress, ImagenCustomer, ImagenOther, ImagenGuarantee

# API
from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response

class ImagenViewSet(viewsets.ModelViewSet):
    serializer_class = ImagenSerializer
    queryset = Imagen.objects.all()

class ImagenAddressViewSet(viewsets.ModelViewSet):
    serializer_class = ImagenAddressSerializer
    queryset = ImagenAddress.objects.all()

class ImagenCustomerViewSet(viewsets.ModelViewSet):
    serializer_class = ImagenCustomerSerializer
    queryset = ImagenCustomer.objects.all()

class ImagenOtherViewSet(viewsets.ModelViewSet):
    serializer_class = ImagenOtherSerializer
    queryset = ImagenOther.objects.all()

class ImagenGuaranteeViewSet(viewsets.ModelViewSet):
    serializer_class = ImagenGuaranteeSerializer
    queryset = ImagenGuarantee.objects.all()