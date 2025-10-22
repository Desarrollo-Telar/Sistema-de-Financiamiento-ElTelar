# URLS
from django.shortcuts import render, redirect

# TIEMPO
from datetime import datetime, timedelta

# Models
from apps.actividades.models import UserLog, SystemLog

# Manejo de mensajes
from django.contrib import messages

# LIBRERIAS PARA CRUD
from django.views.generic.list import ListView
from django.db.models import Q
from itertools import chain
from operator import attrgetter
# Decoradores
from project.decorador import permiso_requerido
from django.utils.decorators import method_decorator

# Scripts
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario



from django.core.paginator import Paginator


def listando_logs(request):
    template_name = 'actividad/logs.html'

    # Obtén los registros
    user_log = list(UserLog.objects.all().order_by('-id'))
    system_log = list(SystemLog.objects.all().order_by('-id'))

    # Combina ambos — zip devuelve pares
    logs_zip = list(zip(user_log, system_log))

    # --- PAGINACIÓN ---
    page_number = request.GET.get('page', 1)  # página actual
    paginator = Paginator(logs_zip, 150)  # 20 pares por página

    # Obtén los registros de la página actual
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'logs_zip': page_obj.object_list,  # opcional, si quieres usar este nombre en el template
        'permisos': recorrer_los_permisos_usuario(request)
    }
    return render(request, template_name, context)



class ListandoLogs(ListView):
    template_name = 'actividad/logs.html'
    paginate_by = 50
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
