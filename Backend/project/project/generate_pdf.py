from django.http import HttpResponse
from django.template.loader import get_template
from django.conf import settings
from weasyprint import HTML

# Modelos
from apps.users.models import User
from django.contrib.auth.models import AnonymousUser
from apps.customers.models import Customer
from apps.addresses.models import Address
from apps.FinancialInformation.models import WorkingInformation, OtherSourcesOfIncome, Reference
from apps.InvestmentPlan.models import InvestmentPlan
from django.db.models import Q

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import usuario_activo
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string

def generar_pdf(request,id):
    # Obtener la plantilla HTML
    template_path = 'customer/forms/forms_ive_pdf.html'  # Ruta a tu plantilla HTML
    template = get_template(template_path)
    
    customer_list = Customer.objects.filter(id=id).first()
    address_list = Address.objects.filter(customer_id=customer_list)
    working_information = WorkingInformation.objects.filter(customer_id=customer_list)
    other_information = OtherSourcesOfIncome.objects.filter(customer_id=customer_list)
    reference = Reference.objects.filter(customer_id=customer_list)
    plan = InvestmentPlan.objects.filter(customer_id=customer_list).first()

    context = {
        'title': 'EL TELAR - FORMULARIO IVE',
        'customer_list': customer_list,
        'address_list': address_list,  
        'working_information': working_information,
        'other_information': other_information,
        'reference': reference,
        'plan_list': plan,
    }

    html = template.render(context)

    # Convertir HTML a PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="Formulario IVE {}.pdf"'.format(customer_list.customer_code)
    HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response)

    return response
