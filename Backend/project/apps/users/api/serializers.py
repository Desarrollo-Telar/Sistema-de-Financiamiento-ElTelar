# SERIALIZADOR
from rest_framework import serializers

# MODELS
from apps.users.models import User, PermisoUsuario

class UserSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = PermisoUsuario
        fields = '__all__'