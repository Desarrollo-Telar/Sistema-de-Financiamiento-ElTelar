# Serializador
from .serializers import RoleSerializer, PermisoSerializer

# Models
from apps.roles.models import Role, Permiso

# API
from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response

class RoleViewSet(viewsets.ModelViewSet):
    serializer_class = RoleSerializer
    queryset = Role.objects.all()

class PermisoViewSet(viewsets.ModelViewSet):
    serializer_class = PermisoSerializer
    queryset = Permiso.objects.all()