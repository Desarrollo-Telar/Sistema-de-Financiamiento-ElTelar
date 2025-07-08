from django.shortcuts import render, get_object_or_404, redirect



# Models
from apps.customers.models import Customer
from apps.addresses.models import Address
from apps.FinancialInformation.models import WorkingInformation, OtherSourcesOfIncome, Reference
from apps.InvestmentPlan.models import InvestmentPlan
from django.db.models import Q



# SCRIPTS
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario

# ----- VER FORMULARIO IVE ----- #
def formulario_ive(request, id):
    template_name = 'customer/forms/forms_ive.html'
    customer_list = get_object_or_404(Customer, id=id)
    address_list = Address.objects.filter(Q(customer_id=customer_list))
    working_information = WorkingInformation.objects.filter(Q(customer_id=customer_list))
    other_information = OtherSourcesOfIncome.objects.filter(Q(customer_id=customer_list))
    reference = Reference.objects.filter(Q(customer_id=customer_list))
    plan = InvestmentPlan.objects.filter(Q(customer_id=customer_list)).first()

    context = {
        'title':f'Formulario IVE del Cliente. {customer_list} ',
        'customer_list':customer_list,
        'address_list': address_list,  
        'working_information' :working_information,
        'other_information' :other_information,
        'reference':reference,
        'plan':plan,
        'permisos':recorrer_los_permisos_usuario(request),
        
    }
    return render(request, template_name, context)