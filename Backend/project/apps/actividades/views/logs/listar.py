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
