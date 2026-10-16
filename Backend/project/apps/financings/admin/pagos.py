from django.contrib import admin
from apps.financings.models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    # 1. Columnas a mostrar en la lista principal
    list_display = (
        'id', 
        'numero_referencia', 
        'tipo_pago', 
        'monto', 
        'estado_transaccion', 
        'cliente', 
        'sucursal', 
        'fecha_creacion'
    )
    
    # 2. Búsqueda optimizada abarcando referencias, estados y códigos relacionados
    search_fields = (
        'numero_referencia', 
        
        'descripcion'
    )
    
    # 3. Filtros laterales limpios (Se eliminó numero_referencia y customer_code para evitar listas gigantes)
    list_filter = (
        'estado_transaccion', 
        'tipo_pago', 
        'registro_ficticio', 
        'sucursal', 
        'fecha_creacion'
    )
    
    # 4. Autocompletado para todas las llaves foráneas y evitar sobrecarga de selects
    autocomplete_fields = (
        'credit', 
        'disbursement', 
        'cliente', 
        'acreedor', 
        'seguro', 
        'sucursal'
    )
    
    # 5. Optimización de rendimiento para consultas SQL (Evita el problema N+1)
    list_select_related = (
        'credit', 
        'disbursement', 
        'cliente', 
        'acreedor', 
        'seguro', 
        'sucursal'
    )
    
    # 6. Paginación y navegación por fecha
    list_per_page = 25
    date_hierarchy = 'fecha_creacion'
    
    # 7. Organización del formulario de edición mediante fieldsets
    fieldsets = (
        ('Información Principal', {
            'fields': (
                'numero_referencia', 
                'tipo_pago', 
                'estado_transaccion', 
                'descripcion_estado',
                'monto', 
                'registro_ficticio'
            )
        }),
        ('Relaciones y Origen', {
            'fields': (
                'credit', 
                'disbursement', 
                'cliente', 
                'acreedor', 
                'seguro', 
                'sucursal'
            )
        }),
        ('Desglose Financiero', {
            'fields': (
                'capital', 
                'capital_generado', 
                'interes', 
                'interes_generado', 
                'mora'
            ),
            'classes': ('collapse',), # Oculto por defecto para mantener la interfaz limpia
        }),
        ('Documentación y Fechas', {
            'fields': (
                'boleta', 
                'descripcion', 
                'fecha_emision', 
                'fecha_creacion', 
                'creation_date'
            )
        }),
    )
    
    # Campos automáticos de solo lectura
    readonly_fields = ('fecha_creacion', 'creation_date')