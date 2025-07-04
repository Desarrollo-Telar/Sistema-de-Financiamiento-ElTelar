# Serializador
from rest_framework import serializers

# Models
from apps.codes.models import Code

class CodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Code
        fields = '__all__'