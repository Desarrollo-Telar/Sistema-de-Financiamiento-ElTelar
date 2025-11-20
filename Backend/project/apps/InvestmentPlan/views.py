from django.shortcuts import render, get_object_or_404, redirect

# FORMULARIO
from .forms import InvestmentPlanForms

# MODELOS
from apps.customers.models import Customer
from .models import InvestmentPlan
from apps.FinancialInformation.models import Reference, WorkingInformation, OtherSourcesOfIncome
from apps.subsidiaries.models import Subsidiary
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
from dateutil.relativedelta import relativedelta
#SCRIPTS
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario
from project.send_mail import send_email_new_customer
# Create your views here.

@login_required
@usuario_activo
def create_plan_financiamiento(request, customer_code):
    customer_id = get_object_or_404(Customer, customer_code=customer_code)
    cantidad = Reference.objects.filter(customer_id=customer_id)
    template_name = 'InvestmentPlan/create.html'
    sucursal = Subsidiary.objects.get(id=request.session['sucursal_id'])

    if request.method == 'POST':
        form = InvestmentPlanForms(request.POST)

        if form.is_valid():
            plan = form.save(commit=False)
            plan.customer_id = customer_id
            plan.type_of_transfers_or_transfer_of_funds = 'Local'
            plan.transfers_or_transfer_of_funds = True
            plan.sucursal = sucursal
            fecha_inicio = form.cleaned_data.get('fecha_inicio')
            plazo = form.cleaned_data.get('plazo')
            plan.fecha_vencimiento = fecha_inicio + relativedelta(months=plazo)
            plan.save()

            informacion_laboral = WorkingInformation.objects.filter(customer_id=customer_id).exists()

            if not informacion_laboral:
                informacion_laboral = OtherSourcesOfIncome.objects.filter(customer_id=customer_id).exists()

            if cantidad.exists() and informacion_laboral and  not customer_id.completado:
                customer_id.completado = True
                customer_id.save()
                send_email_new_customer(customer_id)

            if cantidad.count() < 4:               
                return redirect('financial_information:create_reference_information', customer_id.customer_code)
            
            return redirect('customers:detail',customer_id.customer_code)
        
    form = InvestmentPlanForms()
    
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
    template_name = 'InvestmentPlan/create.html'

    get_plan = get_object_or_404(InvestmentPlan, id=id)

    customer_id = get_object_or_404(Customer, customer_code = customer_code)
    sucursal = Subsidiary.objects.get(id=request.session['sucursal_id'])

    if request.method == 'POST':
        form = InvestmentPlanForms(request.POST, instance=get_plan)

        if form.is_valid():
            plan = form.save(commit=False)
            plan.customer_id = customer_id
            plan.type_of_transfers_or_transfer_of_funds = 'Local'
            plan.transfers_or_transfer_of_funds = True
            plan.sucursal = sucursal
            plan.save()
            
            return redirect('customers:detail',customer_code)
    else:
        
        form = InvestmentPlanForms(instance=get_plan)
        context = {
            'form':form,
            'customer_code':customer_code,
            'investment_plan_id':id,
            'permisos':recorrer_los_permisos_usuario(request)
        }
        return render(request, template_name, context)