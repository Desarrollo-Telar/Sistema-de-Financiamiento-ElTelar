from django.contrib import admin

from apps.financings.models import Credit, Guarantees, DetailsGuarantees, Disbursement, Banco, Payment
# Register your models here.
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
    )
    list_display = ('customer_id','codigo_credito' ,'tipo_credito', 'monto','plazo','tasa_interes','fecha_inicio','creation_date')



admin.site.register(Guarantees)
admin.site.register(DetailsGuarantees)
admin.site.register(Disbursement)
admin.site.register(Banco)
admin.site.register(Payment)