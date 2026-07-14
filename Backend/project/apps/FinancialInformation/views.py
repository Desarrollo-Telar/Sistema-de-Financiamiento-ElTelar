from django.shortcuts import render, get_object_or_404, redirect

# FORMULARIO
from .forms import WorkingInformationForms,OtherSourcesOfIncomeForms,ReferenceForms
from apps.addresses.forms import AddressForms

# MODELOS
from apps.customers.models import Customer
from apps.InvestmentPlan.models import InvestmentPlan
from apps.addresses.models import Address
from .models import WorkingInformation, OtherSourcesOfIncome, Reference

# HISTORIAL Y BITACORA
from apps.actividades.utils import log_user_action, log_system_event
from scripts.conversion_datos import model_to_dict, cambios_realizados

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import usuario_activo
from django.utils.decorators import method_decorator

# Scripts
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario


# Create your views here.
# Import
import json
from django.http import JsonResponse

@login_required
@usuario_activo
def seleccionar(request, customer_code):
    template_name = 'FinancialInformation/seleccionar.html'

    context = {
        'customer_code':customer_code,
        'permisos':recorrer_los_permisos_usuario(request)
    }

    return render(request, template_name, context)

@login_required
@usuario_activo
def delete_other_information(request,id, customer_code):
    other = get_object_or_404(OtherSourcesOfIncome, id = id)
    log_user_action(
        request.user
    )
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
    sucursal = request.session['sucursal_id']

    context = {
        
        'permisos':recorrer_los_permisos_usuario(request),
        'customer_code':customer_code,
        'subsidiary': sucursal,
        'cliente': customer_id.id
    }

    return render(request, template_name, context)

@login_required
@usuario_activo
def create_other_information(request, customer_code):
    template_name = 'FinancialInformation/create_working_information.html'
    customer_id = get_object_or_404(Customer, customer_code=str(customer_code))
    sucursal = request.session['sucursal_id']

    context = {
        
        'permisos':recorrer_los_permisos_usuario(request),
        'customer_code':customer_code,
        'subsidiary': sucursal,
        'cliente': customer_id
    }

    return render(request, template_name, context)

from django.views.decorators.csrf import ensure_csrf_cookie 

@login_required
@usuario_activo
@ensure_csrf_cookie  
def create_gastos_cliente(request, customer_code):
    template_name = 'FinancialInformation/gastos_cliente.html'
    customer_id = get_object_or_404(Customer, customer_code=str(customer_code))
    sucursal = request.session.get('sucursal_id') # Es más seguro usar .get() por si no existe la sesión

    context = {
        'permisos': recorrer_los_permisos_usuario(request),
        'customer_code': customer_code,
        'subsidiary': sucursal,
        'cliente': customer_id
    }

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


def delete_referencias(customer_id):
    referencias = Reference.objects.filter(customer_id = customer_id)

    if referencias is not None:
        for referencia in referencias:
            referencia.delete()

@login_required
@usuario_activo
def create_references_customer(request, customer_code):
    customer_id = get_object_or_404(Customer, customer_code=customer_code)
    template_name = 'FinancialInformation/create_references.html'

    delete_referencias(customer_id)

    if request.method == 'POST':
        form = ReferenceForms(request.POST, prefix='form1')
        form_2 = ReferenceForms(request.POST, prefix='form2')
        form_3 = ReferenceForms(request.POST, prefix='form3')
        form_4 = ReferenceForms(request.POST, prefix='form4')

        validacion = form.is_valid() and form_2.is_valid() and form_3.is_valid() and form_4.is_valid()

        if validacion:
            referencia1 = form.save(commit=False)
            referencia1.customer_id = customer_id
            referencia1.reference_type = 'Personales'
            referencia1.save()

            referencia2 = form_2.save(commit=False)
            referencia2.customer_id = customer_id
            referencia2.reference_type = 'Personales'
            referencia2.save()

            referencia3 = form_3.save(commit=False)
            referencia3.customer_id = customer_id
            referencia3.reference_type = 'Laborales'
            referencia3.save()

            referencia4 = form_4.save(commit=False)
            referencia4.customer_id = customer_id
            referencia4.reference_type = 'Laborales'
            referencia4.save()

           
          
                
                

            return redirect('check_list_customer', customer_code)
    else:
        form = ReferenceForms(prefix='form1')
        form_2 = ReferenceForms(prefix='form2')
        form_3 = ReferenceForms(prefix='form3')
        form_4 = ReferenceForms(prefix='form4')

    context = {
        'form': form,
        'form_2': form_2,
        'form_3': form_3,
        'form_4': form_4,
        'customer_code': customer_code,
        'permisos': recorrer_los_permisos_usuario(request)
    }

    return render(request, template_name, context)

@login_required
@usuario_activo
def update_references_customer(request, id,customer_code):
    customer_id = get_object_or_404(Customer, customer_code = customer_code)
    template_name = 'FinancialInformation/update_references.html'
    referencia = get_object_or_404(Reference, id=id)

    if request.method == 'POST':
        form = ReferenceForms(request.POST, instance=referencia)

        if form.is_valid():
            refe = form.save(commit=False)
            refe.customer_id = customer_id
            refe.save()
            return redirect('customers:detail',customer_code)

    
    form = ReferenceForms(instance=referencia)

    context = {
        'form':form,
        'customer_code':customer_code,
        'permisos':recorrer_los_permisos_usuario(request)

    }

    return render(request, template_name, context)

    