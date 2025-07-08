
# Models
from apps.customers.models import Customer

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

# ----- BUSCAR CLIENTES ----- #
class CustomerSearch(ListView):
    template_name = 'customer/list.html'
    paginate_by = 25

    def get_queryset(self):
        try:
            # Asignar la consulta a una variable local
            query = self.query()

            filters = Q()


            # Definir los filtros utilizando Q objects
            filters |= Q(first_name__icontains=query) 
            filters |= Q(customer_code__icontains=query)
            filters |= Q(last_name__icontains=query)
            filters |= Q(type_identification__icontains=query)
            filters |= Q(gender__icontains=query)

 
            # Filtrar los objetos Customer usando los filtros definidos
            return Customer.objects.filter(filters)
        except Exception as e:
            # Manejar cualquier excepción que ocurra y devolver un queryset vacío
            print(f"Error al filtrar el queryset: {e}")
            
            return Customer.objects.none()
    

    def query(self):
        return self.request.GET.get('q')
    
    @method_decorator([permiso_requerido('puede_realizar_consultar_de_clientes')])
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not (context['object_list']):
            messages.error(self.request,'No se encontrado ningun dato')
        context['query'] = self.query()
        context['title'] = f'Consulta de Clientes. {self.query()}'
        context['count'] = context['customer_list'].count()
        context['posicion'] = self.query() 
        context['permisos'] = recorrer_los_permisos_usuario(self.request)
        

        return context