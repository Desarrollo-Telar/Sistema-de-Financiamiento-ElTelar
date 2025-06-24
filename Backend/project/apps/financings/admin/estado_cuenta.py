# ADMIN
from django.contrib import admin

# MODELO
from apps.financings.models import AccountStatement

@admin.register(AccountStatement)
class AccountStatementAdmin(admin.ModelAdmin):
    search_fields = ('numero_referencia','payment__numero_referencia', 'credit__codigo_credito')
    list_filter = ('numero_referencia','payment__numero_referencia','credit__codigo_credito')

    list_display = ('id', 'numero_referencia','description')
    # Habilitar búsqueda en los campos relacionados
    autocomplete_fields = ('credit', 'payment','cuota','disbursement','acreedor','seguro')