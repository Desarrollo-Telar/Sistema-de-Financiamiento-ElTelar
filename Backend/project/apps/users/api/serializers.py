# SERIALIZADOR
from rest_framework import serializers

# MODELS
from apps.users.models import User, PermisoUsuario

# Serializadores 
from apps.subsidiaries.api.seriealizer import SubsidiarySerializer
from apps.roles.api.serializers import RoleSerializer, PermisoSerializer

class UserSerializer(serializers.ModelSerializer):
    #sucursal = SubsidiarySerializer(read_only=True)
    #rol = RoleSerializer(read_only=True)
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'type_identification',
            'identification_number',
            'telephone',
            'gender',
            'nationality',
            'profile_pic',
            'status',
            'rol',
            'nit',
            'sucursal'

        ]

    


class PermisoUsuarioSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    permiso = PermisoSerializer(read_only=True)
    class Meta:
        model = PermisoUsuario
        fields = '__all__'