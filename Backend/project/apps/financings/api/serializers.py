# SERIALIZADOR
from rest_framework import serializers

# MODELS
from apps.financings.models import Credit

class CreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credit
        fields = [
            'proposito',
            ''
        ]