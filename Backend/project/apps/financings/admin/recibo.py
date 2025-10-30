# ADMIN
from django.contrib import admin

# MODELO
from apps.financings.models import Recibo

@admin.register(Recibo)
class ReciboAdmin(admin.ModelAdmin):
    search_fields = ('pago__numero_referencia',)
    list_filter = ('pago__numero_referencia','sucursal')

    list_display = ('id', 'recibo', 'interes_pagado','mora_pagada','pago','fecha','__str__')
    # Habilitar búsqueda en los campos relacionados
    autocomplete_fields = ('cliente', 'pago', 'cuota')