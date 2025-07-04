# ADMIN
from django.contrib import admin

# MODELO
from apps.financings.models import PaymentPlan

@admin.register(PaymentPlan)
class PaymentPlanAdmin(admin.ModelAdmin):
    search_fields = ('credit_id__codigo_credito','acreedor__codigo_acreedor', 'seguro__codigo_seguro')
    list_filter = ('credit_id__codigo_credito','acreedor__codigo_acreedor', 'seguro__codigo_seguro')
    autocomplete_fields = ('credit_id', 'acreedor','seguro')
    list_display = ('id', 'mes', '__str__','start_date','due_date')