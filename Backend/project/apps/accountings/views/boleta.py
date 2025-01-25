
from django.shortcuts import render, get_object_or_404, redirect

# Manejo de mensajes
from django.contrib import messages

# Models
from apps.accountings.models import Creditor, Income, Insurance, Egress
from apps.financings.models import Payment

# LIBRERIAS PARA CRUD
from django.views.generic import CreateView
from django.views.generic.list import ListView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic.detail import DetailView
from django.db.models import Q

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import usuario_activo, usuario_administrador, usuario_secretaria
from django.utils.decorators import method_decorator

# Paginacion
from project.pagination import paginacion

# Formularios
from apps.accountings.forms import AcreedorForm, SeguroForm, IngresoForm, EgresoForm
from apps.financings.forms import BoletaSeguroForm, BoletaAcreedorForm
# MENSAJES
from django.contrib import messages

@login_required
@usuario_activo
def add_boleta_seguro(request):     
    template_name = 'contable/create.html'
    if request.method == 'POST':
        form = BoletaSeguroForm(request.POST, request.FILES)

        if form.is_valid():
            instance = form.save(commit=False)  
            instance.tipo_pago = 'SEGURO'
            instance.save()
            
            
           
             
            messages.success(request, 'Boleta Registrada')
            return redirect('contable:seguros')

    form = BoletaSeguroForm
    context = {
        'form':form,
        
        'title':'ELTELAR ',
    } 

    return render(request, template_name, context)

@login_required
@usuario_activo
def add_boleta_acreedor(request):     
    template_name = 'contable/create.html'
    if request.method == 'POST':
        form = BoletaAcreedorForm(request.POST, request.FILES)

        if form.is_valid():
            instance = form.save(commit=False)  
            instance.tipo_pago = 'ACREEDOR'
            instance.save()
            
            
           
             
            messages.success(request, 'Egreso Creado con Exito')
            return redirect('contable:acreedores')

    form = BoletaAcreedorForm
    context = {
        'form':form,
        
        'title':'ELTELAR ',
    } 

    return render(request, template_name, context)