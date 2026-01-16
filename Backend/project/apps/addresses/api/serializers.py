# Serializador
from rest_framework import serializers

# Models
from apps.addresses.models import Address, Municiopio, Departamento

class AddressSerializaer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

    def to_representation(self, instance):
        from apps.customers.api.serializers import SubsidiarySerializer, CustomerSerializer
        sucursal = SubsidiarySerializer(instance.subsidiary).data if instance.subsidiary else None
        cliente = CustomerSerializer(instance.customer_id).data if instance.customer_id else None

        return {
            'id':instance.id,
            'street': instance.street,
            'number':instance.number,
            'city':instance.city,
            'state':instance.state,
            'country':instance.country,
            'type_address':instance.type_address,
            'latitud':instance.latitud,
            'longitud':instance.longitud,
            'customer_id':cliente,
            'subsidiary': sucursal,
            'codigo_postal':instance.codigo_postal
        }

class MunicipioSerializaer(serializers.ModelSerializer):
    class Meta:
        model = Municiopio
        fields = ['id','nombre','depart']

    def to_representation(self, instance):
        departamento = DepartamentoSerializaer(instance.depart).data if instance.depart else None
        
        return {
            'id':instance.id,
            'nombre': instance.nombre,
            'depart': departamento
            
        }

class DepartamentoSerializaer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields = ['id', 'nombre']

    def to_representation(self, instance):
        return {
            'id':instance.id,
            'nombre': instance.nombre,
            'codigo_postal':instance.codigo_postal
            
        }