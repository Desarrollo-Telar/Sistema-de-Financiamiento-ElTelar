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
@permiso_requerido('puede_ver_registros_credito')
def filter_credito_proximos_vencerse(request):
    template_name = 'financings/cuota/list.html'
    hoy = datetime.now() 
    hasta = hoy + timedelta(days=7)

    creditos_proximos_vencerse= PaymentPlan.objects.filter(due_date__range=[hoy, hasta], status=False).order_by('due_date')

    
   

    credito = credito_fecha_vencimiento_hoy(creditos_proximos_vencerse)

    asesor_autenticado = CreditCounselor.objects.filter(usuario=request.user).first()

    if asesor_autenticado is not None and request.user.rol.role_name == 'Asesor de Crédito':
        creditos_proximos_vencerse = PaymentPlan.objects.filter(due_date__range=[hoy, hasta], status=False, credit_id__customer_id__new_asesor_credito=asesor_autenticado)
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
        creditos_fecha_limite = PaymentPlan.objects.filter(fecha_limite__date=dia, credit_id__customer_id__new_asesor_credito=asesor_autenticado)
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
        creditos_fecha_vencimiento = PaymentPlan.objects.filter(due_date__date=dia, credit_id__customer_id__new_asesor_credito=asesor_autenticado)
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

@login_required
@permiso_requerido('puede_ver_registros_credito')
def filter_credito_reciente(request):
    template_name = 'financings/credit/list.html'
    hoy = datetime.now()
    inicio = hoy - timedelta(days=5)
    credito = Credit.objects.filter(Q(creation_date__range=[inicio,hoy])).order_by('-id')

    asesor_autenticado = CreditCounselor.objects.filter(usuario=request.user).first()

    if asesor_autenticado is not None and request.user.rol.role_name == 'Asesor de Crédito':
        credito =  Credit.objects.filter(
            Q(creation_date__range=[inicio,hoy]),
            customer_id__new_asesor_credito=asesor_autenticado
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

    asesor_autenticado = CreditCounselor.objects.filter(usuario=request.user).first()

    if asesor_autenticado is not None and request.user.rol.role_name == 'Asesor de Crédito':
        credito =  Credit.objects.filter(
            is_paid_off=True,
            customer_id__new_asesor_credito=asesor_autenticado
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

    credito =  Credit.objects.filter(estados_fechas=False).order_by('-fecha_actualizacion')

    asesor_autenticado = CreditCounselor.objects.filter(usuario=request.user).first()

    if asesor_autenticado is not None and request.user.rol.role_name == 'Asesor de Crédito':
        credito =  Credit.objects.filter(
            estados_fechas=False,
            customer_id__new_asesor_credito=asesor_autenticado
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
   

    credito =  Credit.objects.filter(estado_aportacion__isnull=False, is_paid_off=False).order_by('-fecha_actualizacion')

    asesor_autenticado = CreditCounselor.objects.filter(usuario=request.user).first()

    if asesor_autenticado is not None and request.user.rol.role_name == 'Asesor de Crédito':
        credito =  Credit.objects.filter(
            estado_aportacion__isnull=False, is_paid_off=False,
            customer_id__new_asesor_credito=asesor_autenticado
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

    credito =  Credit.objects.filter(estado_aportacion=False).order_by('-id')

    asesor_autenticado = CreditCounselor.objects.filter(usuario=request.user).first()

    if asesor_autenticado is not None and request.user.rol.role_name == 'Asesor de Crédito':
        credito =  Credit.objects.filter(
            estado_aportacion=False,
            customer_id__new_asesor_credito=asesor_autenticado
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
    

    credito =  Credit.objects.filter(saldo_actual__lt=0).order_by('-id')

    asesor_autenticado = CreditCounselor.objects.filter(usuario=request.user).first()

    if asesor_autenticado is not None and request.user.rol.role_name == 'Asesor de Crédito':
        credito =  Credit.objects.filter(
            saldo_actual__lt=0,
            customer_id__new_asesor_credito=asesor_autenticado
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
        filters &= Q(customer_id__new_asesor_credito=asesor_autenticado)

    
    object_list = Credit.objects.filter(filters).order_by('id')
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


@login_required
@permiso_requerido('puede_ver_registros_boletas_pagos')
def filter_list_payment_pendiente(request):
    template_name = 'financings/payment/list.html'
    page_obj = paginacion(request, Payment.objects.filter(estado_transaccion='PENDIENTE', registro_ficticio=False).order_by('-id'))
    


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
    template_name = 'financings/payment/list.html'
    page_obj = paginacion(request, Payment.objects.filter(estado_transaccion='COMPLETADO', registro_ficticio=False).order_by('-id'))
    


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
    page_obj = paginacion(request, Banco.objects.filter(status=True, registro_ficticio=False).order_by('-fecha'))
    

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
    page_obj = paginacion(request, Banco.objects.filter(status=False, registro_ficticio=False).order_by('-fecha'))
    

    context = {
        'title':'Registro de Bancos que ya han sido vinculados.',
        'page_obj':page_obj,
        'banco_list':page_obj,
        'count':Banco.objects.filter(status=False, registro_ficticio=False).count(),
        'permisos':recorrer_los_permisos_usuario(request),
    }
    return render(request,template_name, context)