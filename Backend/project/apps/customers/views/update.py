from django.shortcuts import render, get_object_or_404, redirect

# Models
from apps.customers.models import Customer, CreditCounselor

# LIBRERIAS PARA CRUD
from django.views.generic.list import ListView
from django.db.models import Q

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import permiso_requerido
# Paginacion
from project.pagination import paginacion

# Formularios
from apps.customers.forms import CustomerForm

# MENSAJES
from django.contrib import messages

# SCRIPTS
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario


# ----- EDITAR INFORMACION PERSONAL DE UN CLIENTE ----- #

@login_required
@permiso_requerido('puede_editar_informacion_personal_cliente')
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
        'title': f'Actualizacion de Informacion para el cliente. {customer.customer_code}',
        'customer_code': customer.customer_code,
        'permisos':recorrer_los_permisos_usuario(request)
    }
    return render(request, template_name, context)