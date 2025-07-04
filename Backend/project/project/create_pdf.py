
from django.template.loader import get_template

# Modelos
from apps.users.models import User
from django.contrib.auth.models import AnonymousUser
from apps.customers.models import Customer
from apps.addresses.models import Address
from apps.FinancialInformation.models import WorkingInformation, OtherSourcesOfIncome, Reference
from apps.InvestmentPlan.models import InvestmentPlan
from django.db.models import Q

def printIVE(id):
    template = get_template('customer/forms/forms_ive.html')
    customer_list = get_object_or_404(Customer, id=id)
    address_list = Address.objects.filter(customer_id=customer_list)
    working_information = WorkingInformation.objects.filter(customer_id=customer_list)
    other_information = OtherSourcesOfIncome.objects.filter(customer_id=customer_list)
    reference = Reference.objects.filter(customer_id=customer_list)
    plan = InvestmentPlan.objects.filter(customer_id=customer_list)

    context = {
        'title': 'EL TELAR - FORMULARIO IVE',
        'customer_list': customer_list,
        'address_list': address_list,  
        'working_information': working_information,
        'other_information': other_information,
        'reference': reference,
        'plan_list': plan,
    }

    html_template = template.render(context)
    

if __name__ == '__main__':
    print("Hola Mundo")