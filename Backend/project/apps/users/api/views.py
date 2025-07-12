# Serializador
from .serializers import UserSerializer, PermisoUsuarioSerializer

# Models
from apps.users.models import User, PermisoUsuario

# API
from rest_framework import viewsets, status, generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response



class ProfileViewSet(viewsets.ViewSet):
    def list(self, request):
        user = request.user

        return Response({
            "id":user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "email": user.email,
            "type_identification": user.type_identification,
            "identification_number": user.identification_number,
            "telephone": user.telephone,
            "gender": user.gender,
            "nationality": user.nationality,
            "profile_pic": user.profile_pic.url if user.profile_pic else None,
            "status": user.status,
            "rol": {
                "id": user.rol.id,
                "role_name": user.rol.role_name
            } if user.rol else None,
            "nit": user.nit,
            "sucursal": {
                "id": user.sucursal.id,
                "nombre": user.sucursal.nombre
            } if user.sucursal else None
        })
  

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class PermisoUsuarioViewSet(viewsets.ModelViewSet):
    serializer_class = PermisoUsuarioSerializer
    queryset = PermisoUsuario.objects.all()