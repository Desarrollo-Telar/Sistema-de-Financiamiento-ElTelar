from django.shortcuts import render, get_object_or_404, redirect

# Models
from apps.financings.models import Credit, Guarantees, Disbursement,DetailsGuarantees, Banco, Payment, PaymentPlan, AccountStatement, Recibo
from apps.customers.models import Customer
from apps.financings.models import Invoice


from django.db.models import Q

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import usuario_activo
from django.utils.decorators import method_decorator

from datetime import datetime,timedelta
# Obtener la fecha y hora actual
now = datetime.now()
# CLASES
from apps.financings.clases.paymentplan import PaymentPlan as PlanPagoos
from apps.financings.clases.credit import Credit as Credito

# TAREA ASINCRONICO
from apps.financings.task import cambiar_plan

# LIBRERIAS PARA CRUD
from django.views.generic import CreateView
from django.views.generic.list import ListView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic.detail import DetailView
from django.db.models import Q

@login_required
@usuario_activo
def filter_credito_reciente(request):
    template_name = 'financings/credit/list.html'
    hoy = datetime.now()
    inicio = hoy - timedelta(days=5)
    page_obj = paginacion(request, Credit.objects.filter(Q(creation_date__range=[inicio,hoy])).order_by('-id'))
    
    context = {
        'title':'ELTELAR - CREDITOS',
        'page_obj':page_obj,
        'credit_list':page_obj,
        'count': Credit.objects.filter(is_paid_off=True).count()
    }
    return render(request, template_name, context)

@login_required
@usuario_activo
def filter_credito_cancelado(request):
    template_name = 'financings/credit/list.html'
    page_obj = paginacion(request, Credit.objects.filter(is_paid_off=True).order_by('-id'))
    
    context = {
        'title':'ELTELAR - CREDITOS',
        'page_obj':page_obj,
        'credit_list':page_obj,
        'count': Credit.objects.filter(is_paid_off=True).count()
    }
    return render(request, template_name, context)

@login_required
@usuario_activo
def filter_credito_en_atraso(request):
    template_name = 'financings/credit/list.html'
    page_obj = paginacion(request, Credit.objects.filter(estados_fechas=False).order_by('-id'))
    
    context = {
        'title':'ELTELAR - CREDITOS',
        'page_obj':page_obj,
        'credit_list':page_obj,
        'count': Credit.objects.filter(estados_fechas=False).count()
    }
    return render(request, template_name, context)

@login_required
@usuario_activo
def filter_credito_en_falta_aportacion(request):
    template_name = 'financings/credit/list.html'
    page_obj = paginacion(request, Credit.objects.filter(estado_aportacion=True).order_by('-id'))
    
    context = {
        'title':'ELTELAR - CREDITOS',
        'page_obj':page_obj,
        'credit_list':page_obj,
        'count': Credit.objects.filter(estado_aportacion=True).count()
    }
    return render(request, template_name, context)