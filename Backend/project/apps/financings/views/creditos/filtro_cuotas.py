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
def filter_credito_proximos_vencerse(request):
    template_name = 'financings/cuota/list.html'
    hoy = datetime.now() 
    hasta = hoy + timedelta(days=7)
    sucursal = request.session['sucursal_id']
    filters = Q()
    filters &= Q(due_date__range=[hoy, hasta])
    filters &= Q(status=False)
    filters &= Q(sucursal=sucursal)

    asesor_autenticado = CreditCounselor.objects.filter(usuario=request.user).first()

    if asesor_autenticado is not None and request.user.rol.role_name == 'Asesor de Crédito':
        
        filters &= Q(credit_id__asesor_de_credito=asesor_autenticado)
    
    if request.user.rol.role_name == 'Secretari@':
        
        filters &= Q(credit_id__isnull=False)
        

    creditos_proximos_vencerse= PaymentPlan.objects.filter(filters).order_by('due_date')
    credito = credito_fecha_vencimiento_hoy(creditos_proximos_vencerse)

    page_obj = paginacion(request, credito)
    
    context = {
        'title': f'Creditos con Fecha Limite de {hoy.date()}.',
        'page_obj':page_obj,
        'cuotas_list':page_obj,
        'count': creditos_proximos_vencerse.count(),
        'permisos':recorrer_los_permisos_usuario(request),
        'posicion':f'Creditos con Proximos a llegar a su Fecha de Vencimiento / {hoy.date()}.',
    }
    return render(request, template_name, context)


@login_required
@permiso_requerido('puede_ver_registros_credito')
def filter_credito_fecha_limite_hoy(request):
    template_name = 'financings/cuota/list.html'
    dia = datetime.now().date() # Obtener el dia 
    sucursal = request.session['sucursal_id']
    
    
    filters = Q()
    filters &= Q(fecha_limite__date=dia)
    filters &= Q(sucursal=sucursal)
    filters &= Q(credit_id__is_paid_off = False)
    filters &= Q(credit_id__estado_judicial = False)


    

    asesor_autenticado = CreditCounselor.objects.filter(usuario=request.user).first()

    if asesor_autenticado is not None and request.user.rol.role_name == 'Asesor de Crédito':
        filters &= Q(credit_id__asesor_de_credito=asesor_autenticado)

    if request.user.rol.role_name == 'Secretari@':
        filters &= Q(credit_id__isnull=False)
        

    creditos_fecha_limite = PaymentPlan.objects.filter(filters)
    credito = credito_fecha_vencimiento_hoy(creditos_fecha_limite)

    page_obj = paginacion(request, credito)
    
    context = {
        'title': f'Creditos con Fecha Limite de {dia}.',
        'page_obj':page_obj,
        'cuotas_list':page_obj,
        'count': creditos_fecha_limite.count(),
        'permisos':recorrer_los_permisos_usuario(request),
        'posicion':f'Creditos con Fecha Limite de / {dia}.',
    }
    return render(request, template_name, context)

@login_required
@permiso_requerido('puede_ver_registros_credito')
def filter_credito_fecha_vencimiento_hoy(request):
    template_name = 'financings/cuota/list.html'
    dia = datetime.now().date() # Obtener el dia 
    sucursal = request.session['sucursal_id']
    
    
    filters = Q()
    filters &= Q(due_date__date=dia)
    filters &= Q(sucursal=sucursal)
    

    asesor_autenticado = CreditCounselor.objects.filter(usuario=request.user).first()

    if asesor_autenticado is not None and request.user.rol.role_name == 'Asesor de Crédito':
        
        filters &= Q(credit_id__asesor_de_credito=asesor_autenticado)
    
    if request.user.rol.role_name == 'Secretari@':
        filters &= Q(credit_id__isnull=False)

    creditos_fecha_vencimiento = PaymentPlan.objects.filter(filters)
    credito = credito_fecha_vencimiento_hoy(creditos_fecha_vencimiento)


    page_obj = paginacion(request, credito)
    
    context = {
        'title': f'Creditos con Fecha de Vencimiento {dia}.',
        'page_obj':page_obj,
        'cuotas_list':page_obj,
        'count': creditos_fecha_vencimiento.count(),
        'permisos':recorrer_los_permisos_usuario(request),
        'posicion':f'Creditos con Fecha de Vencimiento / {dia}.',
    }
    return render(request, template_name, context)
