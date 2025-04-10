from django.shortcuts import render, get_object_or_404, redirect

# Manejo de mensajes
from django.contrib import messages

# Models
from apps.accountings.models import Creditor, Insurance,  Egress, Income
from apps.financings.models import Payment

# LIBRERIAS PARA CRUD
from django.views.generic import CreateView
from django.views.generic.list import ListView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic.detail import DetailView
from django.db.models import Q

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



# Create your views here.
@login_required
@usuario_activo
def list_acreedores(request):
    template_name = 'contable/acreedores/list.html'
    acreedores_list = Creditor.objects.all().order_by('-id')
    page_obj = paginacion(request, acreedores_list)
    cambiar_plan()
    context = {
        'title':'EL TELAR - ACREEDORES',
        'page_obj':page_obj,
        'acreedores_list':page_obj,
        'count':acreedores_list.count(),
        'posicion':'Todos los Acreedores'
        
    }
        
    return render(request, template_name, context)

@login_required
@usuario_activo
def list_seguros(request):
    template_name = 'contable/seguros/list.html'
    object_list = Insurance.objects.all().order_by('-id')
    page_obj = paginacion(request, object_list)
    cambiar_plan()
    context = {
        'title':'EL TELAR - SEGUROS',
        'page_obj':page_obj,
        'object_list':page_obj,
        'count':object_list.count(),
        'posicion':'Todos los Seguros'
        
    }
        
    return render(request, template_name, context)

@login_required
@usuario_activo
def list_ingresos(request):
    template_name = 'contable/ingresos/list.html'
    object_list = Income.objects.all().order_by('-id')
    page_obj = paginacion(request, object_list)
    cambiar_plan()
    context = {
        'title':'EL TELAR - INGRESOS',
        'page_obj':page_obj,
        'object_list':page_obj,
        'count':object_list.count(),
        'posicion':'Todos los Ingresos'
        
    }
        
    return render(request, template_name, context)

@login_required
@usuario_activo
def list_egresos(request):
    template_name = 'contable/egresos/list.html'
    object_list = Egress.objects.all().order_by('-id')
    page_obj = paginacion(request, object_list)
    cambiar_plan()
    context = {
        'title':'EL TELAR - EGRESOS',
        'page_obj':page_obj,
        'object_list':page_obj,
        'count':object_list.count(),
        'posicion':'Todos los Egresos'
        
    }
        
    return render(request, template_name, context)

@login_required
@usuario_activo
def list_modulos(request):
    template_name = 'contable/options.html'
    
    cambiar_plan()
    context = {
        'title':'EL TELAR - MODULOS CONTABLES',
        'acreedores':Creditor.objects.filter(is_paid_off=False),
        'seguros':Insurance.objects.filter(is_paid_off=False),
        
        
    }
        
    return render(request, template_name, context)