from django.contrib import admin

from .models import Customer, ImmigrationStatus

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
            'description',
            'user_id',
            'immigration_status_id'
    )
    list_display = ('get_full_name','customer_code','telephone','identification_number','email','status')
    search_fields = ('customer_code','identification_number','first_name','last_name','email','status')
    
admin.site.register(ImmigrationStatus)