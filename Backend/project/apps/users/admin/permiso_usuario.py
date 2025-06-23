# ADMIN
from django.contrib import admin

# MODELO
from apps.users.models import PermisoUsuario

@admin.register(PermisoUsuario)
class PermisoUsuarioAdministrador(admin.ModelAdmin):
    fields = ('user', 'permiso')
    search_fields = ('user__user_code', 'permiso__codigo_permiso')
    # Habilitar búsqueda en los campos relacionados
    autocomplete_fields = ('user', 'permiso')