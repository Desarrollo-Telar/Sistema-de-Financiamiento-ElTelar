# Serializador
from .serializers import ImagenAddressSerializer, ImagenSerializer, ImagenCustomerSerializer, ImagenOtherSerializer, ImagenGuaranteeSerializer

# Models
from apps.pictures.models import Imagen, ImagenAddress, ImagenCustomer, ImagenOther, ImagenGuarantee

# API
from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response

# HISTORIAL Y BITACORA
from apps.actividades.utils import log_user_action, log_system_event
from scripts.conversion_datos import model_to_dict, cambios_realizados

import traceback
from rest_framework import status
from rest_framework.exceptions import ValidationError


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