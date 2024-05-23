from django.shortcuts import render

# Models
from .models import Customer

# Decoradores
from django.contrib.auth.decorators import login_required

# Paginacion
from project.pagination import paginacion

# Formularios
from .forms import CustomerForm
from apps.addresses.forms import AddressForms
from apps.FinancialInformation.forms import WorkingInformationForms, OtherSourcesOfIncomeForms



# Create your views here.
@login_required
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
def add_customer(request):
    # Listado de formularios
    form1 = CustomerForm
    form2 = WorkingInformationForms
    form3 = OtherSourcesOfIncomeForms
    template_name = 'customer/add.html'
    context = {
        'title': 'EL TELAR - CLIENTES',
        'form1':form1,
        'form2':form2,      
        'form3':form3,  
        'accion':'Agregar',
    }
    return render(request, template_name, context)