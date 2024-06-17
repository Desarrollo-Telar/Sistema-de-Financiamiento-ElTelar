# Serializador
from rest_framework import serializers

# Models
from apps.documents.models import Document, DocumentAddress, DocumentCustomer, DocumentGuarantee, DocumentOther


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'

class DocumentAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentAddress
        fields = '__all__'

class DocumentCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentCustomer
        fields = '__all__'

class DocumentOtherSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentOther
        fields = '__all__'

class DocumentGuaranteeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentGuarantee
        fields = '__all__'