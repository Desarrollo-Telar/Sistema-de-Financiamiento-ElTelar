from django.contrib import admin

# Modelos
from .models import Imagen, ImagenAddress, ImagenCustomer, ImagenGuarantee, ImagenOther

# Formularios
from .forms import ImagenForms
# Register your models here.
@admin.register(Imagen)
class ImagenAdmin(admin.ModelAdmin):
    form = ImagenForms
    list_display = ('image', 'description')
    search_fields = ('image', 'description')
    

@admin.register(ImagenAddress)
class ImagenAddressAdmin(admin.ModelAdmin):
    list_display = ('image_id', 'address_id','customer_id')
    search_fields = ('image','address_id' ,'customer_id')
    list_filter=('customer_id',)

@admin.register(ImagenCustomer)
class ImagenCustomerAdmin(admin.ModelAdmin):
    list_display = ('image_id', 'customer_id')
    search_fields = ('image', 'customer_id')
    list_filter=('customer_id',)

@admin.register(ImagenGuarantee)
class ImagenGuaranteeAdmin(admin.ModelAdmin):
    list_display = ('image_id', 'investment_plan_id','customer_id')
    search_fields = ('image','investment_plan_id' ,'customer_id')
    list_filter=('customer_id',)

@admin.register(ImagenOther)
class ImagenOtherAdmin(admin.ModelAdmin):
    list_display = ('image_id','description', 'customer_id')
    search_fields = ('image','description' ,'customer_id')
    list_filter=('customer_id',)