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
    def to_representation(self, instance):
        return {
            'id':instance.id,
            "first_name": instance.first_name,
            "last_name": instance.last_name,
            "type_identification": instance.type_identification,
            "identification_number": instance.identification_number,
            "telephone": instance.telephone,
            "email": instance.email,
            "status": instance.status,
            "date_birth": instance.date_birth,
            "number_nit": instance.number_nit,
            "place_birth": instance.place_birth,
            "marital_status": instance.marital_status,
            "profession_trade": instance.profession_trade,
            "gender": instance.gender,
            "nationality": instance.nationality,
            "person_type": instance.person_type,
            "user_id": instance.user_id.id,
            "immigration_status_id": instance.immigration_status_id.id,
            'customer_code':instance.customer_code,
            "description":instance.description,
            "creation_date":instance.creation_date.date(),
        }


class ImmigrationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImmigrationStatus
        fields = '__all__'

class CreditCounselorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCounselor
        fields = '__all__'