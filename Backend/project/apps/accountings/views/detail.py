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


# MENSAJES
from django.contrib import messages



# Create your views here.
@login_required
@usuario_activo
def list_acreedores(request):
    template_name = 'contable/acreedores/list.html'
    acreedores_list = Creditor.objects.all().order_by('-id')
    page_obj = paginacion(request, acreedores_list)
    context = {
        'title':'EL TELAR',
        'page_obj':page_obj,
        'acreedores_list':page_obj,
        'count':acreedores_list.count(),
        
    }
        
    return render(request, template_name, context)

@login_required
@usuario_activo
def list_seguros(request):
    template_name = 'contable/seguros/list.html'
    object_list = Insurance.objects.all().order_by('-id')
    page_obj = paginacion(request, object_list)
    context = {
        'title':'EL TELAR',
        'page_obj':page_obj,
        'object_list':page_obj,
        'count':object_list.count(),
        
    }
        
    return render(request, template_name, context)

@login_required
@usuario_activo
def list_ingresos(request):
    template_name = 'contable/ingresos/list.html'
    object_list = Income.objects.all().order_by('-id')
    page_obj = paginacion(request, object_list)
    context = {
        'title':'EL TELAR',
        'page_obj':page_obj,
        'object_list':page_obj,
        'count':object_list.count(),
        
    }
        
    return render(request, template_name, context)

@login_required
@usuario_activo
def list_egresos(request):
    template_name = 'contable/egresos/list.html'
    object_list = Egress.objects.all().order_by('-id')
    page_obj = paginacion(request, object_list)
    context = {
        'title':'EL TELAR',
        'page_obj':page_obj,
        'object_list':page_obj,
        'count':object_list.count(),
        
    }
        
    return render(request, template_name, context)