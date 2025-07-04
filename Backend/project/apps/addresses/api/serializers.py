# Serializador
from rest_framework import serializers

# Models
from apps.addresses.models import Address, Municiopio, Departamento

class AddressSerializaer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class MunicipioSerializaer(serializers.ModelSerializer):
    class Meta:
        model = Municiopio
        fields = ['id','nombre','depart']

class DepartamentoSerializaer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields = ['id', 'nombre']