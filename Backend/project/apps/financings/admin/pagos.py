# ADMIN
from django.contrib import admin

# MODELO
from apps.financings.models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'numero_referencia', 'estado_transaccion','monto','tipo_pago','fecha_creacion')
    search_fields = ('numero_referencia', 'estado_transaccion','tipo_pago','cliente__customer_code','acreedor__codigo_acreedor')
    list_filter = ('numero_referencia', 'estado_transaccion','tipo_pago', 'cliente__customer_code','sucursal')
    autocomplete_fields = ('credit', 'disbursement','cliente','acreedor','seguro')