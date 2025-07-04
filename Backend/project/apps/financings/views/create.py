from django.shortcuts import render, get_object_or_404, redirect

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import usuario_activo, permiso_requerido
from django.utils.decorators import method_decorator

# Scripts
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario

# Models
from apps.financings.models import Credit

# Create your views here.
### ------------------- CREAR ---------------------- ###


@login_required
@permiso_requerido('puede_crear_informacion_credito')
def create_credit(request):
    template_name = 'financings/credit/create.html'
    context = {
        'title':'Creacion de un Credito Nuevo.',
        'permisos':recorrer_los_permisos_usuario(request),
    }

    return render(request,template_name,context)

@login_required
@usuario_activo
def create_disbursement(request,id):
    credit_id = get_object_or_404(Credit, id=id)

    template_name = 'financings/disbursement/create.html'
    context = {
        'title':'Creacion de una Aplicacion de Desembolso.',
        'credit_id':credit_id,
        'permisos':recorrer_los_permisos_usuario(request),
    }

    return render(request,template_name,context)

@login_required
@usuario_activo
def create_guarantee(request):
    template_name = 'financings/guarantee/create.html'
    context = {
        'title':'Creacion de Garantia.',
        'permisos':recorrer_los_permisos_usuario(request),

    }

    return render(request,template_name,context)

