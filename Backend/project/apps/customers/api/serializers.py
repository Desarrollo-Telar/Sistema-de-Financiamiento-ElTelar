# Serializador
from rest_framework import serializers

# Models
from apps.customers.models import Customer, ImmigrationStatus

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class ImmigrationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImmigrationStatus
        fields = '__all__'