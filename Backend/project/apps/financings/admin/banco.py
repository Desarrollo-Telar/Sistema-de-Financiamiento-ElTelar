# ADMIN
from django.contrib import admin

# MODELO
from apps.financings.models import Banco

@admin.register(Banco)
class BancoAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha', 'referencia','status','sucursal')
    search_fields = ('referencia', 'status','sucursal')
    list_filter = ('referencia', 'status','sucursal')