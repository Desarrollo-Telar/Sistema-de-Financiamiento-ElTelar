# Serializador
from .serializers import UserSerializer, PermisoUsuarioSerializer

# Models
from apps.users.models import User, PermisoUsuario

# API
from rest_framework import viewsets, status, generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response



class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class PermisoUsuarioViewSet(viewsets.ModelViewSet):
    serializer_class = PermisoUsuarioSerializer
    queryset = PermisoUsuario.objects.all()