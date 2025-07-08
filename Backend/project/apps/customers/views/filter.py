from django.shortcuts import render, get_object_or_404, redirect

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import permiso_requerido

# SCRIPTS
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario

@login_required
@permiso_requerido('puede_visualizar_el_registro_clientes')
def list_filters(request):
    template_name = 'customer/options.html'
    context = {
        'title':'EL TELAR / REPORTES - CLIENTES',
        'posicion':'Clientes',
        'permisos':recorrer_los_permisos_usuario(request)
    }

    return render(request, template_name, context)
