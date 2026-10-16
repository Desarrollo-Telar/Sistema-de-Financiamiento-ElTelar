from django.contrib import admin

from .models import Customer, ImmigrationStatus, CreditCounselor, Cobranza


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    # 1. Columnas a mostrar en la lista principal
    list_display = (
        'customer_code', 
        'first_name', 
        'last_name', 
        'identification_number', 
        'telephone', 
        'status', 
        'sucursal'
    )
    
    # 2. Búsqueda rápida optimizada
    search_fields = (
        'customer_code', 
        'identification_number', 
        'first_name', 
        'last_name', 
        'email', 
        'number_nit'
    )
    
    # 3. Filtros laterales limpios (Se eliminó customer_code para evitar listas gigantes)
    list_filter = (
        'status', 
        'type_identification', 
        'gender', 
        'person_type', 
        'sucursal'
    )
    
    # 4. Autocompletado para todas las relaciones foráneas del cliente
    autocomplete_fields = (
        'user_id', 
        'immigration_status_id', 
         
        
        'new_asesor_credito', 
        'sucursal'
    )
    
    # 5. Optimización SQL: Carga las relaciones de golpe
    list_select_related = (
        'user_id', 
        'immigration_status_id', 
         
        
        'new_asesor_credito', 
        'sucursal'
    )
    
    # 6. Paginación, orden y jerarquía de fechas
    list_per_page = 25
    ordering = ['-customer_code']
    date_hierarchy = 'creation_date'
    
    # 7. Organización de los campos en pestañas/secciones lógicas (fieldsets)
    fieldsets = (
        ('Información Personal y Básica', {
            'fields': (
               
                'first_name', 
                'last_name', 
                'person_type', 
                'gender', 
                'date_birth', 
                'place_birth', 
                'nationality', 
                'marital_status'
            )
        }),
        ('Identificación y Documentación', {
            'fields': (
                'type_identification', 
                'identification_number', 
                'fehca_vencimiento_de_tipo_identificacion',
                'lugar_emision_tipo_identificacion_departamento',
                'lugar_emision_tipo_identificacion_municipio',
                'number_nit', 
                'immigration_status_id'
            )
        }),
        ('Contacto y Ubicación', {
            'fields': (
                'telephone', 
                'other_telephone', 
                'email', 
                'sucursal', 
                'numero_identificacion_sucursal'
            )
        }),
        ('Información Laboral, Académica y Evaluación', {
            'fields': (
                'profession_trade', 
           
            )
        }),
        ('Asignación y Estado', {
            'fields': (
                'status', 
                'asesor', 
                'new_asesor_credito', 
                'user_id', 
                'description', 
                
            )
        }),
    )
    
    # Campos automáticos de solo lectura
    readonly_fields = ('creation_date', 'uuid')

    


@admin.register(ImmigrationStatus)
class ImmigrationStatusAdmin(admin.ModelAdmin):
    # 1. Columnas a mostrar en la lista principal
    list_display = (
        'id', 
        'condition_name', 
        'creation_date'
    )
    
    # 2. Obligatorio: Esto evita errores si otro modelo lo referencia en autocomplete_fields
    search_fields = (
        'condition_name', 
        'description'
    )
    
    # 3. Paginación y jerarquía de fechas
    list_per_page = 25
    date_hierarchy = 'creation_date'
    
    # 4. Organización del formulario de edición
    fields = (
        'condition_name', 
        'description', 
        'creation_date'
    )
    
    # Campo de solo lectura para la fecha de creación
    readonly_fields = ('creation_date',)



@admin.register(CreditCounselor)
class CreditCounselorAdmin(admin.ModelAdmin):
    # 1. Columnas a mostrar en la lista principal
    list_display = (
        'codigo_asesor', 
        'nombre', 
        'apellido', 
        'email', 
        'telephone', 
        'status', 
        'sucursal'
    )
    
    # 2. Obligatorio para el autocompletado en otros modelos (Créditos, Clientes, etc.)
    search_fields = (
        'codigo_asesor', 
        'nombre', 
        'apellido', 
        'identification_number', 
        'email'
    )
    
    # 3. Filtros laterales útiles
    list_filter = (
        'status', 
        'gender', 
        'type_identification', 
        'sucursal'
    )
    
    # 4. Autocompletado para sus llaves foráneas
    autocomplete_fields = (
        'usuario', 
        'sucursal'
    )
    
    # 5. Optimización SQL: Carga relaciones de golpe para evitar consultas lentas
    list_select_related = (
        'usuario', 
        'sucursal'
    )
    
    # 6. Paginación y navegación por fechas
    list_per_page = 25
    date_hierarchy = 'creation_date'
    
    # 7. Organización del formulario de edición en secciones limpias
    fieldsets = (
        ('Información Personal y Estado', {
            'fields': (
                'codigo_asesor', 
                'nombre', 
                'apellido', 
                'gender', 
                'status',
                'profile_pic'
            )
        }),
        ('Identificación y Contacto', {
            'fields': (
                'type_identification', 
                'identification_number', 
                'nit', 
                'email', 
                'telephone'
            )
        }),
        ('Asignación y Sucursal', {
            'fields': (
                'usuario', 
                'sucursal'
            )
        }),
        ('Fechas y Recordatorios', {
            'fields': (
                'fecha_actualizacion', 
                'recordatorio_clientes', 
                'creation_date'
            )
        }),
    )
    
    # Campos de solo lectura por seguridad
    readonly_fields = ('creation_date',)

admin.site.register(Cobranza)