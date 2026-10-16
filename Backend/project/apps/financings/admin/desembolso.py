from django.contrib import admin

from apps.financings.models import Disbursement

@admin.register(Disbursement)
class DisbursementAdmin(admin.ModelAdmin):
    # 1. Mejora en la lista: Mostramos información clave y usamos tus funciones de formato
    list_display = (
        'id', 
        'credit_id', 
        'forma_desembolso', 
        'f_monto_total_desembolso', 
        'creation_date'
    )
    
    # 2. Filtros útiles (quitamos credit_id si son muchos registros para evitar listas gigantes)
    list_filter = ('forma_desembolso', 'creation_date')
    
    # 3. Búsqueda optimizada (puedes buscar por ID del desembolso o descripción)
    search_fields = ('id', 'description', 'forma_desembolso', 'credit_id__codigo_credito')
    
    # 4. Selector rápido por fecha en la parte superior
    date_hierarchy = 'creation_date'
    
    # 5. Optimización vital: Evita el problema de N+1 consultas al traer las Foreign Keys
    list_select_related = ('credit_id',)
    
    # 6. Autocompletado para relaciones grandes
    autocomplete_fields = ('credit_id',)
    
    # 7. Paginación limpia
    list_per_page = 25

    # 8. Organización visual de los campos dentro del formulario de detalle/edición
    fieldsets = (
        ('Información General', {
            'fields': ('credit_id', 'forma_desembolso', 'description')
        }),
        ('Desglose de Montos y Cálculos', {
            'fields': (
                'monto_credito', 
                'monto_credito_agregar', 
                'monto_credito_cancelar', 
                'saldo_anterior', 
                'honorarios', 
                'poliza_seguro', 
                'monto_desembolsado', 
                'total_gastos', 
                'monto_total_desembolso', 
                'total_t'
            ),
            'classes': ('collapse',), # Opcional: mantiene esta sección colapsada por defecto para no saturar la vista
        }),
        ('Auditoría', {
            'fields': ('creation_date',),
        }),
    )
    
    # Hacemos que la fecha de creación sea de solo lectura en el formulario
    readonly_fields = ('creation_date',)