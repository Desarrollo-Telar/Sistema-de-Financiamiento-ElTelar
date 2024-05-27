# Serializador
from rest_framework import serializers

# Models
from apps.roles.models import Role

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'