from django.contrib import admin

from .models import Address, Coordinate

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
            'customer_id'
    )
    list_display = ('street','number','city','state','country')
    search_fields = ('street','number','city','state','country','type_address','customer_id')

@admin.register(Coordinate)
class CoordinateAdmin(admin.ModelAdmin):
    fields = (
        'latitud',
        'longitud',
        'address_id'
    )

    list_display = ('address_id','latitud','longitud')
    search_fields = ('address_id','latitud','longitud')