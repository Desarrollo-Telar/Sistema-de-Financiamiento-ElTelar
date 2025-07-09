from django.shortcuts import render, get_object_or_404, redirect

# FORMULARIO
from .forms import InvestmentPlanForms

# MODELOS
from apps.customers.models import Customer
from .models import InvestmentPlan
from apps.FinancialInformation.models import Reference

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

#SCRIPTS
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario

# Create your views here.

@login_required
@usuario_activo
def create_plan_financiamiento(request, customer_code):
    customer_id = get_object_or_404(Customer, customer_code=customer_code)
    cantidad = Reference.objects.filter(customer_id=customer_id)
    plan_inversion = InvestmentPlan.objects.filter(customer_id=customer_id).first()

    template_name = 'InvestmentPlan/create.html'

    if request.method == 'POST':
        form = InvestmentPlanForms(request.POST)

        if plan_inversion is not None:
            form = InvestmentPlanForms(request.POST, instance=plan_inversion)


        if form.is_valid():
            plan = form.save(commit=False)
            plan.customer_id = customer_id
            plan.type_of_product_or_service = 'Local'
            plan.transfers_or_transfer_of_funds = True
            plan.save()

            if cantidad.count() >= 4:
                return redirect('customers:detail',customer_id.customer_code)
            return redirect('financial_information:create_reference_information', customer_id.customer_code)
        
    form = InvestmentPlanForms()
    if plan_inversion is not None:
        form = InvestmentPlanForms(instance=plan_inversion)

    context = {
        'form':form,
        'customer_code':customer_code,
        'permisos':recorrer_los_permisos_usuario(request)
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
    template_name = 'InvestmentPlan/update.html'
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
        form = InvestmentPlanForms(instance=plan)
        context = {
            'form':form,
            'customer_code':customer_code,
            'investment_plan_id':id,
            'permisos':recorrer_los_permisos_usuario(request)
        }
        return render(request, template_name, context)