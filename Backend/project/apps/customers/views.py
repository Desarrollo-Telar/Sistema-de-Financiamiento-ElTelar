from django.shortcuts import render, get_object_or_404, redirect

# Models
from .models import Customer
from apps.addresses.models import Address
from apps.FinancialInformation.models import WorkingInformation, OtherSourcesOfIncome, Reference
from apps.InvestmentPlan.models import InvestmentPlan
from apps.pictures.models import ImagenCustomer
from apps.documents.models import DocumentCustomer
from apps.financings.models import Credit

# LIBRERIAS PARA CRUD
from django.views.generic import CreateView
from django.views.generic.list import ListView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic.detail import DetailView
from django.db.models import Q

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import usuario_activo, usuario_administrador, usuario_secretaria
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
@login_required
@usuario_activo
@usuario_administrador
def update_customer(request, customer_code):
    template_name = 'customer/update.html'
    customer = get_object_or_404(Customer, customer_code=str(customer_code))
        
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customers:detail', customer_code=customer.customer_code)
    else:
        form = CustomerForm(instance=customer)

    context = {
        'form': form,
        'title': f'ELTELAR - CLIENTE {customer.customer_code}',
        'customer_code': customer.customer_code
    }
    return render(request, template_name, context)


# ----- ELIMINACION DE CLIENTES ----- #
@login_required
@usuario_activo
def delete_customer(request,id):
    customer = get_object_or_404(Customer, id=id)
    customer.delete()
    return redirect('customers:customers')

@login_required
@usuario_activo
@usuario_administrador
def delete_customers(request,id):
    template_name ='customer/delete.html'
    customer = get_object_or_404(Customer, id=id)
    context = {
        'title':f'ELTELAR - CLIENTE {customer}',
        'customer':customer
    }
    if request.method == 'POST':
        customer.delete()
        return redirect('customers:customers')

    return render(request, template_name, context)

# ----- LISTADO DE CLIENTES ----- #
@login_required
@usuario_activo
@usuario_secretaria
def list_customer(request):
    status = ['Revisión de documentos', 'Aprobado', 'No Aprobado', 'Posible Cliente']
    customer_list = Customer.objects.all().order_by('-id').filter(status__in=status)
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
@usuario_secretaria
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
    
    @method_decorator([usuario_activo,  usuario_secretaria])
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
@usuario_secretaria
def detail_customer(request,customer_code):
    template_name = 'customer/detail.html'
    customer_list = get_object_or_404(Customer,customer_code = str(customer_code))    
    informacion_laboral = WorkingInformation.objects.filter(Q(customer_id=customer_list))
    otra_informacion_laboral = OtherSourcesOfIncome.objects.filter(Q(customer_id=customer_list))
    direccion = Address.objects.filter(Q(customer_id=customer_list))
    
    plan_inversion = InvestmentPlan.objects.filter(Q(customer_id=customer_list))
    reference = Reference.objects.filter(Q(customer_id=customer_list))
    imagen = ImagenCustomer.objects.filter(Q(customer_id=customer_list))
    document = DocumentCustomer.objects.filter(Q(customer_id=customer_list))
    credito = Credit.objects.filter(Q(customer_id =customer_list ))

    #print(credito)
      
    

    limite_direccion = False if direccion.count() >= 2 else True

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
        'credit_list':credito,
        'customer_code':customer_code,
        'limite_direccion':limite_direccion,
        'imagen':imagen,
        'document':document,
    }
    return render(request, template_name, context)

# ----- VER FORMULARIO IVE ----- #
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