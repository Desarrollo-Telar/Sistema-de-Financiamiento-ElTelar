# Serializador
from .serializers import CodeSerializer

# API
from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response

# Models
from apps.codes.models import Code

class CodeViewSet(viewsets.ModelViewSet):
    serializer_class = CodeSerializer
    queryset = Code.objects.all()