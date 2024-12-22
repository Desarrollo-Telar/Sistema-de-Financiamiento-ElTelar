from django.shortcuts import render, get_object_or_404, redirect

# Models
from .models import Credit, Guarantees, Disbursement,DetailsGuarantees, Banco, Payment, PaymentPlan, AccountStatement, Recibo
from apps.customers.models import Customer
from apps.addresses.models import Address
from apps.FinancialInformation.models import WorkingInformation, OtherSourcesOfIncome, Reference
from apps.InvestmentPlan.models import InvestmentPlan
from apps.pictures.models import ImagenCustomer
from apps.documents.models import DocumentCustomer, DocumentBank
#from .models import AccountStatement
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

# TAREA ASINCRONICO
from .task import cambiar_plan
# TIEMPO
from datetime import datetime, timedelta

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
    
    generar()


    context = {
        'title':'EL TELAR - PAGOS',
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
        'title':'EL TELAR - BANCOS',
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
from datetime import datetime
from .task import cambiar_plan
@login_required
@usuario_activo
def detail_credit(request,id):
    template_name = 'financings/credit/detail.html'
    credito= get_object_or_404(Credit,id=id)
    cambiar_plan()
    
    customer_list = get_object_or_404(Customer,id= credito.customer_id.id)
    list_guarantee = Guarantees.objects.filter(credit_id=credito).order_by('-id')
    list_disbursement = Disbursement.objects.filter(credit_id=credito).order_by('-id')

    formatted_date = credito.fecha_inicio.strftime('%Y-%m-%d')
    siguiente_pago = PaymentPlan.objects.filter(credit_id=credito)
    estado_cuenta = AccountStatement.objects.filter(credit=credito)
    pagos = PaymentPlan.objects.filter(credit_id=credito).order_by('-id').first()
    

    
    
    if pagos:
        credito.saldo_pendiente = pagos.saldo_pendiente
        credito.saldo_actual = pagos.saldo_pendiente + pagos.mora + pagos.interest
        credito.save()
    
    

   
    

    
       
    
    credit = Credito(credito.proposito,credito.monto,credito.plazo,credito.tasa_interes,credito.forma_de_pago,credito.frecuencia_pago,formatted_date,credito.tipo_credito,1,None,credito.fecha_vencimiento)
    
    plan_pago = PlanPagoos(credit)
    total_garantia = 0
    total_desembolso = 0
    for garantia in list_guarantee:
        total_garantia += garantia.suma_total
    
    for desembolso in list_disbursement:
        total_desembolso +=desembolso.monto_total_desembolso
    
    plan = plan_pago.generar_plan()
   
   
    context = {
        'title':'ELTELAR - CREDITO',
        'credit_list':credito,
        'customer_list':customer_list,
        'plan':plan,
        'list_guarantee':list_guarantee,
        'list_disbursement':list_disbursement,
        'detalle_garantia':DetailsGuarantees.objects.all(),
        'total_garantia':total_garantia,
        'total_desembolso':total_desembolso,
        'estado_cuenta':estado_cuenta,
        'siguiente_pago':siguiente_pago,
        'total_cuota':plan_pago.calcular_total_cuotas(),
        'total_capital':plan_pago.calcular_total_capital(),
        'total_interes':plan_pago.calcular_total_interes()

    }
    return render(request, template_name,context)

@login_required
@usuario_activo
def detallar_recibo(request,id):
    """
    desembolso = get_object_or_404(Disbursement,id=id)
    if desembolso:
        return redirect('index')
    """
    pago = get_object_or_404(Payment, id=id)
    
    recibo = get_object_or_404(Recibo, pago=pago)

    

   
    template_name = 'financings/credit/recibo/detail.html'
    context = {
        'title':'ELTELAR - RECIBO',
        'recibo':recibo,
    }
    return render(request, template_name, context)


@login_required
@usuario_activo
def detalle_boleta(request,id):
    pago = get_object_or_404(Payment, id=id)
    template_name = 'financings/payment/detail.html'
    context = {
        'title':f'ELTELAR - BOLETA {pago.numero_referencia}',
        'pago':pago,
    }
    return render(request, template_name, context)



### ---------------- ACTUALIZAR --------------------
@login_required
@usuario_activo
def update_pago(request,id):
    template_name = ''
    pago = get_object_or_404(Payment,id=id)
    context = {
        'title':'ELTELAR'
    }
    return render(request)

# ------------------ BUSCADOR ------------------------------
class BankSearch(ListView):
    template_name = 'financings/bank/search.html'

    def get_queryset(self):
        try:
            # Asignar la consulta a una variable local
            query = self.query()

            # Crear una lista para almacenar los filtros
            filters = Q()

            # Añadir filtros si la consulta no está vacía
            if query:
                filters |= Q(fecha__icontains=query)
                filters |= Q(referencia__icontains=query)

                # Si la consulta es numérica, usar filtro exacto para campos numéricos
                if query.isdigit():
                    filters |= Q(credito__exact=query)
                    filters |= Q(debito__exact=query)

            # Filtrar los objetos Banco usando los filtros definidos
            return Banco.objects.filter(filters)
        except Exception as e:
            # Manejar cualquier excepción que ocurra y devolver un queryset vacío
            print(f"Error al filtrar el queryset: {e}")
            return Banco.objects.none()
    

    def query(self):
        return self.request.GET.get('q')
    
    @method_decorator(usuario_activo)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.query()
        context['title'] = 'ELTELAR - Buscar'
        context['count'] = context['object_list'].count()
        return context

class PaymentSearch(ListView):
    template_name = 'financings/payment/search.html'

    def get_queryset(self):
        try:
            # Asignar la consulta a una variable local
            query = self.query()

            # Crear una lista para almacenar los filtros
            filters = Q()

            # Añadir filtros si la consulta no está vacía
            if query:
                filters |= Q(fecha_emision__icontains=query)
                filters |= Q(numero_referencia__icontains=query)
                filters |= Q(estado_transaccion__icontains=query)
                filters |= Q(credit__codigo_credito__icontains=query)
                filters |= Q(tipo_pago__icontains=query)

                # Si la consulta es numérica, usar filtro exacto para campos numéricos
                if query.isdigit():
                    filters |= Q(monto__exact=query)
                    #filters |= Q(numero_referencia__exact=query)

            # Filtrar los objetos Banco usando los filtros definidos
            return Payment.objects.filter(filters)
        except Exception as e:
            # Manejar cualquier excepción que ocurra y devolver un queryset vacío
            print(f"Error al filtrar el queryset: {e}")
            return Payment.objects.none()
    

    def query(self):
        return self.request.GET.get('q')
    
    @method_decorator(usuario_activo)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.query()
        context['title'] = 'ELTELAR - Buscar'
        context['count'] = context['object_list'].count()
        return context