from django.shortcuts import render

# Models
from apps.accountings.models import Creditor, Insurance,  Egress, Income

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import permiso_requerido, usuario_activo
from django.utils.decorators import method_decorator

# Paginacion
from project.pagination import paginacion

# TAREA ASINCRONICO
from apps.financings.tareas_ansicronicas import ver_caso_de_gastos

# Scripts
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario

# Create your views here.
@login_required
@permiso_requerido('puede_ver_registro_acreedores')
def list_acreedores(request):
    template_name = 'contable/acreedores/list.html'
    acreedores_list = Creditor.objects.all().order_by('-id')
    page_obj = paginacion(request, acreedores_list)
    context = {
        'title':'Registro de Acreedores',
        'page_obj':page_obj,
        'acreedores_list':page_obj,
        'count':acreedores_list.count(),
        'posicion':'Todos los Acreedores',
        'permisos':recorrer_los_permisos_usuario(request),
        
    }
        
    return render(request, template_name, context)

@login_required
@permiso_requerido('puede_ver_registro_seguros')
def list_seguros(request):
    template_name = 'contable/seguros/list.html'
    object_list = Insurance.objects.all().order_by('-id')
    page_obj = paginacion(request, object_list)
    context = {
        'title':'Registro de Seguros',
        'page_obj':page_obj,
        'object_list':page_obj,
        'count':object_list.count(),
        'posicion':'Todos los Seguros',
        'permisos':recorrer_los_permisos_usuario(request),
        
    }
        
    return render(request, template_name, context)

@login_required
@permiso_requerido('puede_ver_registro_ingresos')
def list_ingresos(request):
    template_name = 'contable/ingresos/list.html'
    object_list = Income.objects.all().order_by('-id')
    page_obj = paginacion(request, object_list)
    context = {
        'title':'Registro de Ingresos',
        'page_obj':page_obj,
        'object_list':page_obj,
        'count':object_list.count(),
        'posicion':'Todos los Ingresos',
        'permisos':recorrer_los_permisos_usuario(request),
        
    }
        
    return render(request, template_name, context)

@login_required
@permiso_requerido('puede_ver_registro_egresos')
def list_egresos(request):
    template_name = 'contable/egresos/list.html'
    object_list = Egress.objects.all().order_by('-id')
    page_obj = paginacion(request, object_list)
    
    ver_caso_de_gastos()

    context = {
        'title':'Registro de Egresos',
        'page_obj':page_obj,
        'object_list':page_obj,
        'count':object_list.count(),
        'posicion':'Todos los Egresos',
        'permisos':recorrer_los_permisos_usuario(request),
        
    }
        
    return render(request, template_name, context)

@login_required
@usuario_activo
def list_modulos(request):
    template_name = 'contable/options.html'
    
    context = {
        'title':'EL TELAR - MODULOS CONTABLES',
        'acreedores':Creditor.objects.filter(is_paid_off=False),
        'seguros':Insurance.objects.filter(is_paid_off=False),
        'permisos':recorrer_los_permisos_usuario(request),  
    }
        
    return render(request, template_name, context)