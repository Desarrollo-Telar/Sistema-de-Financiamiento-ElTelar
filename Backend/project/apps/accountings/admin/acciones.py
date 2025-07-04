# ADMIN
from django.contrib import admin
from django.contrib import messages

@admin.action(description='Cambiando el status a completado')
def marcar_completado(modeladmin, request, queryset):
    updated = queryset.update(status=True) 
    modeladmin.message_user(request, f'{updated} status cambiados a completados.', messages.SUCCESS)

@admin.action(description='Cambiando el status a pendiente')
def marcar_pendiente(modeladmin, request, queryset):
    updated = queryset.update(status=False) 
    modeladmin.message_user(request, f'{updated} status cambiados a pendientes.', messages.SUCCESS)