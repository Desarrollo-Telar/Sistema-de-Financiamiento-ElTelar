from django.shortcuts import render

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import permiso_requerido

# Scripts
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario

@login_required
@permiso_requerido('puede_crear_boleta_pago')
def create_payment(request):
    template_name = 'financings/payment/create.html'
    context = {
        'title':'Creacion de Boleta Nueva',
        'permisos':recorrer_los_permisos_usuario(request),
    }
    return render(request, template_name, context)