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
            'type_of_transfers_or_transfer_of_funds'
            'customer_id'
        ]