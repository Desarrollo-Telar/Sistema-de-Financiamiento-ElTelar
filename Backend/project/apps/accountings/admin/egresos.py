# ADMIN
from django.contrib import admin

# MODELOS
from apps.accountings.models import Egress

# ACCIONES
from .acciones import marcar_completado, marcar_pendiente


@admin.register(Egress)
class EgressAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha', 'fecha_doc_fiscal','status','numero_referencia')
    search_fields = ('status','numero_referencia','codigo_egreso')
    list_filter = ('status','numero_referencia')
    actions = [marcar_completado, marcar_pendiente]