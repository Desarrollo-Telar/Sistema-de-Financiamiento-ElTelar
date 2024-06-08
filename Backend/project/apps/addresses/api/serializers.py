# Serializador
from rest_framework import serializers

# Models
from apps.addresses.models import Address, Coordinate

class AddressSerializaer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class CoordinateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordinate
        fields = '__all__'