import os
from project.settings import MEDIA_ROOT, STATIC_ROOT, MEDIA_URL, STATIC_URL
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

from django.shortcuts import render, get_object_or_404, redirect

# MODELOS
from apps.financings.models import Recibo, Invoice,AccountStatement,Credit,PaymentPlan, Payment, Cuota

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

def actualizacion(credito):
    pagos = PaymentPlan.objects.filter(credit_id=credito).order_by('-id').first()
    
    # ACTUALIZAR EL SALDO ACTUAL
    if pagos:
        credito.saldo_pendiente = pagos.saldo_pendiente
        credito.saldo_actual = pagos.saldo_pendiente + pagos.mora + pagos.interest
        credito.save()

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


def render_pdf_factura(request,id):    
    recibo = get_object_or_404(Recibo, id=id)
    if not recibo.factura:
        return redirect(request.META.get('HTTP_REFERER', '/'))
    factura = Invoice.objects.filter(Q(recibo_id=recibo))
   
    template_path = 'financings/credit/factura/factura_pdf.html'
    template = get_template(template_path)
    context = {
        'title':'ELTELAR',
        'factura':factura,
        'recibo':recibo
    }
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Factura.pdf"'
    HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response)

    return response

def render_pdf_estado_cuenta(request,id):
    credito = get_object_or_404(Credit,id=id)
    estado_cuenta = AccountStatement.objects.filter(credit=credito)
    siguiente_pago = PaymentPlan.objects.filter(credit_id=credito).order_by('-id').first()

    template_path = 'financings/credit/estado_cuenta/pdf.html'
    template = get_template(template_path)
    actualizacion(credito)
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
    cuotas = PaymentPlan.objects.filter(credit_id=credito)
    pagos = Payment.objects.filter(credit=credito)
    recibos = Recibo.objects.filter(pago__credit=credito)

    template_path = 'financings/calculos/calculos_hechos.html'
    template = get_template(template_path)
    actualizacion(credito)
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
    response['Content-Disposition'] = ' filename="CalculosRealizados.pdf"'
    HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response)

    return response