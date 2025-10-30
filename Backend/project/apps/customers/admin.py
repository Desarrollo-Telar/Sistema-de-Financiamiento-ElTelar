from django.contrib import admin

from .models import Customer, ImmigrationStatus, CreditCounselor, Cobranza

# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    fields = (
        'first_name',
        'last_name',
        'type_identification',
        'identification_number',
        'marital_status',            
        'nationality',
        'number_nit',
        'date_birth',
        'place_birth',
        'gender',
        'profession_trade',
        'person_type',
        'telephone',
        'email',
        'status',  
        'user_id',
        'immigration_status_id',
        "description",
        "asesor",
        "fehca_vencimiento_de_tipo_identificacion"
        
    )
    list_display = ('customer_code', 'first_name', 'last_name', 'telephone', 'identification_number', 'email', 'status')
    search_fields = ('customer_code', 'identification_number', 'first_name', 'last_name', 'email', 'status')
    list_filter = ('customer_code', 'status', 'type_identification','sucursal')
    date_hierarchy = 'creation_date'
    ordering = ['-customer_code']
    list_per_page = 25

    
admin.site.register(ImmigrationStatus)
admin.site.register(CreditCounselor)
admin.site.register(Cobranza)