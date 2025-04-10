from django.contrib import admin
from django.contrib import messages

# MODELOS
from apps.accountings.models import Creditor, Insurance, Income, Egress
# Register your models here.

@admin.register(Creditor)
class CreditorAdmin(admin.ModelAdmin):
    fields = (
        'nombre_acreedor',
        'fecha_inicio',
        'monto',
        'tasa',
        'plazo',
        'numero_referencia',
        'observaciones',
        'boleta',
        'fecha_vencimiento',
    )

    list_display = ('id', 'nombre_acreedor', 'codigo_acreedor','monto','plazo','tasa','fecha_registro')

@admin.register(Insurance)
class InsuranceAdmin(admin.ModelAdmin):
    fields = (
        'nombre_acreedor',
        'fecha_inicio',
        'monto',
        'tasa',
        'plazo',
        'numero_referencia',
        'observaciones',
        'boleta',
        'fecha_vencimiento',
    )

    list_display = ('id', 'nombre_acreedor', 'codigo_seguro','monto','plazo','tasa','fecha_registro')


@admin.action(description='Cambiando el status a completado')
def marcar_completado(modeladmin, request, queryset):
    updated = queryset.update(status=True) 
    modeladmin.message_user(request, f'{updated} status cambiados a completados.', messages.SUCCESS)

@admin.action(description='Cambiando el status a pendiente')
def marcar_pendiente(modeladmin, request, queryset):
    updated = queryset.update(status=False) 
    modeladmin.message_user(request, f'{updated} status cambiados a pendientes.', messages.SUCCESS)

@admin.register(Egress)
class EgressAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha', 'fecha_doc_fiscal','status','numero_referencia')
    search_fields = ('status','numero_referencia')
    list_filter = ('status','numero_referencia')
    actions = [marcar_completado, marcar_pendiente]

admin.site.register(Income)