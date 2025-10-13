from django.shortcuts import render

# Models
from apps.financings.models import Credit, Banco, Payment, PaymentPlan
from apps.customers.models import CreditCounselor

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import usuario_activo, permiso_requerido
from django.utils.decorators import method_decorator

# Paginacion
from project.pagination import paginacion

# Scripts
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario
from scripts.cuotas.recoleccion_informacion import credito_fecha_vencimiento_hoy

# LIBRERIAS PARA CRUD
from django.db.models import Q

# Tiempo
from datetime import datetime, timedelta


@login_required
@permiso_requerido('puede_ver_registros_boletas_pagos')
def filter_list_payment_pendiente(request):
    sucursal = request.session['sucursal_id']
    template_name = 'financings/payment/list.html'
    page_obj = paginacion(request, Payment.objects.filter(estado_transaccion='PENDIENTE', registro_ficticio=False, sucursal=sucursal).order_by('-id'))
    


    context = {
        'title':'Registro de Boletas que se encuentran en Pendientes de Vincular.',
        'page_obj':page_obj,
        'payment_list':page_obj,
        'count':Payment.objects.filter(estado_transaccion='PENDIENTE', registro_ficticio=False).count(),
        'permisos':recorrer_los_permisos_usuario(request),

        
    }
    return render(request,template_name, context)

@login_required
@permiso_requerido('puede_ver_registros_boletas_pagos')
def filter_list_payment_completados(request):
    sucursal = request.session['sucursal_id']
    template_name = 'financings/payment/list.html'
    page_obj = paginacion(request, Payment.objects.filter(estado_transaccion='COMPLETADO', registro_ficticio=False, sucursal=sucursal).order_by('-id'))
    


    context = {
        'title':'Registro de Boletas que estan Completamente Vinculados.',
        'page_obj':page_obj,
        'payment_list':page_obj,
        'count':Payment.objects.filter(estado_transaccion='COMPLETADO', registro_ficticio=False).count(),
        'permisos':recorrer_los_permisos_usuario(request),

        
    }
    return render(request,template_name, context)

@login_required
@permiso_requerido('puede_ver_listado_registro_bancos')
def filter_list_bank_vinculado(request):
    template_name = 'financings/bank/list.html'
    sucursal = request.session['sucursal_id']
    page_obj = paginacion(request, Banco.objects.filter(status=True, registro_ficticio=False, sucursal=sucursal).order_by('-fecha'))
    

    context = {
        'title':'Registro de Bancos que no han sido vinculados.',
        'page_obj':page_obj,
        'banco_list':page_obj,
        'count':Banco.objects.filter(status=True, registro_ficticio=False).count(),
        'permisos':recorrer_los_permisos_usuario(request),
    }
    return render(request,template_name, context)

@login_required
@permiso_requerido('puede_ver_listado_registro_bancos')
def filter_list_bank_no_vinculado(request):
    template_name = 'financings/bank/list.html'
    sucursal = request.session['sucursal_id']
    page_obj = paginacion(request, Banco.objects.filter(status=False, registro_ficticio=False, sucursal=sucursal).order_by('-fecha'))
    

    context = {
        'title':'Registro de Bancos que ya han sido vinculados.',
        'page_obj':page_obj,
        'banco_list':page_obj,
        'count':Banco.objects.filter(status=False, registro_ficticio=False).count(),
        'permisos':recorrer_los_permisos_usuario(request),
    }
    return render(request,template_name, context)