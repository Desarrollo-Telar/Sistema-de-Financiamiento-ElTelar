# ADMIN
from django.contrib import admin

# MODELO
from apps.financings.models import Credit, CategoriaCreditoDemandado


@admin.register(Credit)
class CreditAdmin(admin.ModelAdmin):
    # 1. Columnas a mostrar en la lista principal
    list_display = (
        'id', 
        'codigo_credito', 
        'customer_id', 
        'tipo_credito', 
        'monto', 
        'saldo_actual', 
        'plazo', 
        'fecha_inicio', 
        'is_paid_off'
    )
    
    # 2. CORREGIDO: Ampliamos el search_fields para que el autocompletado funcione sin errores 
    # y te permita buscar por código, ID o nombre/código del cliente relacionado.
    search_fields = (
        'codigo_credito', 
        'numero_credito', 
        'customer_id__customer_code', 
        'customer_id__first_name' 
    )
    
    # 3. Filtros laterales útiles (evitamos campos numéricos directos)
    list_filter = (
        'tipo_credito', 
        'forma_de_pago', 
        'frecuencia_pago', 
        'is_paid_off', 
        'estado_judicial', 
        'sucursal'
    )
    
    # 4. Autocompletado para las llaves foráneas de Credit
    autocomplete_fields = (
        'customer_id', 
         
        'asesor_de_credito', 
        'sucursal', 
        'categoria_credito_demandado'
    )
    
    # 5. Optimización SQL: Carga las relaciones en una sola consulta
    list_select_related = (
        'customer_id', 
         
        'asesor_de_credito', 
        'sucursal', 
        'categoria_credito_demandado'
    )
    
    # 6. Paginación y navegación por fechas
    list_per_page = 25
    date_hierarchy = 'creation_date'
    
    # 7. Organización del formulario de edición mediante fieldsets lógicos
    fieldsets = (
        ('Información General del Crédito', {
            'fields': (
                'codigo_credito', 
                'numero_credito', 
                'customer_id', 
                'proposito', 
                'tipo_credito', 
               
            )
        }),
        ('Condiciones Financieras y Plazos', {
            'fields': (
                'monto', 
                'plazo', 
                'tasa_interes', 
                'forma_de_pago', 
                'frecuencia_pago', 
                'tasa_mora', 
                'plazo_gracia', 
                'fecha_finalizacion_gracia'
            )
        }),
        ('Fechas y Estados', {
            'fields': (
                'fecha_inicio', 
                'fecha_vencimiento', 
                'fecha_actualizacion', 
                'fecha_cancelacion', 
                'fecha_entrar_en_mora',
                'is_paid_off', 
             
                
                
            )
        }),
        ('Saldos y Control', {
            'fields': (
                'saldo_actual', 
                'saldo_pendiente', 
                'saldo_sin_modificar',               
                'excedente', 
                'estado_aportacion', 
                'estados_fechas', 
             
            ),
            'classes': ('collapse',), # Oculto por defecto para no saturar
        }),
        ('Asignación y Sucursal', {
            'fields': (
                'sucursal', 
                'asesor_de_credito',              
                'categoria_credito_demandado',
                
            )
        }),
    )
    
    # Campos de solo lectura por seguridad o automatización
    readonly_fields = ('creation_date',)




@admin.register(CategoriaCreditoDemandado)
class CategoriaCreditoDemandadoAdmin(admin.ModelAdmin):
    # 1. Columnas a mostrar en la lista principal
    list_display = (
        'id', 
        'titulo', 
        'creation_date'
    )
    
    # 2. Obligatorio: Esto evita errores si CreditAdmin lo referencia en autocomplete_fields
    search_fields = (
        'titulo', 
        'descripcion'
    )
    
    # 3. Paginación y jerarquía de fechas
    list_per_page = 25
    date_hierarchy = 'creation_date'
    
    # 4. Organización del formulario de edición
    fields = (
        'titulo', 
        'descripcion', 
       
    )
    
    # Campo de solo lectura para la fecha de creación automática
    readonly_fields = ('creation_date',)