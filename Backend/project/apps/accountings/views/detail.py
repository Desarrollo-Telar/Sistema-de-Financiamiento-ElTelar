from django.shortcuts import render, get_object_or_404, redirect

# TIEMPO
from datetime import datetime,timedelta

# Models
from apps.accountings.models import Creditor, Insurance,  Egress, Income
from apps.financings.models import Payment, PaymentPlan, AccountStatement

# Scripts
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import usuario_activo, usuario_administrador, permiso_requerido
from django.utils.decorators import method_decorator

# Paginacion
from project.pagination import paginacion

# TAREA ASINCRONICO
from apps.financings.tareas_ansicronicas import generar_todas_las_cuotas_acreedores


# CLASES
from apps.financings.clases.paymentplan import PaymentPlan as PlanPagoos
from apps.financings.clases.credit import Credit as Credito

def formatear_numero(numero):
    # Convertir el número a un formato con coma para miles y punto para decimales
    return f"{numero:,.2f}".replace(".", "X").replace(".", ",").replace("X", ".")
    
def planPagosCredito(credito):
    formatted_date = credito.fecha_inicio.strftime('%Y-%m-%d')
    credit = Credito('credito.proposito',credito.monto,credito.plazo,credito.tasa,credito.forma_de_pago,'MENSAUL',formatted_date,'credito.tipo_credito',1,None,credito.fecha_vencimiento)
    plan_pago = PlanPagoos(credit)
    return plan_pago

def total_mora_pagada(estado_cuenta):
    contador = 0
    for estado in estado_cuenta:
        contador+=estado.late_fee_paid
    return formatear_numero(contador)

def total_interes_pagada(estado_cuenta):
    contador = 0
    for estado in estado_cuenta:
        contador+=estado.interest_paid
    return formatear_numero(contador)

def total_capital_pagada(estado_cuenta):
    contador = 0
    for estado in estado_cuenta:
        contador+=estado.capital_paid
    return formatear_numero(contador)

# Create your views here.
@login_required
@permiso_requerido('puede_ver_detalle_acreedores')
def detail_acreedores(request, id):
    template_name = 'contable/acreedores/detail.html'
    object_list = get_object_or_404(Creditor, id=id)
    dia = datetime.now().date()
    dia_mas_uno = dia + timedelta(days=1)

    siguiente_pago = PaymentPlan.objects.filter(
        acreedor=object_list,
        start_date__lte=dia,
        fecha_limite__gte=dia_mas_uno
    ).first()
    plan = planPagosCredito(object_list).generar_plan()
    estado_cuenta = AccountStatement.objects.filter(acreedor=object_list).order_by('issue_date')
    
    
    generar_todas_las_cuotas_acreedores(object_list.codigo_acreedor)

    if siguiente_pago is None:
        siguiente_pago = PaymentPlan.objects.filter(acreedor=object_list).order_by('-id').first()
    
    saldo_actual = siguiente_pago.saldo_pendiente + siguiente_pago.mora + siguiente_pago.interest

    object_list.saldo_actual = saldo_actual
    object_list.save()
    

    context = {
        'title':'Detalle de Acreedor.',
        'object_list':object_list,
        'plan':plan,
        'siguiente_pago':siguiente_pago,
        'total_cuota':formatear_numero(planPagosCredito(object_list).calcular_total_cuotas()),
        'total_capital':formatear_numero(planPagosCredito(object_list).calcular_total_capital()),
        'total_interes':formatear_numero(planPagosCredito(object_list).calcular_total_interes()),
        'estado_cuenta':estado_cuenta,
        'total_moras':total_mora_pagada(estado_cuenta),
        'total_intereses':total_interes_pagada(estado_cuenta),
        'total_capitales':total_capital_pagada(estado_cuenta),
        'permisos':recorrer_los_permisos_usuario(request),
    }
        
    return render(request, template_name, context)

@login_required
@permiso_requerido('puede_ver_detalle_seguros')
def detail_seguro(request, id):
    template_name = 'contable/seguros/detail.html'
    object_list = get_object_or_404(Insurance, id=id)
    siguiente_pago = PaymentPlan.objects.filter(seguro=object_list).order_by('-id').first()
    plan = planPagosCredito(object_list).generar_plan()
    estado_cuenta = AccountStatement.objects.filter(seguro=object_list)
    
    context = {
        'title':'Detalle de Seguro.',
        'object_list':object_list,
        'plan':plan,
        'siguiente_pago':siguiente_pago,
        'total_cuota':formatear_numero(planPagosCredito(object_list).calcular_total_cuotas()),
        'total_capital':formatear_numero(planPagosCredito(object_list).calcular_total_capital()),
        'total_interes':formatear_numero(planPagosCredito(object_list).calcular_total_interes()),
        'estado_cuenta':estado_cuenta,
        'total_moras':total_mora_pagada(estado_cuenta),
        'total_intereses':total_interes_pagada(estado_cuenta),
        'total_capitales':total_capital_pagada(estado_cuenta),
        'permisos':recorrer_los_permisos_usuario(request),
    }
        
    return render(request, template_name, context)

@login_required
@permiso_requerido('puede_ver_detalle_ingresos')
def detail_ingreso(request, id):
    template_name = 'contable/ingresos/detail.html'
    object_list = get_object_or_404(Income, id=id)
  
    context = {
        'title':'Detalle de Ingreso.',
        'object_list':object_list,
        'permisos':recorrer_los_permisos_usuario(request),
        
    }
        
    return render(request, template_name, context)

@login_required
@permiso_requerido('puede_ver_detalle_egresos')
def detail_egreso(request, id):
    template_name = 'contable/egresos/detail.html'
    object_list = get_object_or_404(Egress, id=id)
  
    context = {
        'title':'Detalle de Egreso.',
        'object_list':object_list,
        'permisos':recorrer_los_permisos_usuario(request),
        
    }
        
    return render(request, template_name, context)