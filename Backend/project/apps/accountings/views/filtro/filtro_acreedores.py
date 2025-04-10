from django.shortcuts import render, get_object_or_404, redirect

# Manejo de mensajes
from django.contrib import messages

# Models
from apps.accountings.models import  Creditor


# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import usuario_activo, usuario_administrador, usuario_secretaria
from django.utils.decorators import method_decorator

# Paginacion
from project.pagination import paginacion

# TAREA ASINCRONICO
from apps.financings.task import cambiar_plan

# MENSAJES
from django.contrib import messages

@login_required
@usuario_activo
def acreedores_cancelado(request):
    template_name = 'contable/acreedores/list.html'
    object_list = Creditor.objects.filter(is_paid_off=True).order_by('-id')
    page_obj = paginacion(request, object_list)
    cambiar_plan()
    context = {
        'title':'EL TELAR - ACREEDORES / ACREEDORES CANCELADOS',
        'page_obj':page_obj,
        'object_list':page_obj,
        'count':object_list.count(),
        'posicion':'Acreedores cancelados'
        
    }
        
    return render(request, template_name, context)

@login_required
@usuario_activo
def acreedores_atraso_aportacion(request):
    template_name = 'contable/acreedores/list.html'
    object_list = Creditor.objects.filter(estado_aportacion=False).order_by('-id')
    page_obj = paginacion(request, object_list)
    cambiar_plan()
    context = {
        'title':'EL TELAR - ACREEDORES / ACREEDORES ATRASO POR APORTACION',
        'page_obj':page_obj,
        'object_list':page_obj,
        'count':object_list.count(),
        'posicion':'Acreedores con atraso por aportacion'
        
    }
        
    return render(request, template_name, context)

@login_required
@usuario_activo
def acreedores_atraso_fechas(request):
    template_name = 'contable/acreedores/list.html'
    object_list = Creditor.objects.filter(estados_fechas=False).order_by('-id')
    page_obj = paginacion(request, object_list)
    cambiar_plan()
    context = {
        'title':'EL TELAR - ACREEDORES / ACREEDORES ATRASO POR FECHAS',
        'page_obj':page_obj,
        'object_list':page_obj,
        'count':object_list.count(),
        'posicion':'Acreedores con atraso por fechas'
    }
        
    return render(request, template_name, context)