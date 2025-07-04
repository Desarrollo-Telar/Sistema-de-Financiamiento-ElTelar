# ADMIN
from django.contrib import admin

# Modelo
from apps.actividades.models import Notification, DocumentoNotificacionCliente, NotificationCustomer

@admin.register(Notification)
class NotificacionesAdmin(admin.ModelAdmin):
    list_display = ('user', '__str__')
    list_filter = ('user','created_at')
    search_fields = ('user','created_at')
    autocomplete_fields = ('user',)

@admin.register(DocumentoNotificacionCliente)
class DocumentoNotificacionClientesAdmin(admin.ModelAdmin):
    list_display = ('id','cliente', 'cuota','description','status','created_at')
    list_filter = ('cliente','cuota')
    search_fields = ('cliente','cuota')
    autocomplete_fields = ('cliente','cuota')

@admin.register(NotificationCustomer)
class NotificationCustomerClientesAdmin(admin.ModelAdmin):
    list_display = ('id','cliente', 'cuota','title','user','read','created_at')
    list_filter = ('cliente','user','read')
    search_fields = ('cliente','user')
    autocomplete_fields = ('cliente','user')