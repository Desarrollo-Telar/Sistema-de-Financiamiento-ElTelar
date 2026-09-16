from django.shortcuts import render, get_object_or_404, redirect

# Models
from apps.financings.models import Credit, Guarantees, Disbursement,DetailsGuarantees, Banco, Payment, PaymentPlan, AccountStatement, Recibo
from apps.customers.models import CreditCounselor

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import usuario_activo, permiso_requerido
from django.utils.decorators import method_decorator

# Paginacion
from project.pagination import paginacion

# SCRIPTS
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario
from django.db.models import Q



@login_required
@permiso_requerido('puede_ver_registros_boletas_pagos')
def list_payment(request):
    sucursal = request.session['sucursal_id']
    template_name = 'financings/payment/list.html'
    page_obj = paginacion(request, Payment.objects.filter(registro_ficticio=False, sucursal=sucursal).order_by('-id'))
    
    context = {
        'title':'Registro de Pagos',
        'page_obj':page_obj,
        'payment_list':page_obj,
        'permisos':recorrer_los_permisos_usuario(request),
        'count':Payment.objects.filter(registro_ficticio=False, sucursal=sucursal).count()

        
    }
    return render(request,template_name, context)

@login_required
@permiso_requerido('puede_ver_listado_registro_bancos')
def list_bank(request):
    sucursal = request.session.get('sucursal_id')
    template_name = 'financings/bank/list.html'
    
    # Queryset base filtrado por sucursal y sin registros ficticios
    queryset = Banco.objects.filter(registro_ficticio=False, sucursal=sucursal)
    
    # 1. Parámetros de filtrado y búsqueda desde la URL (GET)
    query = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', '').strip()
    banco_filter = request.GET.get('banco', '').strip()

    # Aplicar búsqueda por texto (referencia, descripción o nombre del banco)
    if query:
        queryset = queryset.filter(
            Q(referencia__icontains=query) | 
            Q(descripcion__icontains=query) | 
            Q(nombre_del_banco__icontains=query)
        )

    # Aplicar filtro por estado (a. Validado / b. Pendiente)
    # Asumiendo que 'status=True' es Validado y 'status=False' es Pendiente
    if status_filter == 'validado':
        queryset = queryset.filter(status=True)
    elif status_filter == 'pendiente':
        queryset = queryset.filter(status=False)

    # Aplicar filtro por clasificador de nombre de banco
    if banco_filter:
        queryset = queryset.filter(nombre_del_banco=banco_filter)

    # Ordenamiento final
    queryset = queryset.order_by('-fecha')

    # Obtener lista única de bancos para poblar el selector en el HTML
    bancos_disponibles = Banco.objects.filter(
        registro_ficticio=False, sucursal=sucursal
    ).values_list('nombre_del_banco', flat=True).distinct()

    # Total de registros filtrados reales
    total_registros = queryset.count()

    # Paginación
    page_obj = paginacion(request, queryset)

    context = {
        'title': 'Registro de Bancos.',
        'page_obj': page_obj,
        'bancos': page_obj,
        'permisos': recorrer_los_permisos_usuario(request),
        'count': total_registros,
        'bancos_disponibles': bancos_disponibles, # Para llenar el select de bancos
        # Devolvemos los valores actuales para mantenerlos seleccionados en el form
        'request_q': query,
        'request_status': status_filter,
        'request_banco': banco_filter,
    }
    return render(request, template_name, context)


@login_required
@permiso_requerido('puede_ver_registros_credito')
def list_credit(request):
    sucursal = request.session['sucursal_id']
    template_name = 'financings/credit/list.html'
    creditos =  Credit.objects.all().order_by('-id').filter(sucursal=sucursal)
    
    asesor_autenticado = CreditCounselor.objects.filter(usuario=request.user).first()

    if asesor_autenticado is not None and request.user.rol.role_name == 'Asesor de Crédito':
        creditos =  Credit.objects.filter(customer_id__new_asesor_credito=asesor_autenticado, sucursal=sucursal)

    page_obj = paginacion(request,creditos)
    
    
    context = {
        'title':'Registro de Creditos.',
        'page_obj':page_obj,
        'credit_list':page_obj,
        'count':creditos.count(),
        'filtro_seleccionado':'Todos',
        'permisos':recorrer_los_permisos_usuario(request),
    }
    return render(request, template_name, context)

@login_required
@permiso_requerido('puede_ver_listado_de_garantias_del_credito')
def list_guarantee(request):
    template_name = 'financings/guarantee/lists.html'
    page_obj = paginacion(request, Guarantees.objects.all().order_by('-id'))

    context = {
        'title':'Registro de Garantias.',
        'page_obj':page_obj,
        'list_guarantee':page_obj,
        'permisos':recorrer_los_permisos_usuario(request),
        'detalle_garantia':DetailsGuarantees.objects.all(),
    }
    return render(request, template_name, context)

@login_required
@permiso_requerido('puede_ver_listado_de_desembolsos_aplicados_del_credito')
def list_disbursement(request):
    template_name = 'financings/disbursement/list.html'
    page_obj = paginacion(request, Disbursement.objects.all().order_by('-id'))
    context = {
        'title':'Registro de Desembolsos.',
        'page_obj':page_obj,
        'permisos':recorrer_los_permisos_usuario(request),
        'list_disbursement':page_obj
    }
    return render(request, template_name, context)




@login_required
@usuario_activo
def list_clasificacion(request):
    template_name = 'financings/credit/clasificacion.html'
    
    context = {
        'title':'ELTELAR - CLASIFICACION DE CREDITOS',
        'posicion':'Creditos',
        'permisos':recorrer_los_permisos_usuario(request),
        

        
    }
    return render(request, template_name, context)



    
