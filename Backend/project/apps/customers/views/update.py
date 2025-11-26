from django.shortcuts import render, get_object_or_404, redirect

# Models
from apps.customers.models import Customer, CreditCounselor
from apps.addresses.models import Municiopio, Departamento

# LIBRERIAS PARA CRUD
from django.views.generic.list import ListView
from django.db.models import Q

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import permiso_requerido
# Paginacion
from project.pagination import paginacion
from datetime import datetime
# Formularios
from apps.customers.forms import CustomerForm

# MENSAJES
from django.contrib import messages

# SCRIPTS
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario


# ----- EDITAR INFORMACION PERSONAL DE UN CLIENTE ----- #

@login_required
@permiso_requerido('puede_editar_informacion_personal_cliente')
def update_customer(request, customer_code):
    template_name = 'customer/update.html'
    customer = get_object_or_404(Customer, customer_code=str(customer_code))
    municipio = Municiopio.objects.filter(
        nombre=customer.lugar_emision_tipo_identificacion_municipio
    ).first()

    departamento = Departamento.objects.filter(
        nombre=customer.lugar_emision_tipo_identificacion_departamento
    ).first()
        
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customers:detail', customer_code=customer.customer_code)
    else:

        form = CustomerForm(instance=customer)

        print(f'{municipio} / {customer.lugar_emision_tipo_identificacion_municipio}\n {departamento} / {customer.lugar_emision_tipo_identificacion_departamento}')

        # ASIGNAR VALORES INICIALES AL FORMULARIO
        if municipio:
            form.initial['lugar_emision_tipo_identificacion_municipio'] = municipio.id

        if departamento:
            form.initial['lugar_emision_tipo_identificacion_departamento'] = departamento.id
            

        fecha = str(customer.date_birth)
        form.initial['date_birth'] = datetime.strptime(fecha, "%Y-%m-%d").strftime("%Y-%m-%d")
        fecha = str(customer.fehca_vencimiento_de_tipo_identificacion)
        form.initial['fehca_vencimiento_de_tipo_identificacion']= datetime.strptime(fecha, "%Y-%m-%d").strftime("%Y-%m-%d")




    context = {
        'form': form,
        'title': f'Actualizacion de Informacion para el cliente. {customer.customer_code}',
        'customer_code': customer.customer_code,
        'permisos':recorrer_los_permisos_usuario(request)
    }
    return render(request, template_name, context)