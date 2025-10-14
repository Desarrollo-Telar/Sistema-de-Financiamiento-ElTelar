from django.shortcuts import render

# Models
from apps.accountings.models import  Creditor


# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import  permiso_requerido


# Scripts
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario

# Paginacion
from project.pagination import paginacion



@login_required
@permiso_requerido('puede_ver_registro_acreedores')
def acreedores_cancelado(request):
    sucursal = request.session['sucursal_id']
    template_name = 'contable/acreedores/list.html'
    object_list = Creditor.objects.filter(is_paid_off=True, sucursal=sucursal).order_by('-id')
    page_obj = paginacion(request, object_list)
    
    context = {
        'title':'EL TELAR - ACREEDORES / ACREEDORES CANCELADOS',
        'page_obj':page_obj,
        'object_list':page_obj,
        'count':object_list.count(),
        'posicion':'Acreedores cancelados',
        'permisos':recorrer_los_permisos_usuario(request)
        
    }
        
    return render(request, template_name, context)

@login_required
@permiso_requerido('puede_ver_registro_acreedores')
def acreedores_atraso_aportacion(request):
    sucursal = request.session['sucursal_id']
    template_name = 'contable/acreedores/list.html'
    object_list = Creditor.objects.filter(estado_aportacion=False, sucursal=sucursal).order_by('-id')
    page_obj = paginacion(request, object_list)
    
    context = {
        'title':'EL TELAR - ACREEDORES / ACREEDORES ATRASO POR APORTACION',
        'page_obj':page_obj,
        'object_list':page_obj,
        'count':object_list.count(),
        'posicion':'Acreedores con atraso por aportacion',
        'permisos':recorrer_los_permisos_usuario(request)
        
    }
        
    return render(request, template_name, context)

@login_required
@permiso_requerido('puede_ver_registro_acreedores')
def acreedores_atraso_fechas(request):
    sucursal = request.session['sucursal_id']
    template_name = 'contable/acreedores/list.html'
    object_list = Creditor.objects.filter(estados_fechas=False, sucursal=sucursal).order_by('-id')
    page_obj = paginacion(request, object_list)
    
    context = {
        'title':'EL TELAR - ACREEDORES / ACREEDORES ATRASO POR FECHAS',
        'page_obj':page_obj,
        'object_list':page_obj,
        'count':object_list.count(),
        'posicion':'Acreedores con atraso por fechas',
        'permisos':recorrer_los_permisos_usuario(request)
    }
        
    return render(request, template_name, context)