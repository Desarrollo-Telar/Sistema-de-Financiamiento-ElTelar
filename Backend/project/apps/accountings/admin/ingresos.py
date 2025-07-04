# ADMIN
from django.contrib import admin

# MODELOS
from apps.accountings.models import Income

# ACCIONES
from .acciones import marcar_completado, marcar_pendiente


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha', 'monto','codigo_ingreso','numero_referencia')
    
    search_fields = ('status','numero_referencia','codigo_ingreso')
    list_filter = ('status','numero_referencia','codigo_ingreso')
    actions = [marcar_completado, marcar_pendiente]