from django.shortcuts import render, get_object_or_404, redirect

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import usuario_activo
from django.utils.decorators import method_decorator

# LIBRERIAS PARA CRUD
from django.views.generic import CreateView
from django.views.generic.list import ListView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic.detail import DetailView
from django.db.models import Q


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
