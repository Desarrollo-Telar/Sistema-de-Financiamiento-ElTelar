# ADMIN
from django.contrib import admin

# MODELO
from apps.financings.models import Disbursement


@admin.register(Disbursement)
class DisbursementAdmin(admin.ModelAdmin):
    list_display = ('id','forma_desembolso', '__str__')
    list_filter = ('credit_id','forma_desembolso')
    search_fields = ('credit_id','forma_desembolso')
    autocomplete_fields = ('credit_id',)