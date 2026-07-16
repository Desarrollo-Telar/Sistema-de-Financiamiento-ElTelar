from django.shortcuts import render, get_object_or_404, redirect

# Formulario
from apps.actividades.forms.votaciones import VotacionClienteForm

# Models
from apps.customers.models import Customer, CreditCounselor
from apps.addresses.models import Address
from apps.FinancialInformation.models import WorkingInformation, OtherSourcesOfIncome, Reference, GastoCliente
from apps.InvestmentPlan.models import InvestmentPlan
from apps.pictures.models import ImagenCustomer
from apps.documents.models import DocumentCustomer
from apps.financings.models import Credit
from django.db.models import Q
from apps.actividades.models import VotacionCliente

# FORMATO
from apps.financings.formato import formatear_numero


# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import permiso_requerido



# MENSAJES
from django.contrib import messages
from project.send_mail import send_email_new_customer


# SCRIPTS
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario

def check_list_customer(request, customer_code):
    
    customer = Customer.objects.filter(customer_code=customer_code).first()
    listado_clientes_no_permitidos = ['No Aprobado',  'Dar de Baja']

    info_trabajo = WorkingInformation.objects.filter(customer_id=customer).first()
    info_ingresos = OtherSourcesOfIncome.objects.filter(customer_id=customer).first()
    info_referencias = Reference.objects.filter(customer_id=customer).first()
    info_gastos = GastoCliente.objects.filter(customer=customer).first()

    if customer is None :
        return redirect('customers:customers')
    
    if customer.status in listado_clientes_no_permitidos:
        pass
    
    if info_trabajo is None or info_ingresos is None:
        messages.error(request,'No el Cliente no tiene información de sus ingresos registrados.')
    
    if info_referencias is None:
        messages.error(request,'No el Cliente no tiene información de referencias registrada.')
    
    if info_gastos is None:
        messages.error(request,'No el Cliente no tiene información de gastos registrada.')
    
    if not customer.completado:
        customer.completado = True
        customer.save()

        send_email_new_customer(customer)
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

    check_list_customer(request, customer_code)
    informacion_laboral = WorkingInformation.objects.filter(Q(customer_id=customer_list))
    otra_informacion_laboral = OtherSourcesOfIncome.objects.filter(Q(customer_id=customer_list))
    
    direccion = Address.objects.filter(Q(customer_id=customer_list))
    
    plan_inversion = InvestmentPlan.objects.filter(Q(customer_id=customer_list))
    reference = Reference.objects.filter(Q(customer_id=customer_list))
    imagen = ImagenCustomer.objects.filter(Q(customer_id=customer_list))
    document = DocumentCustomer.objects.filter(Q(customer_id=customer_list))
    credito = Credit.objects.filter(Q(customer_id =customer_list )).order_by('id')
    comentarios = VotacionCliente.objects.filter(cliente=customer_list).order_by('-id')
    gastos_cliente = GastoCliente.objects.filter(Q(customer=customer_list))
    #print(credito)
      
    

    limite_direccion = False if direccion.count() >= 2 else True

    context = {
        'title': 'Detalle de la Informacion del Cliente | {} {} | {}'.format(customer_list.first_name, customer_list.last_name,str(customer_code)),
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
        'form':VotacionClienteForm(),
        'comentarios':comentarios,
        'gastos_cliente':gastos_cliente,
        'total_ingresos': formatear_numero(customer_list.total_ingresos()),
        'total_egresos': formatear_numero(customer_list.total_egresos()),
        'disponibilidad_efectiva': formatear_numero(customer_list.disponibilidad_efectiva()),
    }
    return render(request, template_name, context)