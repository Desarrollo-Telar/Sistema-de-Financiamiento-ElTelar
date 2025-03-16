from django.contrib import admin

from apps.financings.models import Credit, Guarantees, DetailsGuarantees, Disbursement, Banco, Payment, AccountStatement, PaymentPlan, Recibo
# Register your models here.
from apps.financings.models import Invoice, Cuota
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
        'saldo_actual'
    )
    list_display = ('id','customer_id','codigo_credito' ,'tipo_credito', 'monto','plazo','tasa_interes','fecha_inicio','estados_fechas','creation_date')
    search_fields = ('codigo_credito',)
    list_filter = ('codigo_credito',)

@admin.register(PaymentPlan)
class PaymentPlanAdmin(admin.ModelAdmin):
    search_fields = ('credit_id__codigo_credito','acreedor__codigo_acreedor', 'seguro__codigo_seguro')
    list_filter = ('credit_id__codigo_credito','acreedor__codigo_acreedor', 'seguro__codigo_seguro')

    list_display = ('id', 'mes', '__str__')
    
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'numero_referencia', 'estado_transaccion','monto')
    search_fields = ('numero_referencia', 'estado_transaccion')
    list_filter = ('numero_referencia', 'estado_transaccion')

admin.site.register(Guarantees)
admin.site.register(DetailsGuarantees)

@admin.register(Disbursement)
class DisbursementAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__')

admin.site.register(Banco)
admin.site.register(AccountStatement)

admin.site.register(Recibo)
admin.site.register(Invoice)
admin.site.register(Cuota)