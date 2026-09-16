from django.db.models import Q
from apps.actividades.models import Notification
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from project.decorador import usuario_activo
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario
from project.pagination import paginacion

@login_required
@usuario_activo
def listar_notificaciones(request):
    template_name = 'notification/list.html'
    
    # Queryset base para el usuario actual
    queryset = Notification.objects.filter(user=request.user)
    
    # Parámetros de búsqueda y filtros
    query = request.GET.get('q', '').strip()
    categoria_filter = request.GET.get('categoria', '').strip()

    # 1. Búsqueda por texto (en title o message)
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) | Q(message__icontains=query)
        )

    # 2. Filtrado por categorías limpias usando Q anidados
    if categoria_filter == 'Gestión de Cobranza':
        queryset = queryset.filter(Q(title__icontains='cobranza'))
    elif categoria_filter == 'Boleta de Pago':
        queryset = queryset.filter(Q(title__icontains='alerta de boleta'))
    elif categoria_filter == 'Generación de Recibo':
        queryset = queryset.filter(Q(title__icontains='recibo'))
    elif categoria_filter == 'Crédito Nuevo':
        queryset = queryset.filter(Q(title__icontains='crédito nuevo') | Q(title__icontains='credito nuevo'))
    elif categoria_filter == 'Cliente Nuevo':
        queryset = queryset.filter(Q(title__icontains='cliente nuevo'))
    elif categoria_filter == 'Boleta de Pago de Cliente':
        queryset = queryset.filter(Q(title__icontains='ha subido su boleta de pago'))
    elif categoria_filter == 'Cuotas':
        queryset = queryset.filter(Q(title__icontains='cuotas'))

    # Ordenamiento final
    queryset = queryset.order_by('-created_at')

    # Total de registros tras filtros
    total_registros = queryset.count()

    # Paginación
    page_obj = paginacion(request, queryset)

    # Lista de categorías fijas para el selector del HTML
    categorias_disponibles = [
        'Gestión de Cobranza',
        'Boleta de Pago',
        'Generación de Recibo',
        'Crédito Nuevo',
        'Cliente Nuevo',
        'Boleta de Pago de Cliente',
        'Cuotas'
    ]

    context = {
        'title': 'Notificaciones',
        'object_list': page_obj,
        'page_obj': page_obj,
        'permisos': recorrer_los_permisos_usuario(request),
        'total_count': total_registros,
        'categorias_disponibles': categorias_disponibles,
        'request_q': query,
        'request_categoria': categoria_filter,
    }

    return render(request, template_name, context)