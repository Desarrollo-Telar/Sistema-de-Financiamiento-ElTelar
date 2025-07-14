from django.contrib import admin

from .models import Code, TokenCliente
# Register your models here.

#admin.site.register(Code)
@admin.register(TokenCliente)
class TokenClienteAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'cliente')
    list_filter = ('uuid', 'cliente')
    search_fields = ('uuid', 'cliente')
    autocomplete_fields = ('cliente', 'cuota')