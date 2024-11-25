from django.contrib import admin

from .models import Address, Municiopio, Departamento

# Register your models here.
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    fields = (
        'street',
            'number',
            'city',
            'state',
            
            'country',
            'type_address',
            'latitud',
            'longitud',
            'customer_id'
    )
    list_display = ('street','number','city','state','country')
    search_fields = ('street','number','city','state','country','type_address','customer_id')
    list_filter=('customer_id','type_address')

admin.site.register(Municiopio)
admin.site.register(Departamento)