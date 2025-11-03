
# Models
from apps.customers.models import Customer, CreditCounselor
from apps.subsidiaries.models import Subsidiary

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
class CustomerFiltro(ListView):
    template_name = 'customer/list.html'
    

    def get_queryset(self):
        try:
            # Asignar la consulta a una variable local
            query = self.query()
            gender = self.genero()
            incompleto = self.falta_informacion()
            status = self.status()
            sucursal = self.sucursal()
            request = self.request

            filters = Q()

            asesor_autenticado = CreditCounselor.objects.filter(usuario=request.user).first()

            if status == 'Falta de Informacion':
                status = None
                incompleto = 'incompleto'


            if query:                
                filters |= Q(first_name__icontains=query) 
                filters |= Q(customer_code__icontains=query)
                filters |= Q(last_name__icontains=query)
                filters |= Q(type_identification__icontains=query)
            
            if gender:
                filters |= Q(gender__icontains=gender)

            if incompleto:
                filters |= Q(completado=False)
            
            if status:

                if status == 'Clientes Dados de Baja':
                    status = 'Dar de Baja'
                filters |= Q(status__icontains=status)
            
            if sucursal:
                filters |= Q(sucursal__nombre__icontains=sucursal)
            
            if asesor_autenticado and request.user.rol.role_name == 'Asesor de Crédito':
                filters &= Q(new_asesor_credito=asesor_autenticado) 


 
            # Filtrar los objetos Customer usando los filtros definidos
            return Customer.objects.filter(filters).order_by('-id')
        except Exception as e:
            # Manejar cualquier excepción que ocurra y devolver un queryset vacío
            print(f"Error al filtrar el queryset: {e}")
            
            return Customer.objects.none()
    

    def query(self):
        return self.request.GET.get('q')
    
    def genero(self):
        return self.request.GET.get('gender')
    
    def falta_informacion(self):
        return self.request.GET.get('incompleto')
    
    def status(self):
        return self.request.GET.get('status')
    
    def sucursal(self):
        return self.request.GET.get('sucursal')
    
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not (context['object_list']):
            messages.error(self.request,'No se encontrado ningun dato')

        status = ['Revisión de documentos', 'Aprobado', 'No Aprobado', 'Posible Cliente', 'Clientes Dados de Baja', 'Falta de Informacion']
        context['query'] = self.query() if self.query() else ''
        context['gender'] = self.genero() if self.genero() else ''
        context['incompleto'] = self.falta_informacion() if self.falta_informacion() else ''
        context['status'] = self.status() if self.status() else ''
        context['sucursal'] = self.sucursal() if self.sucursal() else ''

        context['title'] = f'Consulta de Clientes.'
        context['count'] = context['customer_list'].count()
        context['posicion'] = self.query() if self.query() else ''
        context['permisos'] = recorrer_los_permisos_usuario(self.request)
        context['sucursales'] = Subsidiary.objects.filter(activa=True).order_by('id')
        context['status'] = status 
        

        return context