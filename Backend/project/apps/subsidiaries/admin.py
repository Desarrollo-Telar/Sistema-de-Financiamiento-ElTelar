from django.contrib import admin
from .models import Subsidiary

@admin.register(Subsidiary)
class SubsidiaryAdmin(admin.ModelAdmin):
    # 1. Columnas a mostrar en la lista principal
    list_display = (
        'id',
        'codigo_sucursal', 
        'nombre', 
        'numero_telefono', 
        'activa', 
        'fecha_apertura'
    )
    
    # 2. Obligatorio: Esto soluciona el error E040 para que funcione el autocompletado en los demás modelos
    search_fields = (
        'codigo_sucursal', 
        'nombre', 
        'numero_telefono', 
        'codigo_establecimiento'
    )
    
    # 3. Filtros laterales útiles
    list_filter = (
        'activa', 
        'fecha_apertura', 
        'nombre_banco'
    )
    
    # 4. Paginación y navegación
    list_per_page = 25
    date_hierarchy = 'creation_date'
    
    # 5. Organización del formulario de edición en secciones limpias
    fieldsets = (
        ('Información General', {
            'fields': (
                'codigo_sucursal', 
                'nombre', 
                'activa', 
                'fecha_apertura', 
                'descripcion'
            )
        }),
        ('Contacto y Ubicación', {
            'fields': (
                'numero_telefono', 
                'otro_numero_telefono', 
                'codigo_postal', 
                'codigo_establecimiento'
            )
        }),
        ('Información Bancaria', {
            'fields': (
                'nombre_banco', 
                'numero_de_cuenta_banco'
            )
        }),
        ('Auditoría', {
            'fields': (
                'creation_date',
            )
        }),
    )
    
    # Campo de solo lectura para la fecha de creación
    readonly_fields = ('creation_date',)