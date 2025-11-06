# Serializador
from rest_framework import serializers

# Models
from apps.roles.models import Role, Permiso, CategoriaPermiso

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class CategoriaPermisoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaPermiso
        fields = '__all__'

class PermisoSerializer(serializers.ModelSerializer):
    categoria_permiso = CategoriaPermisoSerializer(read_only = True)
    class Meta:
        model = Permiso
        fields = '__all__'