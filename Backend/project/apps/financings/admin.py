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
    list_display = ('id', 'numero_referencia', 'estado_transaccion','monto','tipo_pago')
    search_fields = ('numero_referencia', 'estado_transaccion','tipo_pago','cliente__customer_code')
    list_filter = ('numero_referencia', 'estado_transaccion','tipo_pago', 'cliente__customer_code')

admin.site.register(Guarantees)
admin.site.register(DetailsGuarantees)

@admin.register(Disbursement)
class DisbursementAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__')


@admin.register(Banco)
class BancoAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha', 'referencia','status')
    search_fields = ('referencia', 'status')
    list_filter = ('referencia', 'status')

@admin.register(AccountStatement)
class AccountStatementAdmin(admin.ModelAdmin):
    search_fields = ('numero_referencia','payment__numero_referencia', 'credit__codigo_credito')
    list_filter = ('numero_referencia','payment__numero_referencia','credit__codigo_credito')

    list_display = ('id', 'numero_referencia')
    # Habilitar búsqueda en los campos relacionados
    autocomplete_fields = ('credit', 'payment','cuota')


@admin.register(Recibo)
class ReciboAdmin(admin.ModelAdmin):
    search_fields = ('pago__numero_referencia',)
    list_filter = ('pago__numero_referencia',)

    list_display = ('id', 'recibo', '__str__')
    # Habilitar búsqueda en los campos relacionados
    autocomplete_fields = ('cliente', 'pago', 'cuota')

    

admin.site.register(Invoice)
admin.site.register(Cuota)