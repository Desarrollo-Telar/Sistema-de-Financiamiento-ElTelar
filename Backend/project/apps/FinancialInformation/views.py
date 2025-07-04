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

# Scripts
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario

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
    template_name = 'FinancialInformation/create_working_information.html'
    customer_id = get_object_or_404(Customer, customer_code=str(customer_code))
    
    form = WorkingInformationForms
    context = {
        'form':form,
        'customer_code':customer_code,
        'permisos':recorrer_los_permisos_usuario(request)
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
            return redirect('customer:detail',customer_code)

        else:
            return render(request, template_name, context)

    return render(request, template_name, context)

@login_required
@usuario_activo
def create_other_information(request, customer_code):
    template_name = 'FinancialInformation/create_other_information.html'
    customer_id = get_object_or_404(Customer, customer_code=str(customer_code))
    form = OtherSourcesOfIncomeForms
    context = {
        'form':form,
        'customer_code':customer_code,
        'permisos':recorrer_los_permisos_usuario(request)
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
            return redirect('customer:detail',customer_code)
        else:
            return render(request, template_name, context)
        
    return render(request, template_name, context)


@login_required
@usuario_activo
def update_working_information(request, id, customer_code):
    customer_id = get_object_or_404(Customer, customer_code=customer_code)
    working = get_object_or_404(WorkingInformation, id = id)
    template_name = 'FinancialInformation/update_working_information.html'

    if request.method == 'POST':
        form = WorkingInformationForms(request.POST)
        if form.is_valid():
            #working.customer_id = customer_id
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
            return redirect('customers:detail', customer_code)
        else:
            return render(request, template_name, context)
    else:
        initial_data = {
            'position':working.position,
            'company_name':working.company_name,
            'start_date':working.start_date,            
            'salary':working.salary,
            'working_hours':working.working_hours,
            'phone_number':working.phone_number,
            'source_of_income':working.source_of_income,
            'income_detail':working.income_detail,
            'employment_status':working.employment_status ,
            'description':working.description,
        }
        form = WorkingInformationForms(instance=working)
        context = {
            'form':form,
            'working_id':id,
            'customer_code':customer_code,
            'permisos':recorrer_los_permisos_usuario(request)
        }
        return render(request, template_name, context)

@login_required
@usuario_activo
def update_other_information(request, id, customer_code):
    customer = get_object_or_404(Customer, customer_code=customer_code)
    other = get_object_or_404(OtherSourcesOfIncome, id=id)
    template_name = 'FinancialInformation/update_other_information.html'

    if request.method == 'POST':
        form = OtherSourcesOfIncomeForms(request.POST, instance=other)
        if form.is_valid():
            other.customer_id = customer
            other.nit = form.cleaned_data.get('nit')
            other.phone_number = form.cleaned_data.get('phone_number')
            other.salary = form.cleaned_data.get('salary')
            other.source_of_income = form.cleaned_data.get('source_of_income')
            other.save()
            return redirect('customers:detail', customer_code=customer_code)
    else:
        form = OtherSourcesOfIncomeForms(instance=other)

    context = {
        'form': form,
        'other_id': other.id,
        'customer_code': customer_code,
        'permisos':recorrer_los_permisos_usuario(request)
    }
    return render(request, template_name, context)

@login_required
@usuario_activo
def create_references_customer(request, customer_code):
    customer_id = get_object_or_404(Customer, customer_code = customer_code)
    template_name = 'FinancialInformation/create_references.html'

    if request.method == 'POST':
        form = ReferenceForms(request.POST)
        if form.is_valid():
            referencia = Reference()
            referencia.full_name = form.cleaned_data.get('full_name')
            referencia.phone_number = form.cleaned_data.get('phone_number')
            referencia.reference_type = form.cleaned_data.get('reference_type')
            referencia.save()

            return redirect('customers:detail',customer_code)
    form = ReferenceForms
    context = {
        'form':form,
        'customer_code':customer_code,
        'permisos':recorrer_los_permisos_usuario(request)
    }

    return render(request, template_name, context)

@login_required
@usuario_activo
def update_references_customer(request, id,customer_code):
    customer_id = get_object_or_404(Customer, customer_code = customer_code)
    template_name = 'FinancialInformation/update_references.html'
    referencia = get_object_or_404(Reference, id=id)
    if request.method == 'POST':
        form = ReferenceForms(request.POST)
        if form.is_valid():
            
            referencia.full_name = form.cleaned_data.get('full_name')
            referencia.phone_number = form.cleaned_data.get('phone_number')
            referencia.reference_type = form.cleaned_data.get('reference_type')
            referencia.save()

            return redirect('customers:detail',customer_code)
    else:
        initial_data = {
            'full_name':referencia.full_name,
            'phone_number':referencia.phone_number,
            'reference_type':referencia.reference_type
        }
        form = ReferenceForms(initial=initial_data)

        context = {
            'form':form,
            'references_id':id,
            'customer_code':customer_code,
            'permisos':recorrer_los_permisos_usuario(request)
        }

        return render(request, template_name, context)