from django.shortcuts import render

# Models
from apps.accountings.models import  Insurance


# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import  permiso_requerido


# Scripts
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario

# Paginacion
from project.pagination import paginacion



@login_required
@permiso_requerido('puede_ver_registro_seguros')
def seguro_cancelado(request):
    template_name = 'contable/seguros/list.html'
    object_list = Insurance.objects.filter(is_paid_off=True).order_by('-id')
    page_obj = paginacion(request, object_list)

    context = {
        'title':'Registro de Seguros Cancelados.',
        'page_obj':page_obj,
        'object_list':page_obj,
        'count':object_list.count(),
        'posicion':'Seguros cancelados',
        'permisos':recorrer_los_permisos_usuario(request)
        
    }
        
    return render(request, template_name, context)

@login_required
@permiso_requerido('puede_ver_registro_seguros')
def seguros_atraso_aportacion(request):
    template_name = 'contable/seguros/list.html'
    object_list = Insurance.objects.filter(estado_aportacion=False).order_by('-id')
    page_obj = paginacion(request, object_list)

    context = {
        'title':'Registro de Seguros en Atraso Por Aportacion',
        'page_obj':page_obj,
        'object_list':page_obj,
        'count':object_list.count(),
        'posicion':'Seguros con atraso por aportacion',
        'permisos':recorrer_los_permisos_usuario(request)
        
    }
        
    return render(request, template_name, context)

@login_required
@permiso_requerido('puede_ver_registro_seguros')
def seguros_atraso_fechas(request):
    template_name = 'contable/seguros/list.html'
    object_list = Insurance.objects.filter(estados_fechas=False).order_by('-id')
    page_obj = paginacion(request, object_list)

    context = {
        'title':'Registro de Seguros en Atraso por Fechas',
        'page_obj':page_obj,
        'object_list':page_obj,
        'count':object_list.count(),
        'posicion':'Seguros con atraso por fechas',
        'permisos':recorrer_los_permisos_usuario(request)
    }
        
    return render(request, template_name, context)