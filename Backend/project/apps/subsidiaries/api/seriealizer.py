# SERIALIZADOR
from rest_framework import serializers

# Modelo
from apps.subsidiaries.models import Subsidiary


class SubsidiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subsidiary
        fields = '__all__'
