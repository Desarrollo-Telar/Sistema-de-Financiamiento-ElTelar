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

@login_required
@usuario_activo
def create_working_information(request, customer_code):
    template_name = ''
    customer_id = get_object_or_404(Customer, customer_code=str(customer_code))
    
    form = WorkingInformationForms
    context = {
        'form':form
    }
    if request.method == 'POST':
        form = WorkingInformationForms(request.POST)
        if form.is_valid():
            working = WorkingInformation()
            working.customer_id = customer_id
            working.position = form.cleaned_data.get('position')
            working.start_date = form.cleaned_data.get('start_date')
            working.description = form.cleaned_data.get('description')
            working.salary = form.cleaned_data.get('salary')
            working.working_hours = form.cleaned_data.get('working_hours')
            working.phone_number = form.cleaned_data.get('phone_number')
            working.source_of_income = form.cleaned_data.get('source_of_income')
            working.income_detail = form.cleaned_data.get('income_detail')
            working.employment_status = form.cleaned_data.get('employment_status')
            working.company_name = form.cleaned_data.get('company_name')
            working.save()

    return render(request, template_name, context)

@login_required
@usuario_activo
def create_other_information(request, customer_code):
    template_name = ''
    customer_id = get_object_or_404(Customer, customer_code=str(customer_code))
    form = OtherSourcesOfIncomeForms
    context = {
        'form':form
    }
    if request.method == 'POST':
        form = OtherSourcesOfIncomeForms(request.POST)
        if form.is_valid():
            other = OtherSourcesOfIncome()
            other.customer_id = customer_id
            other.nit = form.cleaned_data.get('nit')
            other.phone_number = form.cleaned_data.get('phone_number')
            other.salary = form.cleaned_data.get('salary')
            other.source_of_income = form.cleaned_data.get('source_of_income')
            other.save()
    return render(request, template_name, context)

@login_required
@usuario_activo
def delete_working_information(request, id, customer_code):
    working = get_object_or_404(WorkingInformation, id=id)
    working.delete()
    return redirect('customers:detail',customer_code)

@usuario_activo
def delete_other_information(request, id, customer_code):
    other = get_object_or_404(OtherSourcesOfIncome, id=id)
    other.delete()
    return redirect('customers:detail',customer_code)