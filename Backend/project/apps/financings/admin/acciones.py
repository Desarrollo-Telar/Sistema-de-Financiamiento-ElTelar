from django.contrib import admin
from django.contrib import messages

# models
from apps.subsidiaries.models import Subsidiary

@admin.action(description='Cambiando el registro de banco a otra sucursal 1')
def cambiar_sucursal_1(modeladmin, request, queryset):
    sucursal_id = Subsidiary.objects.get(id= 1)
    updated = queryset.update(sucursal=sucursal_id) 
    modeladmin.message_user(request, f'{updated} cambio de registro a sucursal 1.', messages.SUCCESS)

@admin.action(description='Cambiando el registro de banco a otra sucursal 2')
def cambiar_sucursal_2(modeladmin, request, queryset):
    sucursal_id = Subsidiary.objects.get(id= 2)
    updated = queryset.update(sucursal=sucursal_id) 
    modeladmin.message_user(request, f'{updated} cambio de registro a sucursal 2.', messages.SUCCESS)