from django.shortcuts import render, get_object_or_404, redirect

# Models
from .models import Credit
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
def list_credit(request):
    template_name = 'financings/credit/list.html'
    page_obj = paginacion(request, Credit.objects.all().order_by('-id'))
    context = {
        'title':'ELTELAR - CREDITOS',
        'page_obj':page_obj,
        'credit_list':page_obj
    }
    return render(request, template_name, context)