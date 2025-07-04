from django.shortcuts import render, get_object_or_404, redirect

# Models
from .models import Customer, CreditCounselor


# LIBRERIAS PARA CRUD

from django.views.generic.list import ListView
from django.db.models import Q

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import permiso_requerido
from django.utils.decorators import method_decorator

# Paginacion
from project.pagination import paginacion
from datetime import datetime, timedelta

# SCRIPTS
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario

@login_required
@permiso_requerido('puede_visualizar_el_registro_clientes')
def recent_customer(request):
    hoy = datetime.now()
    inicio = hoy - timedelta(days=5)

    customer_list = Customer.objects.all().filter(Q(creation_date__range=[inicio,hoy])).order_by('-id')

    asesor_autenticado = CreditCounselor.objects.filter(usuario=request.user).first()

    if asesor_autenticado is not None:
        customer_list = Customer.objects.all().filter(Q(creation_date__range=[inicio,hoy]), new_asesor_credito=asesor_autenticado).order_by('-id')

    page_obj = paginacion(request, customer_list)
    template_name = 'customer/list.html'
    context = {
        'title':'Registro de Clientes Recientes.',        
        'customer_list':page_obj,
        'count':customer_list.count(),
        'message': 'RECIENTEMENTE',
        'page_obj':page_obj,
        'posicion':'Recientemente',
        'permisos':recorrer_los_permisos_usuario(request)
    
    }
    return render(request, template_name, context)

@login_required
@permiso_requerido('puede_visualizar_el_registro_clientes')
def solicitude_customer(request):
    customer_list = Customer.objects.all().filter(Q(status='Posible Cliente')).order_by('-id')

    asesor_autenticado = CreditCounselor.objects.filter(usuario=request.user).first()

    if asesor_autenticado is not None:
        customer_list = Customer.objects.all().filter(Q(status='Posible Cliente'), new_asesor_credito=asesor_autenticado).order_by('-id')
         
    page_obj = paginacion(request, customer_list)
    template_name = 'customer/list.html'
    context = {
        'title':'Registro de Clientes que estan en Solicitud.',        
        'customer_list':page_obj,
        'count':customer_list.count(),
        'message': 'EN PROCESO DE SOLICITUD',
        'page_obj':page_obj,
        'posicion':'Solicitudes',
        'permisos':recorrer_los_permisos_usuario(request)
    
    }
    return render(request, template_name, context)

@login_required
@permiso_requerido('puede_visualizar_el_registro_clientes')
def not_accepted_customer(request):
    customer_list = Customer.objects.all().filter(Q(status='No Aprobado')).order_by('-id')

    asesor_autenticado = CreditCounselor.objects.filter(usuario=request.user).first()

    if asesor_autenticado is not None:
        customer_list = Customer.objects.all().filter(Q(status='No Aprobado'), new_asesor_credito=asesor_autenticado).order_by('-id')

    page_obj = paginacion(request, customer_list)
    template_name = 'customer/list.html'
    context = {
        'title':'Registro de Clientes que no fueron aceptados.',        
        'customer_list':page_obj,
        'count':customer_list.count(),
        'message': 'NO APROBADOS',
        'page_obj':page_obj,
        'posicion':'No Aprobados',
        'permisos':recorrer_los_permisos_usuario(request)
    
    }
    return render(request, template_name, context)

@login_required
@permiso_requerido('puede_visualizar_el_registro_clientes')
def accepted_customer(request):
    customer_list = Customer.objects.all().filter(Q(status='Aprobado')).order_by('-id')

    asesor_autenticado = CreditCounselor.objects.filter(usuario=request.user).first()

    if asesor_autenticado is not None:
        customer_list = Customer.objects.all().filter(Q(status='Aprobado'), new_asesor_credito=asesor_autenticado).order_by('-id')

    page_obj = paginacion(request, customer_list)
    template_name = 'customer/list.html'
    context = {
        'title':'Registro de Clientes Aprobados.',        
        'customer_list':page_obj,
        'count':customer_list.count(),
        'message': 'APROBADOS',
        'page_obj':page_obj,
        'posicion':'Aprobados',
        'permisos':recorrer_los_permisos_usuario(request)
    
    }
    return render(request, template_name, context)

@login_required
@permiso_requerido('puede_visualizar_el_registro_clientes')
def inactive_customer(request):
    customer_list = Customer.objects.all().filter(Q(status='Dar de Baja')).order_by('-id')
    asesor_autenticado = CreditCounselor.objects.filter(usuario=request.user).first()

    if asesor_autenticado is not None:
        customer_list = Customer.objects.all().filter(Q(status='Dar de Baja'), new_asesor_credito=asesor_autenticado).order_by('-id')

    page_obj = paginacion(request, customer_list)
    template_name = 'customer/list.html'
    context = {
        'title':'Registro de Clientes que fueron dados de Baja',        
        'customer_list':page_obj,
        'count':customer_list.count(),
        'message': 'INACTIVOS',
        'page_obj':page_obj,
        'posicion':'Inactivos',
        'permisos':recorrer_los_permisos_usuario(request)
    
    }
    return render(request, template_name, context)

@login_required
@permiso_requerido('puede_visualizar_el_registro_clientes')
def document_review_customer(request):
    customer_list = Customer.objects.all().filter(Q(status='Revisión de documentos')).order_by('-id')

    asesor_autenticado = CreditCounselor.objects.filter(usuario=request.user).first()

    if asesor_autenticado is not None:
        customer_list = Customer.objects.all().filter(Q(status='Revisión de documentos'), new_asesor_credito=asesor_autenticado).order_by('-id')

    page_obj = paginacion(request, customer_list)
    template_name = 'customer/list.html'
    context = {
        'title':'Registro de Clientes que estan en proceso de Revisión de Documentos',        
        'customer_list':page_obj,
        'count':customer_list.count(),
        'message': 'EN PROCESO DE REVISIÓN DE DOCUMENTOS',
        'page_obj':page_obj,
        'posicion':'Revisión de documentos',
        'permisos':recorrer_los_permisos_usuario(request)
    
    }
    return render(request, template_name, context)