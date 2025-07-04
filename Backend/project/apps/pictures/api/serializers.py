# Serializador
from rest_framework import serializers

# Models
from apps.pictures.models import Imagen, ImagenAddress, ImagenCustomer, ImagenOther, ImagenGuarantee

class ImagenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imagen
        fields = '__all__'

class ImagenAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagenAddress
        fields = '__all__'

class ImagenCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagenCustomer
        fields = '__all__'

class ImagenOtherSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagenOther
        fields = '__all__'

class ImagenGuaranteeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagenGuarantee
        fields = '__all__'