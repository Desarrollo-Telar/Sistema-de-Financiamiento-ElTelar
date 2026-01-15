# Serializador
from rest_framework import serializers

# Models
from apps.roles.models import Role, Permiso, CategoriaPermiso

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'
    
    def to_representation(self, instance):
        return {
            'id':instance.id,
            'role_name':instance.role_name,
            'description':instance.description,
            'estado':instance.estado
        }


class CategoriaPermisoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaPermiso
        fields = '__all__'
    
    def to_representation(self, instance):
        return {
            'id':instance.id,
            'nombre':instance.nombre,
            'descripcion':instance.descripcion,
            'estado':instance.estado
        }

class PermisoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Permiso
        fields = '__all__'

    def to_representation(self, instance):
        categoria = CategoriaPermisoSerializer(instance.categoria_permiso).data if instance.categoria_permiso else None

        return {
            'id':instance.id,
            'categoria_permiso':categoria,
            'nombre':instance.nombre,
            'descripcion':instance.descripcion,
            'codigo_permiso':instance.codigo_permiso,
            'estado':instance.estado,
            'fecha_registro':instance.fecha_registro
        }