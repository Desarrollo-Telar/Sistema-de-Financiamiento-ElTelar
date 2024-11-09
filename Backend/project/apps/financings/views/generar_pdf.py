import os
from project.settings import MEDIA_ROOT, STATIC_ROOT, MEDIA_URL, STATIC_URL
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders


# MODELOS
from apps.financings.models import Recibo, Invoice
import os
from django.conf import settings
from django.contrib.staticfiles import finders
from django.utils._os import safe_join
from django.core.exceptions import SuspiciousFileOperation
from weasyprint import HTML





def render_pdf_factura(request,id):
    """
    recibo = get_object_or_404(Recibo, id=id)
    if not recibo.factura:
        return redirect(request.META.get('HTTP_REFERER', '/'))
    factura = Invoice.objects.filter(Q(recibo_id=recibo))
    """
    template_path = 'financings/credit/factura/factura_pdf.html'
    template = get_template(template_path)
    context = {
        'title':'ELTELAR',
        #'factura':factura,
        #'recibo':recibo
    }
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Factura.pdf"'
    HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response)

    

    return response