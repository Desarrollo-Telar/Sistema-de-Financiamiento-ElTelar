from django.shortcuts import render

# Models
from .models import Customer

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import usuario_activo

# Paginacion
from project.pagination import paginacion

# Formularios
from .forms import CustomerForm, ImmigrationStatus
from apps.addresses.forms import AddressForms
from apps.FinancialInformation.forms import WorkingInformationForms, OtherSourcesOfIncomeForms, ReferenceForms
from apps.InvestmentPlan.forms import InvestmentPlanForms



# Create your views here.
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