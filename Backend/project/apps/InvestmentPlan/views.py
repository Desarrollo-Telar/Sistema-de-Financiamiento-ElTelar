from django.shortcuts import render, get_object_or_404, redirect

# FORMULARIO
from .forms import InvestmentPlanForms

# MODELOS
from apps.customers.models import Customer
from .models import InvestmentPlan
from apps.FinancialInformation.models import Reference, WorkingInformation, OtherSourcesOfIncome
from apps.subsidiaries.models import Subsidiary
from apps.financings.models import Credit
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
from scripts.conversion_datos import model_to_dict
# Create your views here.

@login_required
@usuario_activo
def create_plan_financiamiento(request, customer_code):
    customer_id = get_object_or_404(Customer, customer_code=customer_code)
    cantidad = Reference.objects.filter(customer_id=customer_id)
    template_name = 'InvestmentPlan/create.html'
    sucursal = Subsidiary.objects.get(id=request.session['sucursal_id'])

   
    
    context = {
        'customer_id':customer_id,
        'sucursal': sucursal,
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
            credito_seleccionado = form.cleaned_data.get('credito_anterior_vigente')
            fiador_seleccionado = form.cleaned_data.get('fiador')

            if credito_seleccionado:
                credito = Credit.objects.get(id=credito_seleccionado)
                plan.credito_anterior_vigente = model_to_dict(credito)
            
            if fiador_seleccionado:
                fiador = Customer.objects.get(id=fiador_seleccionado)
                plan.fiador = model_to_dict(fiador)
                
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