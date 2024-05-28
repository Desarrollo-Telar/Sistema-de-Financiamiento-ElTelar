# Serializador
from rest_framework import serializers

# Models
from apps.addresses.models import Address

class AddressSerializaer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'