# ADMIN
from django.contrib import admin

# MODELOS
from apps.accountings.models import Creditor


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
        'is_paid_off',
        'estado_aportacion',
        'estados_fechas',
        'saldo_actual'
    )
    search_fields = ('codigo_acreedor', 'nombre_acreedor')
    list_display = ('id', 'nombre_acreedor', 'codigo_acreedor','monto','plazo','tasa','fecha_registro')