from django.contrib import admin

from .models import WorkingInformation, OtherSourcesOfIncome, Reference
# Register your models here.

@admin.register(WorkingInformation)
class WorkingInformationAdmin(admin.ModelAdmin):
    fields = (
        'position',
        'company_name',
        'start_date',            
        'salary',
        'working_hours',
        'phone_number',
        'source_of_income',
        'income_detail',
        'employment_status',
        'description',
        'customer_id'
    )

    list_display = ('__str__', 'customer_id','phone_number','salary')
    list_filter = ('customer_id',)
    autocomplete_fields = ('customer_id',)
    search_fields = ('salary','customer_id')
    
@admin.register(OtherSourcesOfIncome)
class OtherSourcesOfIncomeAdmin(admin.ModelAdmin):
    fields = (
        'source_of_income',
            'nit',
            'phone_number',
            'salary',
            'customer_id'
    )

    list_display = ('__str__', 'source_of_income','customer_id','phone_number','salary')
    search_fields = ('source_of_income', 'customer_id')
    list_filter = ('customer_id',)
    autocomplete_fields = ('customer_id',)

@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    fields = (
        'full_name',
            'phone_number',
            'reference_type',
            'customer_id'
    )
    list_display = ('__str__', 'full_name','customer_id','reference_type','phone_number')
    search_fields = ('full_name','reference_type','phone_number' ,'customer_id')
    list_filter = ('customer_id',)
    autocomplete_fields = ('customer_id',)