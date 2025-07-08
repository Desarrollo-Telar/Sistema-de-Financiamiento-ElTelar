from django.shortcuts import render, get_object_or_404, redirect

# Models
from apps.customers.models import Customer

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import permiso_requerido, usuario_activo

# MENSAJES
from django.contrib import messages

# SCRIPTS
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario

# ----- ELIMINACION DE CLIENTES ----- #
@login_required
@usuario_activo
def delete_customer(request,id):
    customer = get_object_or_404(Customer, id=id)
    customer.delete()
    return redirect('customers:customers')

@login_required
@permiso_requerido('puede_eliminar_registro_cliente')
def delete_customers(request,id):
    template_name ='customer/delete.html'
    customer = get_object_or_404(Customer, id=id)
    context = {
        'title':f'Eliminar al Cliente. {customer}',
        'customer':customer,
        'permisos':recorrer_los_permisos_usuario(request)
    }
    if request.method == 'POST':
        customer.delete()
        messages.success(request,'CLIENTE ELIMINADO')
        return redirect('customers:customers')

    return render(request, template_name, context)