# SERIALIZADOR
from rest_framework import serializers

# MODELS
from apps.users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'type_identification',
            'identification_number',
            'telephone',
            'gender',
            'nationality',
            'profile_pic',
            'status',
            'rol'

        ]