from django.shortcuts import render

# Models
from .models import Customer

# Decoradores
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def list_customer(request):
    template_name = 'customer/list.html'
    context = {
        'title':'EL TELAR - CLIENTES',
    }
    return render(request, template_name, context)