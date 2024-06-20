from django.shortcuts import render, get_object_or_404, redirect

# Models
from .models import Customer


# LIBRERIAS PARA CRUD

from django.views.generic.list import ListView
from django.db.models import Q

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import usuario_activo
from django.utils.decorators import method_decorator

# Paginacion
from project.pagination import paginacion
from datetime import datetime, timedelta

@login_required
@usuario_activo
def recent_customer(request):
    hoy = datetime.now()
    inicio = hoy - timedelta(days=5)
    customer_list = Customer.objects.all().filter(Q(creation_date__range=[inicio,hoy])).order_by('-id')
    page_obj = paginacion(request, customer_list)
    template_name = 'customer/list.html'
    context = {
        'title':'EL TELAR - CLIENTES',        
        'customer_list':page_obj,
        'count':customer_list.count(),
        'message': 'RECIENTEMENTE',
        'page_obj':page_obj,
        'posicion':'Recientemente',
    
    }
    return render(request, template_name, context)

@login_required
@usuario_activo
def solicitude_customer(request):
    customer_list = Customer.objects.all().filter(Q(status='Posible Cliente')).order_by('-id')
    page_obj = paginacion(request, customer_list)
    template_name = 'customer/list.html'
    context = {
        'title':'EL TELAR - CLIENTES',        
        'customer_list':page_obj,
        'count':customer_list.count(),
        'message': 'EN PROCESO DE SOLICITUD',
        'page_obj':page_obj,
        'posicion':'Solicitudes',
    
    }
    return render(request, template_name, context)

@login_required
@usuario_activo
def not_accepted_customer(request):
    customer_list = Customer.objects.all().filter(Q(status='No Aprobado')).order_by('-id')
    page_obj = paginacion(request, customer_list)
    template_name = 'customer/list.html'
    context = {
        'title':'EL TELAR - CLIENTES',        
        'customer_list':page_obj,
        'count':customer_list.count(),
        'message': 'NO APROBADOS',
        'page_obj':page_obj,
        'posicion':'No Aprobados',
    
    }
    return render(request, template_name, context)

@login_required
@usuario_activo
def accepted_customer(request):
    customer_list = Customer.objects.all().filter(Q(status='Aprobado')).order_by('-id')
    page_obj = paginacion(request, customer_list)
    template_name = 'customer/list.html'
    context = {
        'title':'EL TELAR - CLIENTES',        
        'customer_list':page_obj,
        'count':customer_list.count(),
        'message': 'APROBADOS',
        'page_obj':page_obj,
        'posicion':'Aprobados',
    
    }
    return render(request, template_name, context)

@login_required
@usuario_activo
def inactive_customer(request):
    customer_list = Customer.objects.all().filter(Q(status='Dar de Baja')).order_by('-id')
    page_obj = paginacion(request, customer_list)
    template_name = 'customer/list.html'
    context = {
        'title':'EL TELAR - CLIENTES',        
        'customer_list':page_obj,
        'count':customer_list.count(),
        'message': 'INACTIVOS',
        'page_obj':page_obj,
        'posicion':'Inactivos',
    
    }
    return render(request, template_name, context)

@login_required
@usuario_activo
def document_review_customer(request):
    customer_list = Customer.objects.all().filter(Q(status='Revisión de documentos')).order_by('-id')
    page_obj = paginacion(request, customer_list)
    template_name = 'customer/list.html'
    context = {
        'title':'EL TELAR - CLIENTES',        
        'customer_list':page_obj,
        'count':customer_list.count(),
        'message': 'EN PROCESO DE REVISIÓN DE DOCUMENTOS',
        'page_obj':page_obj,
        'posicion':'Revisión de documentos',
    
    }
    return render(request, template_name, context)