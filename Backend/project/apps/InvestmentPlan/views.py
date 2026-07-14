from django.shortcuts import render, get_object_or_404, redirect

# FORMULARIO
from .forms import InvestmentPlanForms
# FORMATO
from apps.financings.formato import formatear_numero

# MODELOS
from apps.customers.models import Customer, CreditCounselor
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

    asesor_autenticado = CreditCounselor.objects.filter(usuario=request.user).first()
    es_asesor = False

    if asesor_autenticado is not None and request.user.rol.role_name == 'Asesor de Crédito':
        es_asesor = True

   
    
    context = {
        'customer_id':customer_id,
        'sucursal': sucursal,
        'customer_code':customer_code,
        'es_asesor':es_asesor,
        'permisos':recorrer_los_permisos_usuario(request),
        'disponibilidad_efectiva': formatear_numero(customer_id.disponibilidad_efectiva()),

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
def update_plan_financiamiento(request, id, customer_code):
    template_name = 'InvestmentPlan/create.html'
    get_plan = get_object_or_404(InvestmentPlan, id=id)
    customer_id = get_object_or_404(Customer, customer_code=customer_code)
    sucursal = Subsidiary.objects.get(id=request.session['sucursal_id'])
    asesor_autenticado = CreditCounselor.objects.filter(usuario=request.user).first()
    es_asesor = False

    if asesor_autenticado is not None and request.user.rol.role_name == 'Asesor de Crédito':
        es_asesor = True

    context = {
        'plan': get_plan,  # <-- AGREGADO: Enviamos el objeto con los datos existentes
        'customer_id': customer_id,
        'cliente': customer_id, # Asegura compatibilidad si usabas cliente.id en el hidden input
        'sucursal': sucursal,
        'customer_code': customer_code,
        'es_asesor':es_asesor,
        'permisos': recorrer_los_permisos_usuario(request),
        'disponibilidad_efectiva': formatear_numero(customer_id.disponibilidad_efectiva()),
    }
    return render(request, template_name, context)