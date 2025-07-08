from django.shortcuts import render, get_object_or_404, redirect



# Models
from apps.customers.models import Customer, CreditCounselor
from apps.addresses.models import Address
from apps.FinancialInformation.models import WorkingInformation, OtherSourcesOfIncome, Reference
from apps.InvestmentPlan.models import InvestmentPlan
from apps.pictures.models import ImagenCustomer
from apps.documents.models import DocumentCustomer
from apps.financings.models import Credit
from django.db.models import Q

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import permiso_requerido



# MENSAJES
from django.contrib import messages



# SCRIPTS
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario
# ----- VER DETALLES DE UN CLIENTE ----- #
@login_required
@permiso_requerido('puede_visualizar_detalle_cliente')
def detail_customer(request,customer_code):
    template_name = 'customer/detail.html'
    
    customer_list = get_object_or_404(Customer,customer_code=customer_code)

    asesor_autenticado = CreditCounselor.objects.filter(usuario=request.user).first()

    if asesor_autenticado is not None and request.user.rol.role_name == 'Asesor de Crédito':
        customer_list = Customer.objects.filter(customer_code=str(customer_code), new_asesor_credito=asesor_autenticado).first()
        if customer_list is None:
            messages.error(request,'No tienes permitido visualizar el perfil de este cliente.')
            return redirect('customers:customers')


    informacion_laboral = WorkingInformation.objects.filter(Q(customer_id=customer_list))
    otra_informacion_laboral = OtherSourcesOfIncome.objects.filter(Q(customer_id=customer_list))
    direccion = Address.objects.filter(Q(customer_id=customer_list))
    
    plan_inversion = InvestmentPlan.objects.filter(Q(customer_id=customer_list))
    reference = Reference.objects.filter(Q(customer_id=customer_list))
    imagen = ImagenCustomer.objects.filter(Q(customer_id=customer_list))
    document = DocumentCustomer.objects.filter(Q(customer_id=customer_list))
    credito = Credit.objects.filter(Q(customer_id =customer_list ))

    #print(credito)
      
    

    limite_direccion = False if direccion.count() >= 2 else True

    context = {
        'title': 'Detalle de la Informacion del Cliente. {} {} / {}'.format(customer_list.first_name, customer_list.last_name,str(customer_code)),
        'customer_list':customer_list,
        'user_id':request.user.id,
        'direccion': direccion,  
        'informacion_laboral' :informacion_laboral,
        'laboral':informacion_laboral.exists(),
        'otra':otra_informacion_laboral.exists(),
        'otra_informacion_laboral' :otra_informacion_laboral,
        'reference':reference,
        'plan_inversion':plan_inversion,
        'credit_list':credito,
        'customer_code':customer_code,
        'limite_direccion':limite_direccion,
        'imagen':imagen,
        'document':document,
        'permisos':recorrer_los_permisos_usuario(request),
    }
    return render(request, template_name, context)