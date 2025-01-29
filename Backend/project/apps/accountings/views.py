from django.shortcuts import render, get_object_or_404, redirect

# Manejo de mensajes
from django.contrib import messages

# Models
from .models import Creditor, Insurance, Insurance, Egress
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
from .forms import AcreedorForm, SeguroForm

# MENSAJES
from django.contrib import messages



# Create your views here.
@login_required
@usuario_activo
def list_acreedores(request):
    template_name = 'contable/acreedores/list.html'
    acreedores_list = Creditor.objects.all().order_by('-id')
    page_obj = paginacion(request, acreedores_list)
    context = {
        'title':'EL TELAR',
        'page_obj':page_obj,
        'acreedores_list':page_obj,
        'count':acreedores_list.count(),
        
    }
        
    return render(request, template_name, context)

@login_required
@usuario_activo
def add_acreedor(request):     
    template_name = 'contable/create.html'
    if request.method == 'POST':
        form = AcreedorForm(request.POST, request.FILES)

        if form.is_valid():
            acreedor = Creditor()
            inicio = form.cleaned_data.get('fecha_inicio')
            numero_referencia = form.cleaned_data.get('numero_referencia')
            boleta = form.cleaned_data.get('boleta')
            monto = form.cleaned_data.get('monto')
            descripcion = form.cleaned_data.get('observaciones')
            tasa = form.cleaned_data.get('tasa')
            
            if tasa > 0:
                tasa = tasa /100

            acreedor.nombre_acreedor = form.cleaned_data.get('nombre_acreedor')
            acreedor.fecha_inicio = inicio
            acreedor.monto = monto
            acreedor.tasa = tasa
            acreedor.plazo = form.cleaned_data.get('plazo')
            acreedor.numero_referencia = numero_referencia
            acreedor.observaciones = descripcion
            acreedor.boleta = boleta
            
            acreedor.save() 
            print(acreedor.codigo_acreedor)
            """
            boleta = Payment(
                acreedor=acreedor, 
                fecha_emision=inicio,
                numero_referencia=numero_referencia,
                tipo_pago='ACREEDOR',
                boleta = boleta,
                monto=monto,
                descripcion=descripcion
                )  
            boleta.save()
            """    
            messages.success(request, 'Acreedor Creado con Exito')
            return redirect('contable:acreedores')

    form = AcreedorForm
    context = {
        'form':form,
        
        'title':'ELTELAR ',
    } 

    return render(request, template_name, context)

@login_required
@usuario_activo
def add_seguro(request):     
    template_name = 'contable/create.html'
    if request.method == 'POST':
        form = SeguroForm(request.POST, request.FILES)

        if form.is_valid():
            acreedor = Insurance()
            inicio = form.cleaned_data.get('fecha_inicio')
            numero_referencia = form.cleaned_data.get('numero_referencia')
            boleta = form.cleaned_data.get('boleta')
            monto = form.cleaned_data.get('monto')
            descripcion = form.cleaned_data.get('observaciones')
            tasa = form.cleaned_data.get('tasa')
            
            if tasa > 0:
                tasa = tasa /100

            acreedor.nombre_acreedor = form.cleaned_data.get('nombre_acreedor')
            acreedor.fecha_inicio = inicio
            acreedor.monto = monto
            acreedor.tasa = tasa
            acreedor.plazo = form.cleaned_data.get('plazo')
            acreedor.numero_referencia = numero_referencia
            acreedor.observaciones = descripcion
            acreedor.boleta = boleta
            
            acreedor.save() 
            print(acreedor.codigo_acreedor)
            """
            boleta = Payment(
                acreedor=acreedor, 
                fecha_emision=inicio,
                numero_referencia=numero_referencia,
                tipo_pago='ACREEDOR',
                boleta = boleta,
                monto=monto,
                descripcion=descripcion
                )  
            boleta.save()
            """    
            messages.success(request, 'Acreedor Creado con Exito')
            return redirect('contable:acreedores')

    form = AcreedorForm
    context = {
        'form':form,
        
        'title':'ELTELAR ',
    } 

    return render(request, template_name, context)