# ADMIN
from django.contrib import admin

# MODELO
from apps.financings.models import Credit


@admin.register(Credit)
class CreditAdmin(admin.ModelAdmin):
    fields = (
        'proposito',
        'monto',
        'plazo',
        'tasa_interes',
        'forma_de_pago',
        'frecuencia_pago',
        'fecha_inicio',
        'fecha_vencimiento',
        'tipo_credito',        
        'customer_id',
        'estado_aportacion',
        'estados_fechas',
        'is_paid_off',
        'saldo_actual',
        'saldo_pendiente',
        'sucursal',
        'asesor_de_credito'
    )
    list_display = ('id','customer_id','codigo_credito' ,'tipo_credito', 'monto','plazo','tasa_interes','fecha_inicio','estados_fechas','creation_date','fecha_actualizacion')
    search_fields = ('codigo_credito',)
    list_filter = ('codigo_credito','sucursal')
    autocomplete_fields = ('customer_id', )
    date_hierarchy = 'creation_date'