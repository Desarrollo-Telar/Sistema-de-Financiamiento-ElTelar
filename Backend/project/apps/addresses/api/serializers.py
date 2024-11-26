# Serializador
from rest_framework import serializers

# Models
from apps.addresses.models import Address, Municiopio, Departamento

class AddressSerializaer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class MuniciopioSerializaer(serializers.ModelSerializer):
    class Meta:
        model = Municiopio
        fields = '__all__'

class DepartamentoSerializaer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields = ['id', 'nombre']