# ADMIN
from django.contrib import admin

# MODELO
from apps.financings.models import Banco

# Acciones
from .acciones import cambiar_sucursal_1, cambiar_sucursal_2

@admin.register(Banco)
class BancoAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha', 'referencia','status','sucursal')
    search_fields = ('referencia', 'status')
    list_filter = ('referencia', 'status','sucursal')
    actions = [cambiar_sucursal_1, cambiar_sucursal_2 ]