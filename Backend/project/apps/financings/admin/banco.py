# ADMIN
from django.contrib import admin

# MODELO
from apps.financings.models import Banco

@admin.register(Banco)
class BancoAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha', 'referencia','status')
    search_fields = ('referencia', 'status')
    list_filter = ('referencia', 'status')