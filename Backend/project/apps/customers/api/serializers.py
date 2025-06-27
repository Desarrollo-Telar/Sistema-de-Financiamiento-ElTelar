# Serializador
from rest_framework import serializers

# Models
from apps.customers.models import Customer, ImmigrationStatus, CreditCounselor

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "first_name",
            "last_name",
            "type_identification",
            "identification_number",
            "telephone",
            "email",
            "status",
            "date_birth",
            "number_nit",
            "place_birth",
            "marital_status",
            "profession_trade",
            "gender",
            "nationality",
            "person_type",
            "user_id",
            "immigration_status_id",
            "description",
            "asesor",
            "fehca_vencimiento_de_tipo_identificacion",
            "new_asesor_credito",
        ]
    


class ImmigrationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImmigrationStatus
        fields = '__all__'

class CreditCounselorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCounselor
        fields = '__all__'