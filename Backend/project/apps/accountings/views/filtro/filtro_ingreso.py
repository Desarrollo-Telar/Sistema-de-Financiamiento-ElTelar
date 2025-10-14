from django.shortcuts import render

# Models
from apps.accountings.models import  Income

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import  permiso_requerido


# Scripts
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario

# Paginacion
from project.pagination import paginacion



@login_required
@permiso_requerido('puede_ver_registro_ingresos')
def pendiente_ingresos_vincular(request):
    sucursal = request.session['sucursal_id']
    template_name = 'contable/ingresos/list.html'
    object_list = Income.objects.filter(status=False, sucursal=sucursal).order_by('-id')
    page_obj = paginacion(request, object_list)
    
    context = {
        'title':'Registro de Ingresos que estan Pendientes por Vincular',
        'page_obj':page_obj,
        'object_list':page_obj,
        'count':object_list.count(),
        'permisos':recorrer_los_permisos_usuario(request)
        
    }
        
    return render(request, template_name, context)

@login_required
@permiso_requerido('puede_ver_registro_ingresos')
def ingresos_vinculados(request):
    sucursal = request.session['sucursal_id']
    template_name = 'contable/ingresos/list.html'
    object_list = Income.objects.filter(status=False, sucursal=sucursal).order_by('-id')
    page_obj = paginacion(request, object_list)
    
    context = {
        'title':'Registro de Ingresos que estan Vinculados',
        'page_obj':page_obj,
        'object_list':page_obj,
        'count':object_list.count(),
        'permisos':recorrer_los_permisos_usuario(request)
        
    }
        
    return render(request, template_name, context)