from django.shortcuts import render, get_object_or_404

# Models
from .models import Customer
from apps.addresses.models import Address
from apps.FinancialInformation.models import WorkingInformation, OtherSourcesOfIncome, Reference
from apps.InvestmentPlan.models import InvestmentPlan

# LIBRERIAS PARA CRUD
from django.views.generic import CreateView
from django.views.generic.list import ListView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic.detail import DetailView
from django.db.models import Q

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import usuario_activo
from django.utils.decorators import method_decorator

# Paginacion
from project.pagination import paginacion

# Formularios
from .forms import CustomerForm, ImmigrationStatus
from apps.addresses.forms import AddressForms
from apps.FinancialInformation.forms import WorkingInformationForms, OtherSourcesOfIncomeForms, ReferenceForms
from apps.InvestmentPlan.forms import InvestmentPlanForms

from django.apps import apps

# Create your views here.
# ----- LISTADO DE CLIENTES ----- #
@login_required
@usuario_activo
def list_customer(request):
    customer_list = Customer.objects.all().order_by('-id')
    page_obj = paginacion(request, customer_list)
    template_name = 'customer/list.html'
    context = {
        'title':'EL TELAR - CLIENTES',
        'page_obj':page_obj,
        'customer_list':customer_list,
    }
    return render(request, template_name, context)

# ----- CREANDO USUARIOS NUEVOS ----- #
@login_required
@usuario_activo
def add_customer(request):
    # Listado de formularios
    
    ime = ImmigrationStatus.objects.all()
    
    template_name = 'customer/add.html'
    print(request.user.id)
    context = {
        'title': 'EL TELAR - CLIENTES',
        
        'immigration_status':ime,
        'user_id':request.user.id,
        'accion':'Agregar',
    }
    return render(request, template_name, context)

# ----- BUSCAR CLIENTES ----- #
class CustomerSearch(ListView):
    template_name = 'customer/search.html'

    def get_queryset(self):
        try:
            # Asignar la consulta a una variable local
            query = self.query()
            
            # Definir los filtros utilizando Q objects
            filters = (
                Q(first_name__icontains=query) | 
                Q(customer_code__icontains=query) | 
                Q(last_name__icontains=query) | 
                Q(type_identification__icontains=query) |
                Q(gender__icontains=query)
            )
            
            # Filtrar los objetos Customer usando los filtros definidos
            return Customer.objects.filter(filters)
        except Exception as e:
            # Manejar cualquier excepción que ocurra y devolver un queryset vacío
            print(f"Error al filtrar el queryset: {e}")
            return Customer.objects.none()
    

    def query(self):
        return self.request.GET.get('q')
    
    @method_decorator(usuario_activo)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.query()
        context['title'] = 'ELTELAR - Buscar'
        context['count'] = context['customer_list'].count()
        

        return context

# ----- VER DETALLES DE UN CLIENTE ----- #
@login_required
@usuario_activo
def detail_customer(request,customer_code):
    template_name = 'customer/detail.html'
    customer_list = get_object_or_404(Customer,customer_code = str(customer_code))    
    informacion_laboral = WorkingInformation.objects.filter(Q(customer_id=customer_list))
    otra_informacion_laboral = OtherSourcesOfIncome.objects.filter(Q(customer_id=customer_list))
    direccion = Address.objects.filter(Q(customer_id=customer_list))
    plan_inversion = InvestmentPlan.objects.filter(Q(customer_id=customer_list))

    
    
    context = {
        'title': 'ELTELAR - {} {} / {}'.format(customer_list.first_name, customer_list.last_name,str(customer_code)),
        'customer_list':customer_list,
        'user_id':request.user.id,
    }
    return render(request, template_name, context)

# ----- VER FORMULARIO IVE ----- #
@login_required
@usuario_activo
def formulario_ive(request, id):
    template_name = 'customer/forms/forms_ive.html'
    customer_list = get_object_or_404(Customer, id=id)
    address_list = Address.objects.filter(Q(customer_id=customer_list))
    working_information = WorkingInformation.objects.filter(Q(customer_id=customer_list))
    other_information = OtherSourcesOfIncome.objects.filter(Q(customer_id=customer_list))
    reference = Reference.objects.filter(Q(customer_id=customer_list))
    plan = InvestmentPlan.objects.filter(Q(customer_id=customer_list))

    context = {
        'title':'EL TELAR - FORMULARIO IVE',
        'customer_list':customer_list,
        'address_list': address_list,  
        'working_information' :working_information,
        'other_information' :other_information,
        'reference':reference,
        'plan_list':plan,
        
        }
    return render(request, template_name, context)