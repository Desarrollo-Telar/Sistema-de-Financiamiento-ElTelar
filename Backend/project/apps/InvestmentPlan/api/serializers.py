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
        return {
            'id':instance.id,
            'type_of_product_or_service':instance.type_of_product_or_service,
            'total_value_of_the_product_or_service':instance.total_value_of_the_product_or_service,
            'investment_plan_description':instance.investment_plan_description,
            'initial_amount':instance.initial_amount,
            'monthly_amount':instance.monthly_amount,
            'transfers_or_transfer_of_funds':instance.transfers_or_transfer_of_funds,
            'type_of_transfers_or_transfer_of_funds':instance.type_of_transfers_or_transfer_of_funds,
            'customer_id':instance.customer_id.id,
            'investment_plan_code':instance.investment_plan_code
        }