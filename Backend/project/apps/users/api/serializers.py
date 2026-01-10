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

    def to_representation(self, instance):
        sucursal_serializado = SubsidiarySerializer(instance.sucursal).data if instance.sucursal else None
        rol_serializado = RoleSerializer(instance.rol).data if instance.rol else None

        return{
            "id":instance.id,
            "first_name":instance.first_name,
            "last_name":instance.last_name,
            "username":instance.username,
            "email":instance.email,
            "type_identification":instance.type_identification,
            'identification_number':instance.identification_number,
            'telephone':instance.telephone,
            'gender':instance.gender,
            'nationality':instance.nationality,            
            'status':instance.status,
            'rol': rol_serializado,
            'nit': instance.nit,
            'sucursal': sucursal_serializado
        }



    


class PermisoUsuarioSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    permiso = PermisoSerializer(read_only=True)
    class Meta:
        model = PermisoUsuario
        fields = '__all__'