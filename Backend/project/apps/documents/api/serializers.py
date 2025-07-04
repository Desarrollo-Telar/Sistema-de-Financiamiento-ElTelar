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
    document_id = DocumentSerializer()  

    class Meta:
        model = DocumentGuarantee
        fields = [
            'garantia',
            'document_id',
            'customer_id'
        ]

    def create(self, validated_data):
        document_data = validated_data.pop('document_id')
        document = Document.objects.create(**document_data)
        return DocumentGuarantee.objects.create(document_id=document, **validated_data)