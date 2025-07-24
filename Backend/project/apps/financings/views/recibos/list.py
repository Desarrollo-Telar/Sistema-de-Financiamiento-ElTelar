# TIEMPO
from datetime import datetime, timedelta

# Models
from apps.financings.models import  Recibo

# Manejo de mensajes
from django.contrib import messages

# LIBRERIAS PARA CRUD
from django.views.generic.list import ListView
from django.db.models import Q

# Decoradores
from project.decorador import permiso_requerido
from django.utils.decorators import method_decorator

# Scripts
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario

# Paginacion
from project.pagination import paginacion

# LIBRERIAS PARA CRUD
from django.views.generic.list import ListView
from django.db.models import Q

class RecibosListView(ListView):
    template_name = 'financings/recibos/list.html'
    model=Recibo
    paginate_by = 75
    

    def get_queryset(self):
        try:
            # Asignar la consulta a una variable local
            query = self.query()

            # Crear una lista para almacenar los filtros
            filters = Q()
            # Filtro especial para Secretari@
            if self.request.user.rol.role_name == 'Secretari@':
                filters &= Q(pago__tipo_pago='CREDITO')

            if query:
                try:
                    fecha = datetime.strptime(query, '%Y-%m-%d')
                    fecha_inicio = datetime.combine(fecha.date(), datetime.min.time())
                    fecha_fin = datetime.combine(fecha.date(), datetime.max.time())

                    filters |= Q(fecha__range=(fecha_inicio, fecha_fin))
                except ValueError:
                    pass  # No es fecha válida, continúa con los otros filtros

                filters |= Q(recibo__icontains = query)
                filters |= Q(cliente__first_name__icontains = query)
                filters |= Q(cliente__last_name__icontains = query)
                filters |= Q(pago__numero_referencia__icontains = query)


            return Recibo.objects.filter(filters).order_by('-recibo')
        
        except Exception as e:
            print(f'error: {e}')
            
            return Recibo.objects.none()
    
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

        
        context['title'] = f'Recibos | {consulta}'
        context['count'] = context['object_list'].count()
        context['posicion'] = self.query() if self.query() else ''
        context['permisos'] = recorrer_los_permisos_usuario(self.request)
        return context
    

    

