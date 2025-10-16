import os
from project.settings import MEDIA_ROOT, STATIC_ROOT, MEDIA_URL, STATIC_URL
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

from django.shortcuts import render, get_object_or_404, redirect

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
from django.db.models import Q

def generar_pagare_pdf(request, id):
    credito = Credit.objects.get(id=id)
    template_path = 'financings/credit/pagare/pagare_pdf.html'
    template = get_template(template_path)
    context = {
        'title':'ELTELAR',
        'credito':credito
    }
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="pagare.pdf"'
    HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response)

    return response