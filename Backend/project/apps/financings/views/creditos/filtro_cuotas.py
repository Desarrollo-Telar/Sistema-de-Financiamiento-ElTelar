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

    creditos_proximos_vencerse= PaymentPlan.objects.filter(due_date__range=[hoy, hasta], status=False).order_by('due_date')

    credito = credito_fecha_vencimiento_hoy(creditos_proximos_vencerse)

    asesor_autenticado = CreditCounselor.objects.filter(usuario=request.user).first()

    if asesor_autenticado is not None and request.user.rol.role_name == 'Asesor de Crédito':
        creditos_proximos_vencerse = PaymentPlan.objects.filter(due_date__range=[hoy, hasta], status=False, credit_id__asesor_de_credito=asesor_autenticado)
        credito = credito_fecha_vencimiento_hoy(creditos_proximos_vencerse)
    
    if request.user.rol.role_name == 'Secretari@':
        creditos_proximos_vencerse = PaymentPlan.objects.filter(
            due_date__range=[hoy, hasta],
            status=False,
            credit_id__isnull=False
        )
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

    creditos_fecha_limite = PaymentPlan.objects.filter(fecha_limite__date=dia)
    
   

    credito = credito_fecha_vencimiento_hoy(creditos_fecha_limite)

    asesor_autenticado = CreditCounselor.objects.filter(usuario=request.user).first()

    if asesor_autenticado is not None and request.user.rol.role_name == 'Asesor de Crédito':
        creditos_fecha_limite = PaymentPlan.objects.filter(fecha_limite__date=dia, credit_id__asesor_de_credito=asesor_autenticado)
        credito = credito_fecha_vencimiento_hoy(creditos_fecha_limite)

    if request.user.rol.role_name == 'Secretari@':
        creditos_fecha_limite = PaymentPlan.objects.filter(
            fecha_limite__date=dia,
            credit_id__isnull=False
        )
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

    creditos_fecha_vencimiento = PaymentPlan.objects.filter(due_date__date=dia)
    
   

    credito = credito_fecha_vencimiento_hoy(creditos_fecha_vencimiento)

    asesor_autenticado = CreditCounselor.objects.filter(usuario=request.user).first()

    if asesor_autenticado is not None and request.user.rol.role_name == 'Asesor de Crédito':
        creditos_fecha_vencimiento = PaymentPlan.objects.filter(due_date__date=dia, credit_id__asesor_de_credito=asesor_autenticado)
        credito = credito_fecha_vencimiento_hoy(creditos_fecha_vencimiento)
    
    if request.user.rol.role_name == 'Secretari@':
        creditos_fecha_vencimiento = PaymentPlan.objects.filter(
            due_date__date=dia,
            credit_id__isnull=False
        )
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
