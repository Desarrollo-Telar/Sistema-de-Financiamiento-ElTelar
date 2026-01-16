# SERIALIZADOR
from rest_framework import serializers

# MODELS
from apps.InvestmentPlan.models import InvestmentPlan

class InvestmentPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentPlan
        fields = [
            'type_of_product_or_service',
            'total_value_of_the_product_or_service',
            'investment_plan_description',
            'initial_amount',
            'monthly_amount',
            'transfers_or_transfer_of_funds',
            'type_of_transfers_or_transfer_of_funds',
            'customer_id'
        ]
    def to_representation(self, instance):
        from apps.customers.api.serializers import CustomerSerializer
        cliente = CustomerSerializer(instance.customer_id).data if instance.customer_id else None
        return {
            'id':instance.id,
            'type_of_product_or_service':instance.type_of_product_or_service,
            'total_value_of_the_product_or_service':instance.total_value_of_the_product_or_service,
            'investment_plan_description':instance.investment_plan_description,
            'initial_amount':instance.initial_amount,
            'monthly_amount':instance.monthly_amount,
            'transfers_or_transfer_of_funds':instance.transfers_or_transfer_of_funds,
            'type_of_transfers_or_transfer_of_funds':instance.type_of_transfers_or_transfer_of_funds,
            'customer_id': cliente,
            'investment_plan_code':instance.investment_plan_code
        }