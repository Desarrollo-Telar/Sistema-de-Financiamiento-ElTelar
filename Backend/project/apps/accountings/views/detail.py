from django.shortcuts import render, get_object_or_404, redirect

# TIEMPO
from datetime import datetime,timedelta

# Manejo de mensajes
from django.contrib import messages

# Models
from apps.accountings.models import Creditor, Insurance,  Egress, Income
from apps.financings.models import Payment, PaymentPlan, AccountStatement

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
# TAREA ASINCRONICO
from apps.financings.task import cambiar_plan
from apps.financings.tareas_ansicronicas import generar_todas_las_cuotas_acreedores


# MENSAJES
from django.contrib import messages

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
@usuario_administrador
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
    
    cambiar_plan()
    generar_todas_las_cuotas_acreedores(object_list.codigo_acreedor)

    if siguiente_pago is None:
        siguiente_pago = PaymentPlan.objects.filter(acreedor=object_list).order_by('-id').first()
    
    saldo_actual = siguiente_pago.saldo_pendiente + siguiente_pago.mora + siguiente_pago.interest

    object_list.saldo_actual = saldo_actual
    object_list.save()
    

    context = {
        'title':'EL TELAR',
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
    }
        
    return render(request, template_name, context)

@login_required
@usuario_administrador
def detail_seguro(request, id):
    template_name = 'contable/seguros/detail.html'
    object_list = get_object_or_404(Insurance, id=id)
    siguiente_pago = PaymentPlan.objects.filter(seguro=object_list).order_by('-id').first()
    plan = planPagosCredito(object_list).generar_plan()
    estado_cuenta = AccountStatement.objects.filter(seguro=object_list)
    cambiar_plan()
    context = {
        'title':'EL TELAR',
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
    }
        
    return render(request, template_name, context)

@login_required
@usuario_activo
def detail_ingreso(request, id):
    template_name = 'contable/ingresos/detail.html'
    object_list = get_object_or_404(Income, id=id)
  
    context = {
        'title':'EL TELAR',
        'object_list':object_list
        
    }
        
    return render(request, template_name, context)

@login_required
@usuario_activo
def detail_egreso(request, id):
    template_name = 'contable/egresos/detail.html'
    object_list = get_object_or_404(Egress, id=id)
  
    context = {
        'title':'EL TELAR',
        'object_list':object_list
        
    }
        
    return render(request, template_name, context)