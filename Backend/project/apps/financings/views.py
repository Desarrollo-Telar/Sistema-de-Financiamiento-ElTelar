from django.shortcuts import render, get_object_or_404, redirect

# Models
from .models import Credit, Guarantees, Disbursement,DetailsGuarantees
from apps.addresses.models import Address
from apps.FinancialInformation.models import WorkingInformation, OtherSourcesOfIncome, Reference
from apps.InvestmentPlan.models import InvestmentPlan
from apps.pictures.models import ImagenCustomer
from apps.documents.models import DocumentCustomer

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

# Create your views here.
### ------------------- CREAR ---------------------- ###
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
    context = {
        'title':'ELTELAR - CREDITO',
        'credit_list':credito

    }
    return render(request, template_name,context)
