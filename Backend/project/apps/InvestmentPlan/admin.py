from django.contrib import admin

from .models import InvestmentPlan

# Register your models here.
@admin.register(InvestmentPlan)
class InvestmentPlanAdmin(admin.ModelAdmin):
    fields = (
        'type_of_product_or_service',
            'total_value_of_the_product_or_service',
            'investment_plan_description',
            'initial_amount',
            'monthly_amount',
            'transfers_or_transfer_of_funds',
            'type_of_transfers_or_transfer_of_funds',
            'customer_id'
    )
    list_display = ('__str__','investment_plan_description','total_value_of_the_product_or_service','initial_amount','monthly_amount','investment_plan_code')
    search_fields = ('type_of_product_or_service','customer_id','investment_plan_code')
    list_filter = ('customer_id','type_of_product_or_service','investment_plan_code')