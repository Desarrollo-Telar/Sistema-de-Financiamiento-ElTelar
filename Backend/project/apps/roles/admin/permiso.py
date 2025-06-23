# ADMIN
from django.contrib import admin

# MODELO
from apps.roles.models import Permiso

@admin.register(Permiso)
class PermisoAdministrador(admin.ModelAdmin):
    fields = (
        'nombre',
        'codigo_permiso',
        'descripcion',        
        'estado'
        )
    search_fields = ('nombre','codigo_permiso')