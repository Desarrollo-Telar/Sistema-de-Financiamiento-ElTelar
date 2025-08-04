# formulario
from apps.actividades.forms.votaciones import VotacionClienteForm, VotacionCreditoForm

# URL
from django.shortcuts import render, get_object_or_404, redirect

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import usuario_activo, permiso_requerido
from django.utils.decorators import method_decorator

# Scripts
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario

# MENSAJES
from django.contrib import messages

# Modelos
from apps.customers.models import Customer

@login_required
def votar_cliente(request, customer_code):
    template_name = 'votacion/crear.html'
    cliente = Customer.objects.filter(customer_code=customer_code).first()
    if request.method == 'POST':
        form = VotacionClienteForm(request.POST)
        if form.is_valid():
            votacion = form.save(commit=False)
            votacion.cliente = cliente
            votacion.usuario = request.user
            votacion.save()
            messages.success(request, 'Registro Completado')
            return redirect('customers:detail',customer_code)
    else:
        form = VotacionClienteForm()

    context = {
        'form':form,
        'customer_code':customer_code
    }
    return render(request, template_name, context)