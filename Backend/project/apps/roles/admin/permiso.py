# ADMIN
from django.contrib import admin

# MODELO
from apps.roles.models import Permiso, CategoriaPermiso

@admin.register(Permiso)
class PermisoAdministrador(admin.ModelAdmin):
    fields = (
        'nombre',
        'categoria_permiso',
        'descripcion',        
        'codigo_permiso'
        )
    search_fields = ('nombre', 'codigo_permiso','categoria_permiso')
    autocomplete_fields = ('categoria_permiso', )
    list_display = ('categoria_permiso', 'nombre','codigo_permiso','fecha_registro')
    list_filter = ('categoria_permiso',)
    ordering = ['categoria_permiso']
    list_per_page = 25

@admin.register(CategoriaPermiso)
class CategoriaPermisoAdmin(admin.ModelAdmin):
    fields = (
        'nombre',
        'descripcion'
    )
    list_display = ('nombre', 'estado', 'descripcion')
    list_filter = ('nombre',)
    search_fields = ('nombre',)
    list_per_page = 25