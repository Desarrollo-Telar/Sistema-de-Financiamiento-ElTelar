from django.shortcuts import render

# Models
from .models import Customer

# Decoradores
from django.contrib.auth.decorators import login_required

# Paginacion
from project.pagination import paginacion

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