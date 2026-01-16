# SERIALIZADOR
from rest_framework import serializers

# Modelo
from apps.subsidiaries.models import Subsidiary


class SubsidiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subsidiary
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'id':instance.id,
            'codigo_sucursal':instance.codigo_sucursal,
            'nombre':instance.nombre,
            'fecha_apertura':instance.fecha_apertura,
            'numero_telefono': instance.numero_telefono,
            'otro_numero_telefono': instance.otro_numero_telefono,
            'activa':instance.activa,
            'codigo_postal':instance.codigo_postal,
            'descripcion':instance.descripcion,
            'codigo_establecimiento': instance.codigo_establecimiento,
            'numero_de_cuenta_banco': instance.numero_de_cuenta_banco,
            'nombre_banco': instance.nombre_banco
        }