
# Models
from apps.customers.models import Customer, CreditCounselor

# LIBRERIAS PARA CRUD
from django.views.generic.list import ListView
from django.db.models import Q

# Decoradores
from project.decorador import permiso_requerido
from django.utils.decorators import method_decorator

# MENSAJES
from django.contrib import messages


# SCRIPTS
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario

class AsesoresCreditosList(ListView):
    model = CreditCounselor
    template_name = 'asesores_credito/list.html'
    paginate_by = 50

    def query(self):
        return self.request.GET.get('q')
    
    def get_queryset(self):
        try:
            # Asignar la consulta a una variable local
            query = self.query()

            # Crear una lista para almacenar los filtros
            filters = Q()
            

            if query:
               

                filters |= Q(usuario__username__icontains = query)
                filters |= Q(nombre__icontains = query)
                filters |= Q(apellido__last_name__icontains = query)
                filters |= Q(usuario__user_code__icontains = query)


            return CreditCounselor.objects.filter(filters).order_by('id')
        
        except Exception as e:
            print(f'error: {e}')
            
            return CreditCounselor.objects.none()
    
    @method_decorator([permiso_requerido('puede_ver_registros_asesores')])
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if not (context['object_list']):
            messages.error(self.request,'No se encontrado ningun dato')

        if self.query():
            context['query'] = self.query()
            
            
        consulta = self.query()
        if consulta is None:
            consulta = ''

        
        context['title'] = f'Asesores de Creditos | {consulta}'
        context['count'] = context['object_list'].count()
        context['posicion'] = self.query() if self.query() else ''
        context['permisos'] = recorrer_los_permisos_usuario(self.request)
        return context