from django.shortcuts import render, get_object_or_404, redirect

# Models
from .models import Credit, Guarantees, Disbursement,DetailsGuarantees, Banco, Payment, PaymentPlan, AccountStatement
from apps.customers.models import Customer
from apps.addresses.models import Address
from apps.FinancialInformation.models import WorkingInformation, OtherSourcesOfIncome, Reference
from apps.InvestmentPlan.models import InvestmentPlan
from apps.pictures.models import ImagenCustomer
from apps.documents.models import DocumentCustomer, DocumentBank

# LIBRERIAS PARA CRUD
from django.views.generic import CreateView
from django.views.generic.list import ListView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic.detail import DetailView
from django.db.models import Q

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import usuario_activo
from django.utils.decorators import method_decorator

# Paginacion
from project.pagination import paginacion

# CLASES
from .clases.paymentplan import PaymentPlan as PlanPagoos
from .clases.credit import Credit as Credito

# Create your views here.
### ------------------- CREAR ---------------------- ###
@login_required
@usuario_activo
def create_payment(request):
    template_name = 'financings/payment/create.html'
    context = {
        'title':'ELTELAR - PAGOS'
    }

    return render(request,template_name,context)

@login_required
@usuario_activo
def create_credit(request):
    template_name = 'financings/credit/create.html'
    context = {
        'title':'ELTELAR - CREDITO'
    }

    return render(request,template_name,context)

@login_required
@usuario_activo
def create_disbursement(request):
    template_name = 'financings/disbursement/create.html'
    context = {
        'title':'ELTELAR - DESEMBOLSO'
    }

    return render(request,template_name,context)

@login_required
@usuario_activo
def create_guarantee(request):
    template_name = 'financings/guarantee/create.html'
    context = {
        'title':'ELTELAR - GARANTIA'
    }

    return render(request,template_name,context)

### ----------------- LISTAR ------------------------ ###    
from .functions import realizar_pago
from .functions_payment import generar
@login_required
@usuario_activo
def list_payment(request):
    template_name = 'financings/payment/list.html'
    page_obj = paginacion(request, Payment.objects.all().order_by('id'))
    
    #generar()


    context = {
        'title':'EL TELAR',
        'page_obj':page_obj,
        'payment_list':page_obj

        
    }
    return render(request,template_name, context)

@login_required
@usuario_activo
def list_bank(request):
    template_name = 'financings/bank/list.html'
    page_obj = paginacion(request, Banco.objects.all().order_by('-fecha'))
    

    context = {
        'title':'EL TELAR',
        'page_obj':page_obj,
        'bank_list':page_obj
    }
    return render(request,template_name, context)

@login_required
@usuario_activo
def list_credit(request):
    template_name = 'financings/credit/list.html'
    page_obj = paginacion(request, Credit.objects.all().order_by('-id'))
    context = {
        'title':'ELTELAR - CREDITOS',
        'page_obj':page_obj,
        'credit_list':page_obj
    }
    return render(request, template_name, context)

@login_required
@usuario_activo
def list_guarantee(request):
    template_name = 'financings/guarantee/lists.html'
    page_obj = paginacion(request, Guarantees.objects.all().order_by('-id'))

    context = {
        'title':'ELTELAR - GARANTIAS',
        'page_obj':page_obj,
        'list_guarantee':page_obj,
        'detalle_garantia':DetailsGuarantees.objects.all(),
    }
    return render(request, template_name, context)

@login_required
@usuario_activo
def list_disbursement(request):
    template_name = 'financings/disbursement/list.html'
    page_obj = paginacion(request, Disbursement.objects.all().order_by('-id'))
    context = {
        'title':'ELTELAR - DESEMBOLSOS',
        'page_obj':page_obj,
        'list_disbursement':page_obj
    }
    return render(request, template_name, context)


### ------------ DETALLE -------------- ###
@login_required
@usuario_activo
def detail_credit(request,id):
    template_name = 'financings/credit/detail.html'
    credito= get_object_or_404(Credit,id=id)
    
    customer_list = get_object_or_404(Customer,id= credito.customer_id.id)
    list_guarantee = Guarantees.objects.filter(credit_id=credito).order_by('-id')
    list_disbursement = Disbursement.objects.filter(credit_id=credito).order_by('-id')

    formatted_date = credito.fecha_inicio.strftime('%Y-%m-%d')
    plan_pago = PaymentPlan.objects.filter(credit_id=credito)
    estado_cuenta = AccountStatement.objects.filter(credit=credito)
    cuotas = PaymentPlan.objects.filter(credit_id=credito, status=False).order_by('due_date').first()
    
    
    print(cuotas)
    
    #credit = Credito(credito.proposito,credito.monto,credito.plazo,credito.tasa_interes,credito.forma_de_pago,credito.frecuencia_pago,formatted_date,credito.tipo_credito,1)
    #plan_pago = PaymentPlan(credit)
    total_garantia = 0
    total_desembolso = 0
    for garantia in list_guarantee:
        total_garantia += garantia.suma_total
    
    for desembolso in list_disbursement:
        total_desembolso +=desembolso.monto_total_desembolso
    
    #plan = plan_pago.generar_plan()
     
    context = {
        'title':'ELTELAR - CREDITO',
        'credit_list':credito,
        'customer_list':customer_list,
        'plan':plan_pago,
        'list_guarantee':list_guarantee,
        'list_disbursement':list_disbursement,
        'detalle_garantia':DetailsGuarantees.objects.all(),
        'total_garantia':total_garantia,
        'total_desembolso':total_desembolso,
        'estado_cuenta':estado_cuenta,

    }
    return render(request, template_name,context)
