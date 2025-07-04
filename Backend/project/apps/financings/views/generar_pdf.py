import os
from project.settings import MEDIA_ROOT, STATIC_ROOT, MEDIA_URL, STATIC_URL
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

from django.shortcuts import render, get_object_or_404, redirect

# TAREA ASINCRONICO
from apps.financings.task import cambiar_plan

# MODELOS
from apps.financings.models import Recibo, Invoice,AccountStatement,Credit,PaymentPlan, Payment, Cuota
from apps.accountings.models import Creditor, Insurance

import os
from django.conf import settings
from django.contrib.staticfiles import finders
from django.utils._os import safe_join
from django.core.exceptions import SuspiciousFileOperation
from weasyprint import HTML
# tiempo
from datetime import datetime,timedelta
# Obtener la fecha y hora actual
now = datetime.now()

def formatear_numero(numero):
    # Convertir el número a un formato con coma para miles y punto para decimales
    return f"{numero:,.2f}".replace(".", "X").replace(".", ",").replace("X", ".")



def total_desembolsos(estado_cuenta):
    contador = 0
    for estado in estado_cuenta:
        contador+=estado.disbursement_paid
    return formatear_numero(contador)

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

from django.db.models import Q

def render_pdf_factura(request,id):    
    recibo = get_object_or_404(Recibo, id=id)
    if not recibo.factura:
        return redirect(request.META.get('HTTP_REFERER', '/'))
    factura = Invoice.objects.filter(Q(recibo_id=recibo)).first()
    
   
    template_path = 'financings/credit/factura/factura_pdf.html'
    template = get_template(template_path)
    context = {
        'title':'ELTELAR',
        'factura':factura,
        'recibo':recibo
    }
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="Factura.pdf"'
    HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response)

    return response

def render_pdf_estado_cuenta(request,id):
    credito = get_object_or_404(Credit,id=id)
    estado_cuenta = AccountStatement.objects.filter(credit=credito).order_by('issue_date')
    dia = datetime.now().date()
    dia_mas_uno = dia + timedelta(days=1)
    
    siguiente_pago = PaymentPlan.objects.filter(
        credit_id=credito,
        start_date__lte=dia,
        fecha_limite__gte=dia_mas_uno
    ).first()

    if siguiente_pago is None:
        siguiente_pago = PaymentPlan.objects.filter(
        credit_id=credito).order_by('-id').first()

    template_path = 'financings/credit/estado_cuenta/pdf.html'
    template = get_template(template_path)
   
    #
    #actualizacion(credito)
    context = {
        'title':'ELTELAR',
        'credito':credito,
        'estado_cuenta':estado_cuenta,
        'total_desembolsos':total_desembolsos(estado_cuenta),
        'total_moras':total_mora_pagada(estado_cuenta),
        'total_intereses':total_interes_pagada(estado_cuenta),
        'total_capitales':total_capital_pagada(estado_cuenta),
        'dia':now,
        'siguiente_pago':siguiente_pago,
    }

    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = ' filename="Estado de Cuenta.pdf"'
    HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response)

    return response

def render_pdf_calculos_credito(request,id):
    
    credito = get_object_or_404(Credit,id=id)
    cuotas = PaymentPlan.objects.filter(credit_id=credito).order_by('mes')
    pagos = Payment.objects.filter(credit=credito)
    recibos = Recibo.objects.filter(pago__credit=credito).order_by('pago__fecha_emision')

    template_path = 'financings/calculos/calculos_hechos.html'
    template = get_template(template_path)
    #actualizacion(credito)
    cuotas_data = []
    for cuota in cuotas:
        recibos_asociados = recibos.filter(
            fecha__range=[cuota.start_date.date(), cuota.fecha_limite.date()]
        )
        cuotas_data.append({'cuota': cuota, 'recibos': recibos_asociados})

    context = {
        'title':'ELTELAR',
        'credito':credito,
        'cuotas':cuotas,
        'pagos':pagos,
        'recibos':recibos,
        'cuotas_data': cuotas_data,
    }

    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = ' filename="ReporteSobrePagos.pdf"'
    HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response)

    return response

def render_pdf_calculos_credito_acreedor(request,id):
    
    credito = get_object_or_404(Creditor,id=id)
    cuotas = PaymentPlan.objects.filter(acreedor=credito)
    pagos = Payment.objects.filter(acreedor=credito)
    recibos = Recibo.objects.filter(pago__acreedor=credito)

    template_path = 'contable/calculos/calculos_hechos.html'
    template = get_template(template_path)
    #actualizacion(credito)
    cuotas_data = []
    for cuota in cuotas:
        recibos_asociados = recibos.filter(
            fecha__range=[cuota.start_date.date(), cuota.fecha_limite.date()]
        )
        cuotas_data.append({'cuota': cuota, 'recibos': recibos_asociados})

    context = {
        'title':'ELTELAR',
        'credito':credito,
        'cuotas':cuotas,
        'pagos':pagos,
        'recibos':recibos,
        'cuotas_data': cuotas_data,
    }

    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = ' filename="ReporteSobrePagos.pdf"'
    HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response)

    return response

def render_pdf_calculos_credito_seguro(request,id):
    
    credito = get_object_or_404(Insurance,id=id)
    cuotas = PaymentPlan.objects.filter(seguro=credito)
    pagos = Payment.objects.filter(seguro=credito)
    recibos = Recibo.objects.filter(pago__seguro=credito)

    template_path = 'contable/calculos/calculos_hechos.html'
    template = get_template(template_path)
    #actualizacion(credito)
    cuotas_data = []
    for cuota in cuotas:
        recibos_asociados = recibos.filter(
            fecha__range=[cuota.start_date.date(), cuota.fecha_limite.date()]
        )
        cuotas_data.append({'cuota': cuota, 'recibos': recibos_asociados})

    context = {
        'title':'ELTELAR',
        'credito':credito,
        'cuotas':cuotas,
        'pagos':pagos,
        'recibos':recibos,
        'cuotas_data': cuotas_data,
    }

    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = ' filename="ReporteSobrePagos.pdf"'
    HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response)

    return response

# CLASES
from apps.financings.clases.paymentplan import PaymentPlan as PlanPagoos
from apps.financings.clases.credit import Credit as Credito

def planPagosCredito(credito):
    formatted_date = credito.fecha_inicio.strftime('%Y-%m-%d')
    credit = Credito(credito.proposito,credito.monto,credito.plazo,credito.tasa_interes,credito.forma_de_pago,credito.frecuencia_pago,formatted_date,credito.tipo_credito,1,None,credito.fecha_vencimiento)
    plan_pago = PlanPagoos(credit)
    return plan_pago

def planPagosCreditoAS(credito):
    formatted_date = credito.fecha_inicio.strftime('%Y-%m-%d')
    credit = Credito('credito proposito',credito.monto,credito.plazo,credito.tasa,credito.forma_de_pago,'MENSAUL',formatted_date,'credito.tipo_credito',1,None,credito.fecha_vencimiento)
    plan_pago = PlanPagoos(credit)
    return plan_pago

def render_pdf_plan_pagos(request,id):
    
    credito = get_object_or_404(Credit,id=id)    
    plan = planPagosCredito(credito).recalcular_capital()
    

    template_path = 'financings/credit/plan_pagos/detail.html'
    template = get_template(template_path)
    
    

    context = {
        'title':'ELTELAR',
        'credito':credito,
        'plan':plan,
        'total_cuota':formatear_numero(planPagosCredito(credito).calcular_total_cuotas()),
        'total_capital':formatear_numero(planPagosCredito(credito).calcular_total_capital()),
        'total_interes':formatear_numero(planPagosCredito(credito).calcular_total_interes()),
        
        
    }

    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = ' filename="plan_pagos.pdf"'
    HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response)

    return response

def render_pdf_plan_pagos_acreedor(request,id):
    
    credito = get_object_or_404(Creditor,id=id)    
    plan = planPagosCreditoAS(credito).recalcular_capital()
    

    template_path = 'contable/acreedores/plan_pagos/detail.html'
    template = get_template(template_path)
    
    

    context = {
        'title':'ELTELAR',
        'credito':credito,
        'plan':plan,
        'total_cuota':formatear_numero(planPagosCreditoAS(credito).calcular_total_cuotas()),
        'total_capital':formatear_numero(planPagosCreditoAS(credito).calcular_total_capital()),
        'total_interes':formatear_numero(planPagosCreditoAS(credito).calcular_total_interes()),
        
        
    }

    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = ' filename="plan_pagos.pdf"'
    HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response)

    return response

def render_pdf_plan_pagos_seguro(request,id):
    
    credito = get_object_or_404(Insurance,id=id)    
    plan = planPagosCreditoAS(credito).recalcular_capital()
    

    template_path = 'contable/acreedores/plan_pagos/detail.html'
    template = get_template(template_path)
    
    

    context = {
        'title':'ELTELAR',
        'credito':credito,
        'plan':plan,
        'total_cuota':formatear_numero(planPagosCreditoAS(credito).calcular_total_cuotas()),
        'total_capital':formatear_numero(planPagosCreditoAS(credito).calcular_total_capital()),
        'total_interes':formatear_numero(planPagosCreditoAS(credito).calcular_total_interes()),
        
        
    }

    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = ' filename="plan_pagos.pdf"'
    HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response)

    return response