# Models
from apps.actividades.models import DocumentoNotificacionCliente

# LIBRERIAS PARA CRUD
from django.views.generic.list import ListView
from django.db.models import Q



# Decoradores
from project.decorador import permiso_requerido
from django.utils.decorators import method_decorator

# MENSAJES
from django.contrib import messages

# TIEMPO
from datetime import datetime, timedelta

# URLS
from django.shortcuts import redirect

# SCRIPTS
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario


class DocumentoNotificacionClientesList(ListView):
    model = DocumentoNotificacionCliente
    template_name = 'customer/boletas_clientes/list.html'
    paginate_by = 50
 
    def get_queryset(self):
        try:
            # Asignar la consulta a una variable local
            query = self.query()

            # Crear una lista para almacenar los filtros
            filters = Q()
            

            if query:
                try:
                    fecha = datetime.strptime(query, '%Y-%m-%d')
                    fecha_inicio = datetime.combine(fecha.date(), datetime.min.time())
                    fecha_fin = datetime.combine(fecha.date(), datetime.max.time())
                    filters |= Q(created_at__range=(fecha_inicio, fecha_fin))
                except ValueError:
                    pass  # No es fecha válida, continúa con los otros filtros
                filters |= Q(status__icontains = query)
                filters |= Q(cliente__first_name__icontains = query)             
                filters |= Q(cliente__last_name__icontains = query)
                filters |= Q(cliente__customer_code__icontains = query)
                filters |= Q(cuota__credit_id__codigo_credito__icontains = query)


            return DocumentoNotificacionCliente.objects.filter(filters).order_by('-id')
        
        except Exception as e:
            print(f'error: {e}')
            
            return DocumentoNotificacionCliente.objects.all().order_by('-id')
    
    
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def query(self):
        return self.request.GET.get('q')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if not (context['object_list']):
            messages.error(self.request,'No se encontrado ningun dato')

        if self.query():
            context['query'] = self.query()
            
            
        consulta = self.query()
        if consulta is None:
            consulta = ''

        
        context['title'] = f'Boletas Subidas Por Clientes | {consulta}'
        context['count'] = context['object_list'].count()
        context['posicion'] = self.query() if self.query() else ''
        context['permisos'] = recorrer_los_permisos_usuario(self.request)
        context['usuario'] = self.request.user
        return context