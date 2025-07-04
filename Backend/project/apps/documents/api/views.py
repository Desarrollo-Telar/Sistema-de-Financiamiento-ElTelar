# SERIALIZADOR
from .serializers import DocumentCustomerSerializer,DocumentGuaranteeSerializer, DocumentOtherSerializer,DocumentSerializer,DocumentAddressSerializer
# MODELS
from apps.documents.models import Document,DocumentAddress,DocumentCustomer,DocumentGuarantee,DocumentOther
# API
from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response

class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    queryset = Document.objects.all()

class DocumentAddressViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentAddressSerializer
    queryset = DocumentAddress.objects.all()

class DocumentCustomerViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentCustomerSerializer
    queryset = DocumentCustomer.objects.all()

class DocumentOtherViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentOtherSerializer
    queryset = DocumentOther.objects.all()

class DocumentGuaranteeViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentGuaranteeSerializer
    queryset = DocumentGuarantee.objects.all()