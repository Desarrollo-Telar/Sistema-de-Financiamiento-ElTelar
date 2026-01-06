# URLS
from django.shortcuts import render, redirect

# TIEMPO
from datetime import datetime, timedelta

# Models
from apps.actividades.models import InformeDiarioSistema

# Manejo de mensajes
from django.contrib import messages

# LIBRERIAS PARA CRUD
from django.views.generic.list import ListView
from django.db.models import Q
from itertools import chain
from operator import attrgetter
# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import permiso_requerido, usuario_activo
from django.utils.decorators import method_decorator

# Scripts
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario



from django.core.paginator import Paginator

@login_required
@usuario_activo
def listar_cierre_diario(request):
    template_name = 'cierre_diario/reportes_cierre.html'
    context = {
        'permisos': recorrer_los_permisos_usuario(request),
    }
    return render(request, template_name, context)

class ListarCierreDiario(ListView):
    template_name = 'cierre_diario/reportes_cierre.html'
    def get_queryset(self):
        try:
            sucursal = self.request.session['sucursal_id']
            # Asignar la consulta a una variable local
            query = self.query()

            # Crear una lista para almacenar los filtros
            filters = Q()

            # Añadir filtros si la consulta no está vacía
            if query:
                try:
                    fecha = datetime.strptime(query, '%Y-%m-%d')
                    fecha_inicio = datetime.combine(fecha.date(), datetime.min.time())
                    fecha_fin = datetime.combine(fecha.date(), datetime.max.time())
                    filters |= Q(fecha_registro__range=(fecha_inicio, fecha_fin))
                except ValueError:
                    pass  # No es fecha válida, continúa con los otros filtros

                # Filtrar los objetos Customer usando los filtros definidos
            return InformeDiarioSistema.objects.filter(filters, sucursal=sucursal).order_by('-id')
            
        except Exception as e:
            # Manejar cualquier excepción que ocurra y devolver un queryset vacío
            print(f"Error al filtrar el queryset: {e}")
            return InformeDiarioSistema.objects.filter( sucursal=sucursal).order_by('-id')
        
    def query(self):
        return self.request.GET.get('q')
    
    @method_decorator(usuario_activo)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
       

        context['query'] = self.query() if self.query() else ''
        context['title'] = f'Cierre Diario | {self.query() if self.query() else ''}'
        
        context['posicion'] = self.query() if self.query() else ''
        context['permisos'] = recorrer_los_permisos_usuario(self.request)
        return context