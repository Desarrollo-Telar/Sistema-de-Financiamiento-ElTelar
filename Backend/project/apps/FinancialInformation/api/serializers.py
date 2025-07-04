# Serializador
from rest_framework import serializers

# Models
from apps.FinancialInformation.models import WorkingInformation, OtherSourcesOfIncome, Reference

class WorkingInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkingInformation
        fields = '__all__'

class OtherSourcesOfIncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherSourcesOfIncome
        fields = '__all__'

class ReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reference
        fields = '__all__'