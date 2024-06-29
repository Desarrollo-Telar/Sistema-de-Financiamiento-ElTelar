from django.shortcuts import render, get_object_or_404, redirect

# FORMULARIO
from .forms import WorkingInformationForms,OtherSourcesOfIncomeForms,ReferenceForms

# MODELOS
from apps.customers.models import Customer
from .models import WorkingInformation, OtherSourcesOfIncome, Reference

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

# Create your views here.

@login_required
@usuario_activo
def delete_other_information(request,id, customer_code):
    other = get_object_or_404(OtherSourcesOfIncome, id = id)
    other.delete()
    return redirect('customers:detail', customer_code)

@login_required
@usuario_activo
def delete_working_information(request,id, customer_code):
    working = get_object_or_404(WorkingInformation, id = id)
    working.delete()
    return redirect('customers:detail', customer_code)