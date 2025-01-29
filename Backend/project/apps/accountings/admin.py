from django.contrib import admin


# MODELOS
from apps.accountings.models import Creditor, Insurance
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