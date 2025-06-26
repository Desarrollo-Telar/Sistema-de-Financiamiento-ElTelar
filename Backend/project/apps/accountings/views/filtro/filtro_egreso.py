from django.shortcuts import render


# Models
from apps.accountings.models import  Egress


# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import  permiso_requerido


# Scripts
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario

# Paginacion
from project.pagination import paginacion

# TAREA ASINCRONICO
from apps.financings.tareas_ansicronicas import ver_caso_de_gastos


@login_required
@permiso_requerido('puede_ver_registro_egresos')
def pendiente_egresos_vincular(request):
    template_name = 'contable/egresos/list.html'
    object_list = Egress.objects.filter(status=False).order_by('-id')
    page_obj = paginacion(request, object_list)
    ver_caso_de_gastos()
    
    context = {
        'title':'Registro de Egresos que estan Pendientes por Vincular',
        'page_obj':page_obj,
        'object_list':page_obj,
        'count':object_list.count(),
        'permisos':recorrer_los_permisos_usuario(request)
        
    }
        
    return render(request, template_name, context)

@login_required
@permiso_requerido('puede_ver_registro_egresos')
def egresos_vinculados(request):
    template_name = 'contable/egresos/list.html'
    object_list = Egress.objects.filter(status=True).order_by('-id')
    page_obj = paginacion(request, object_list)

    context = {
        'title':'Registro de Egresos que se encuentran Vinculados',
        'page_obj':page_obj,
        'object_list':page_obj,
        'count':object_list.count(),
        'permisos':recorrer_los_permisos_usuario(request)
        
    }
        
    return render(request, template_name, context)