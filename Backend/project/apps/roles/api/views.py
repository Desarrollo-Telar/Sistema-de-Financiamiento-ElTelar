# Serializador
from .serializers import RoleSerializer

# Models
from apps.roles.models import Role

# API
from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response

class RoleViewSet(viewsets.ModelViewSet):
    serializer_class = RoleSerializer
    queryset = Role.objects.all()