# URLS
from django.shortcuts import render, redirect

# TIEMPO
from datetime import datetime, timedelta

# Models
from apps.actividades.models import UserLog, SystemLog, LogCategory, LogLevel

# Manejo de mensajes
from django.contrib import messages

# LIBRERIAS PARA CRUD
from django.views.generic.list import ListView
from django.db.models import Q
from itertools import chain
from operator import attrgetter
# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import permiso_requerido
from django.utils.decorators import method_decorator

# Scripts
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario



from django.core.paginator import Paginator

@login_required
def listando_logs(request):
    template_name = "actividad/logs.html"

    # 1. Obtener parámetros de filtro de la URL (GET)
    nivel_id = request.GET.get("nivel")
    categoria_id = request.GET.get("categoria")

    # 2. Construir la consulta base (QuerySet diferido)
    system_log = SystemLog.objects.all()

    # 3. Aplicar filtros dinámicos si se enviaron valores válidos
    if nivel_id and nivel_id.isdigit():
        system_log = system_log.filter(level_id=nivel_id)

    if categoria_id and categoria_id.isdigit():
        system_log = system_log.filter(category_id=categoria_id)

    # 4. Ordenar del más reciente al más antiguo
    system_log = system_log.order_by("-id")

    # 5. Paginación directa sobre el QuerySet filtrado
    page_number = request.GET.get("page", 1)
    paginator = Paginator(system_log, 10)
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "logs_zip": page_obj.object_list,
        "permisos": recorrer_los_permisos_usuario(request),
        "niveles": LogLevel.objects.all(),
        "categorias": LogCategory.objects.all(),
        # Enviamos los filtros seleccionados para mantener el estado en los <select>
        "nivel_selected": nivel_id,
        "categoria_selected": categoria_id,
    }
    return render(request, template_name, context)





@login_required
def listando_user_logs(request):
    template_name = "actividad/user_logs.html"

    # Capturar parámetros de filtro
    search_query = request.GET.get("q", "").strip()
    categoria_id = request.GET.get("categoria", "").strip()

    # QuerySet base
    logs_qs = UserLog.objects.select_related("user", "category").order_by("-timestamp")

    # Filtro por término de búsqueda
    if search_query:
        logs_qs = logs_qs.filter(
            Q(user__username__icontains=search_query)
            | Q(user__first_name__icontains=search_query)
            | Q(user__last_name__icontains=search_query)
            | Q(action__icontains=search_query)
            | Q(details__icontains=search_query)
            | Q(ip_address__icontains=search_query)
        )

    # Filtro por Categoría
    if categoria_id and categoria_id.isdigit():
        logs_qs = logs_qs.filter(category_id=categoria_id)

    # Paginación
    page_number = request.GET.get("page", 1)
    paginator = Paginator(logs_qs, 15)
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "search_query": search_query,
        "categoria_selected": categoria_id,
        "categorias": LogCategory.objects.all(),
        "permisos": recorrer_los_permisos_usuario(request),
    }

    return render(request, template_name, context)


class ListandoLogs(ListView):
    template_name = 'actividad/logs.html'
    paginate_by = 20
    model = UserLog  # Solo por compatibilidad con ListView
    
    def query(self):
        return self.request.GET.get('q')

    def get_queryset(self):
        """
        Combina los registros de UserLog y SystemLog en un solo queryset
        ordenado por fecha.
        """
        user_logs = UserLog.objects.all()
        system_logs = SystemLog.objects.all()

        

        # Combinar resultados en memoria (eficiente si no son miles de registros)
        combined = sorted(
            chain(user_logs, system_logs),
            key=attrgetter('timestamp'),
            reverse=True
        )

        return combined
    
    def query(self):
        return self.request.GET.get('q')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posicion'] = self.query() if self.query() else ''
        context['permisos'] = recorrer_los_permisos_usuario(self.request)
        context['titulo'] = "Bitácora del Sistema"
        return context
