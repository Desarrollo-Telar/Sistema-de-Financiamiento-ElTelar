from django.shortcuts import render

# Models
from apps.financings.models import Credit, PaymentPlan
from apps.customers.models import CreditCounselor

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import  permiso_requerido

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
@permiso_requerido('puede_ver_registros_credito')
def filter_credito_reciente(request):
    template_name = 'financings/credit/list.html'
    sucursal = request.session['sucursal_id']
    hoy = datetime.now()
    inicio = hoy - timedelta(days=5)
    credito = Credit.objects.filter(Q(creation_date__range=[inicio,hoy]), sucursal=sucursal).order_by('-id')

    asesor_autenticado = CreditCounselor.objects.filter(usuario=request.user).first()

    if asesor_autenticado is not None and request.user.rol.role_name == 'Asesor de Crédito':
        credito =  Credit.objects.filter(
            Q(creation_date__range=[inicio,hoy]),
            asesor_de_credito=asesor_autenticado
            ).order_by('-id')

    page_obj = paginacion(request, credito)
    
    context = {
        'title':'Registro de Creditos Agregados Recientemente.',
        'page_obj':page_obj,
        'credit_list':page_obj,
        'count': credito.count(),
        'filtro_seleccionado':'Recientes',
        'permisos':recorrer_los_permisos_usuario(request),
    }
    return render(request, template_name, context)

@login_required
@permiso_requerido('puede_ver_registros_credito')
def filter_credito_cancelado(request):
    template_name = 'financings/credit/list.html'
    credito =  Credit.objects.filter(is_paid_off=True).order_by('-id')
    sucursal = request.session['sucursal_id']
    asesor_autenticado = CreditCounselor.objects.filter(usuario=request.user).first()

    if asesor_autenticado is not None and request.user.rol.role_name == 'Asesor de Crédito':
        credito =  Credit.objects.filter(
            is_paid_off=True,
            asesor_de_credito=asesor_autenticado, sucursal=sucursal
            ).order_by('-id')

    page_obj = paginacion(request, credito)

    
    context = {
        'title':'Registro de Creditos que ya estan Cancelados.',
        'page_obj':page_obj,
        'credit_list':page_obj,
        'count': credito.count(),
        'filtro_seleccionado':'Creditos Cancelados',
        'permisos':recorrer_los_permisos_usuario(request),
    }
    return render(request, template_name, context)

@login_required
@permiso_requerido('puede_ver_registros_credito')
def filter_credito_en_atraso(request):
    template_name = 'financings/credit/list.html'
    sucursal = request.session['sucursal_id']
    credito =  Credit.objects.filter(estados_fechas=False, sucursal=sucursal).order_by('-fecha_actualizacion')

    asesor_autenticado = CreditCounselor.objects.filter(usuario=request.user).first()

    if asesor_autenticado is not None and request.user.rol.role_name == 'Asesor de Crédito':
        credito =  Credit.objects.filter(
            estados_fechas=False,
            asesor_de_credito=asesor_autenticado, sucursal=sucursal
            ).order_by('-fecha_actualizacion')

    page_obj = paginacion(request, credito)
    
    context = {
        'title':'Registro de Creditos que estan en Atraso por Fechas.',
        'page_obj':page_obj,
        'credit_list':page_obj,
        'count': credito.count(),
        'filtro_seleccionado':'Creditos en Atraso',
        'permisos':recorrer_los_permisos_usuario(request),
    }
    return render(request, template_name, context)

@login_required
@permiso_requerido('puede_ver_registros_credito')
def filter_credito_con_aportaciones(request):
    template_name = 'financings/credit/list.html'
    sucursal = request.session['sucursal_id']

    credito =  Credit.objects.filter(estado_aportacion__isnull=False, is_paid_off=False, sucursal=sucursal).order_by('-fecha_actualizacion')

    asesor_autenticado = CreditCounselor.objects.filter(usuario=request.user).first()

    if asesor_autenticado is not None and request.user.rol.role_name == 'Asesor de Crédito':
        credito =  Credit.objects.filter(
            estado_aportacion__isnull=False, is_paid_off=False,
            asesor_de_credito=asesor_autenticado, sucursal=sucursal
            ).order_by('-fecha_actualizacion')

    page_obj = paginacion(request, credito)

    
    context = {
        'title':'Registro de Creditos que estan en Atrado por Aportacion.',
        'page_obj':page_obj,
        'credit_list':page_obj,
        'count': credito.count(),
        'filtro_seleccionado':'Creditos en Atraso',
        'permisos':recorrer_los_permisos_usuario(request),
    }
    return render(request, template_name, context)

@login_required
@permiso_requerido('puede_ver_registros_credito')
def filter_credito_en_falta_aportacion(request):
    template_name = 'financings/credit/list.html'
    sucursal = request.session['sucursal_id']
    credito =  Credit.objects.filter(estado_aportacion=False, sucursal=sucursal).order_by('-id')

    asesor_autenticado = CreditCounselor.objects.filter(usuario=request.user).first()

    if asesor_autenticado is not None and request.user.rol.role_name == 'Asesor de Crédito':
        credito =  Credit.objects.filter(
            estado_aportacion=False,
            asesor_de_credito=asesor_autenticado, sucursal=sucursal
            ).order_by('-fecha_actualizacion')

    page_obj = paginacion(request, credito)
    
    context = {
        'title':'Registro de Creditos que estan en Atrado por Aportacion.',
        'page_obj':page_obj,
        'credit_list':page_obj,
        'count': credito.count(),
        'filtro_seleccionado':'Creditos con falta de Aportacion',
        'permisos':recorrer_los_permisos_usuario(request),
    }
    return render(request, template_name, context)

@login_required
@permiso_requerido('puede_ver_registros_credito')
def filter_credito_con_excedente(request):
    template_name = 'financings/credit/list.html'
    sucursal = request.session['sucursal_id']

    credito =  Credit.objects.filter(Q(saldo_actual__lt=0) | Q(excedente__gt=0), sucursal=sucursal).order_by('-id')

    asesor_autenticado = CreditCounselor.objects.filter(usuario=request.user).first()

    if asesor_autenticado is not None and request.user.rol.role_name == 'Asesor de Crédito':
        credito =  Credit.objects.filter(
            Q(saldo_actual__lt=0) | Q(excedente__gt=0)).filter(
            asesor_de_credito=asesor_autenticado, sucursal=sucursal
            ).order_by('-fecha_actualizacion')

    page_obj = paginacion(request, credito)

    

    context = {
        'title':'Registro de Creditos que estan con excedente.',
        'page_obj':page_obj,
        'credit_list':page_obj,
        'count': credito.count(),
        'filtro_seleccionado': 'Creditos con excedente',
        'permisos':recorrer_los_permisos_usuario(request),
        
    }
    return render(request, template_name, context)

@login_required
@permiso_requerido('puede_ver_registros_credito')
def filter_credito_por_mes_anio(request):
    template_name = 'financings/credit/list.html'
    sucursal = request.session['sucursal_id']

    mes = datetime.now().month
    anio = datetime.now().year
    asesor_autenticado = CreditCounselor.objects.filter(usuario=request.user).first()

    

    if request.method == 'POST':
        mes = request.POST.get('mes')
        anio = request.POST.get('anio')
        

        # Validación de mes y año
        if not mes:
            mes = datetime.now().month
        else:
            mes = int(mes)

        if not anio:
            anio = datetime.now().year
        else:
            anio = int(anio)

    filters = Q()
    filters &= Q(creation_date__year=anio)
    filters &= Q(creation_date__month=mes)
    if asesor_autenticado is not None and request.user.rol.role_name == 'Asesor de Crédito':
        filters &= Q(asesor_de_credito=asesor_autenticado)

    
    object_list = Credit.objects.filter(filters, sucursal=sucursal).order_by('id')
    page_obj = paginacion(request, object_list)
    

    context = {
        'title':f'Registro de Creditos Creatos en el mes de. {mes} {anio}',
        #'page_obj':page_obj,
        'credit_list':page_obj,
        'reporte':True,
        'reporte_excel':True,
        'reporte_desembolso':True,
        'count': object_list.count(),
        'mes': mes,
        'anio': anio,
        'filtro_seleccionado':'Creditos con falta de Aportacion',
        'permisos':recorrer_los_permisos_usuario(request),
    }
    return render(request, template_name, context)

