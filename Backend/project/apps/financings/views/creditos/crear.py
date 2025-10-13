from django.shortcuts import render, get_object_or_404, redirect

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import usuario_activo, permiso_requerido
from django.utils.decorators import method_decorator

# Scripts
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario

# Models
from apps.financings.models import Credit


@login_required
@permiso_requerido('puede_crear_informacion_credito')
def create_credit(request):

    template_name = 'financings/credit/create.html'

    sucursal = request.session['sucursal_id']

    context = {
        'title':'Creacion de un Credito Nuevo.',
        'sucursal_id':sucursal,
        'permisos':recorrer_los_permisos_usuario(request),
    }

    return render(request,template_name,context)