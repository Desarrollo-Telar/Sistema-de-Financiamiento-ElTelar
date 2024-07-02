from django.shortcuts import render, get_object_or_404, redirect

# Models
from .models import Customer
from apps.addresses.models import Address, Coordinate
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

# ----- EDITAR INFORMACION PERSONAL DE UN CLIENTE ----- #
def update_customer(request, customer_code):
    template_name = 'customer/update.html'
    customer = get_object_or_404(Customer, customer_code=str(customer_code))
    print(customer.description, customer.immigration_status_id)
    
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            cliente = customer
            cliente.first_name = form.changed_data.get('first_name')
            cliente.last_name = form.changed_data.get('last_name')
            cliente.type_identification = form.changed_data.get('type_identification')
            cliente.identification_number = form.changed_data.get('identification_number')
            cliente.marital_status = form.changed_data.get('marital_status')
            cliente.nationality = form.changed_data.get('nationality')
            cliente.number_nit = form.changed_data.get('number_nit')
            cliente.date_birth = form.changed_data.get('date_birth')
            cliente.place_birth = form.changed_data.get('place_birth')
            cliente.gender = form.changed_data.get('gender')
            cliente.profession_trade = form.changed_data.get('profession_trade')
            cliente.person_type = form.changed_data.get('person_type')
            cliente.telephone = form.changed_data.get('telephone')
            cliente.email = form.changed_data.get('email')
            cliente.status = form.changed_data.get('status')
            cliente.description = form.changed_data.get('description')
            cliente.save()
            redirect('customers:detail',cliente.customer_code)
            

    else:

        initial_data_customer = {
            'first_name':customer.first_name,
            'last_name':customer.last_name,
            'type_identification':customer.type_identification,
            'identification_number':customer.identification_number,
            'marital_status':customer.marital_status,            
            'nationality':customer.nationality,
            'number_nit':customer.number_nit,
            'date_birth':customer.date_birth,
            'place_birth':customer.place_birth,
            'gender':customer.gender,
            'profession_trade':customer.profession_trade,
            'person_type':customer.person_type,
            'telephone':customer.telephone,
            'email':customer.email,
            'status':customer.status,  
            'description':customer.description,
            'immigration_status_id':customer.immigration_status_id,
        

        }
        form = CustomerForm(initial=initial_data_customer)
        context = {
            'form':form,
            'title':'ELTELAR - CLIENTE {}'.format(customer),
            'customer_code':customer.customer_code
        }
        return render(request, template_name, context)


# ----- ELIMINACION DE CLIENTES ----- #
@login_required
@usuario_activo
def delete_customer(request,id):
    customer = get_object_or_404(Customer, id=id)
    customer.delete()
    return redirect('customers:customers')

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
        'customer_list':page_obj,
        'count':customer_list.count(),
        
    }
    return render(request, template_name, context)

# ----- CREANDO USUARIOS NUEVOS ----- #
@login_required
@usuario_activo
def add_customer(request):     
    ime = ImmigrationStatus.objects.all()    
    template_name = 'customer/add.html'    
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
    reference = Reference.objects.filter(Q(customer_id=customer_list))
    coor = []        
    for dire in direccion:
        coordenada = Coordinate.objects.filter(Q(address_id=dire))
        coor.append(coordenada)

    context = {
        'title': 'ELTELAR - {} {} / {}'.format(customer_list.first_name, customer_list.last_name,str(customer_code)),
        'customer_list':customer_list,
        'user_id':request.user.id,
        'direccion': direccion,  
        'informacion_laboral' :informacion_laboral,
        'laboral':informacion_laboral.exists(),
        'otra':otra_informacion_laboral.exists(),
        'otra_informacion_laboral' :otra_informacion_laboral,
        'reference':reference,
        'plan_inversion':plan_inversion,
        'coordenada':coor,
        'customer_code':customer_code,
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
    plan = InvestmentPlan.objects.filter(Q(customer_id=customer_list)).first()

    context = {
        'title':'EL TELAR - FORMULARIO IVE',
        'customer_list':customer_list,
        'address_list': address_list,  
        'working_information' :working_information,
        'other_information' :other_information,
        'reference':reference,
        'plan':plan,
        
        }
    return render(request, template_name, context)