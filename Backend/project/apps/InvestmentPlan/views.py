from django.shortcuts import render, get_object_or_404, redirect

# FORMULARIO
from .forms import InvestmentPlanForms

# MODELOS
from apps.customers.models import Customer
from .models import InvestmentPlan

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
def create_plan_financiamiento(request, customer_code):
    customer_id = get_object_or_404(Customer, customer_code=customer_code)
    template_name = ''
    if request.method == 'POST':
        form = InvestmentPlanForms(request.POST)
        if form.is_valid():
            plan = InvestmentPlan()
            plan.customer_id = customer_id
            plan.type_of_product_or_service = form.cleaned_data.get('type_of_product_or_service')
            plan.total_value_of_the_product_or_service = form.cleaned_data.get('total_value_of_the_product_or_service')
            plan.investment_plan_description= form.cleaned_data.get('investment_plan_description')
            plan.initial_amount = form.cleaned_data.get('initial_amount')
            plan.monthly_amount= form.cleaned_data.get('monthly_amount')
            plan.transfers_or_transfer_of_funds = form.cleaned_data.get('transfers_or_transfer_of_funds')
            plan.type_of_transfers_or_transfer_of_funds = form.cleaned_data.get('type_of_transfers_or_transfer_of_funds')
            plan.save()
            return redirect('customers:detail',customer_code)
    form = InvestmentPlanForms
    context = {
        'form':form
    }
    return render(request, template_name, context)

@login_required
@usuario_activo
def delete_plan_financiamiento(request, id,customer_code):
    plan = get_object_or_404(InvestmentPlan, id = id)
    plan.delete()
    return redirect('customers:detail',customer_code)


@login_required
@usuario_activo
def update_plan_financiamiento(request,id,customer_code):
    template_name = ''
    plan = get_object_or_404(InvestmentPlan, id=id)
    customer_id = get_object_or_404(Customer, customer_code = customer_code)
    if request.method == 'POST':
        form = InvestmentPlanForms(request.POST)
        if form.is_valid():
            plan.customer_id = customer_id
            plan.type_of_product_or_service = form.cleaned_data.get('type_of_product_or_service')
            plan.total_value_of_the_product_or_service = form.cleaned_data.get('total_value_of_the_product_or_service')
            plan.investment_plan_description= form.cleaned_data.get('investment_plan_description')
            plan.initial_amount = form.cleaned_data.get('initial_amount')
            plan.monthly_amount= form.cleaned_data.get('monthly_amount')
            plan.transfers_or_transfer_of_funds = form.cleaned_data.get('transfers_or_transfer_of_funds')
            plan.type_of_transfers_or_transfer_of_funds = form.cleaned_data.get('type_of_transfers_or_transfer_of_funds')
            plan.save()
            return redirect('customers:detail',customer_code)
    else:
        initial_data = {
            'type_of_product_or_service':plan.type_of_product_or_service ,
            'total_value_of_the_product_or_service':plan.type_of_product_or_service,
            'investment_plan_description': plan.investment_plan_description,
            'initial_amount':plan.initial_amount,
            'monthly_amount':plan.monthly_amount,
            'transfers_or_transfer_of_funds':plan.transfers_or_transfer_of_funds,
            'type_of_transfers_or_transfer_of_funds':plan.type_of_transfers_or_transfer_of_funds,

        }
        form = InvestmentPlanForms(initial=initial_data)
        context = {
            'form':form
        }
        return render(request, template_name, context)