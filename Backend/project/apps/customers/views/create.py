from django.shortcuts import render, redirect

# Models
from apps.customers.models import Customer, ImmigrationStatus, CreditCounselor
from apps.subsidiaries.models import Subsidiary

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import permiso_requerido


# Formularios
from apps.customers.forms import CustomerForm
from apps.addresses.forms import AddressForms

# MENSAJES
from django.contrib import messages

# SCRIPTS
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario

# Import
import json
from django.http import JsonResponse
import uuid

# HISTORIAL Y BITACORA
from apps.actividades.utils import log_user_action, log_system_event
from scripts.conversion_datos import model_to_dict, cambios_realizados



# ----- CREANDO USUARIOS NUEVOS ----- #
@login_required
@permiso_requerido('puede_crear_informacion_personal_cliente')
def add_customer(request):     
    ime = ImmigrationStatus.objects.all()    
    template_name = 'customer/add.html'    
    context = {
        'title': 'Creacion de Clientes',        
        'immigration_status':ime,
        'user_id':request.user.id,
        'accion':'Agregar',
        'permisos':recorrer_los_permisos_usuario(request),
    }
    return render(request, template_name, context)

@login_required
@permiso_requerido('puede_crear_informacion_personal_cliente')
def create_customer(request):
    template_name = 'customer/created.html'
    sucursal = request.session['sucursal_id']

    asesor_autenticado = CreditCounselor.objects.filter(usuario=request.user).first()

    if request.method == 'POST':
        form_cliente = CustomerForm(request.POST)
        form_direccion = AddressForms(request.POST)

        if form_cliente.is_valid() and form_direccion.is_valid():
            cliente = form_cliente.save(commit=False)

            if asesor_autenticado is not None and request.user.rol.role_name == 'Asesor de Crédito':
                cliente.new_asesor_credito = asesor_autenticado

            cliente.user_id = request.user
            cliente.sucursal = Subsidiary.objects.get(id=sucursal)
            cliente.completado = False
            cliente.save()

            direccion = form_direccion.save(commit=False)
            direccion.customer_id = cliente
            direccion.type_address = 'Dirección Personal'
            direccion.save()

            log_user_action(
                request.user, 'Registro de Cliente',
                f'El usuario {request.user} ha registro al cliente {cliente.first_name} {cliente.last_name}',
                request,'CLIENTES',model_to_dict(cliente)
            )
            return redirect('financial_information:seleccionar',  cliente.customer_code)
            

    else:
        form_cliente = CustomerForm()
        form_direccion = AddressForms()
        form_direccion.fields.pop('type_address')

        

    

    if asesor_autenticado is not None and request.user.rol.role_name == 'Asesor de Crédito':
        form_cliente.fields.pop('new_asesor_credito')

    context = {
        'title': 'Creación de Clientes |',
        'permisos':recorrer_los_permisos_usuario(request),
        'form_cliente':form_cliente,
        'form_direccion':form_direccion,
    }
    return render (request, template_name, context)