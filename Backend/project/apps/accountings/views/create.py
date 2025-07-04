from django.shortcuts import render, redirect

# Manejo de mensajes
from django.contrib import messages

# Models
from apps.accountings.models import Creditor, Insurance
from apps.financings.models import Payment


# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import usuario_activo, permiso_requerido


# Formularios
from apps.accountings.forms import AcreedorForm, SeguroForm, IngresoForm, EgresoForm

# MENSAJES
from django.contrib import messages

# Scripts
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario


@login_required
@permiso_requerido('puede_crear_acreedor')
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
            acreedor.estados_fechas = True
            
            acreedor.save() 
            
            if numero_referencia is not None:
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
                
            messages.success(request, 'Acreedor Creado con Exito')
            return redirect('contable:acreedores')

    form = AcreedorForm
    context = {
        'form':form,
        
        'title':'Creacion de un nuevo Acreedor. ',
        'permisos':recorrer_los_permisos_usuario(request),
    } 

    return render(request, template_name, context)

@login_required
@permiso_requerido('puede_crear_seguro')
def add_seguro(request):     
    template_name = 'contable/create.html'
    if request.method == 'POST':
        form = SeguroForm(request.POST, request.FILES)

        if form.is_valid():
            numero_referencia = None
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
            acreedor.estados_fechas = True
            
            acreedor.save() 
            
                
            messages.success(request, 'Seguro Creado con Exito')
            return redirect('contable:seguros')

    form = SeguroForm
    context = {
        'form':form,
        
        'title':'Creacion de un Seguro Nuevo.',
        'permisos':recorrer_los_permisos_usuario(request),
    } 

    return render(request, template_name, context)

@login_required
@permiso_requerido('puede_crear_ingresos')
def add_ingreso(request):     
    template_name = 'contable/create.html'
    if request.method == 'POST':
        form = IngresoForm(request.POST, request.FILES)

        if form.is_valid():
            

            inicio = form.cleaned_data.get('fecha')
            numero_referencia = form.cleaned_data.get('numero_referencia')
            boleta = form.cleaned_data.get('boleta')
            monto = form.cleaned_data.get('monto')
            descripcion = form.cleaned_data.get('descripcion')
            form.save()
            
            
            boleta = Payment(
                
                fecha_emision=inicio,
                numero_referencia=numero_referencia,
                tipo_pago='INGRESO',
                boleta = boleta,
                monto=monto,
                descripcion=descripcion
                )  
            boleta.save()
               
            messages.success(request, 'Ingreso Creado con Exito')
            return redirect('contable:ingresos')

    form = IngresoForm
    context = {
        'form':form,
        
        'title':'Creacion de un Ingreso Nuevo. ',
        'permisos':recorrer_los_permisos_usuario(request),
    } 

    return render(request, template_name, context)

@login_required
@permiso_requerido('puede_crear_egresos')
def add_egresos(request):     
    template_name = 'contable/create.html'
    if request.method == 'POST':
        form = EgresoForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            

            inicio = form.cleaned_data.get('fecha')
            numero_referencia = form.cleaned_data.get('numero_referencia')
            boleta = form.cleaned_data.get('boleta')
            monto = form.cleaned_data.get('monto')
            descripcion = form.cleaned_data.get('observaciones')
            codigo_egreso = form.cleaned_data.get('codigo_egreso')
            

            form.save()
            
            if codigo_egreso != 'ACREEDORES' or codigo_egreso !='PAGO DE SEGUROS':
            
                boletas = Payment(
                    fecha_emision=inicio,
                    numero_referencia=numero_referencia,
                    tipo_pago='EGRESO', 
                    boleta = boleta,
                    monto=monto,
                    descripcion=descripcion
                    )  
                boletas.save()
             
            messages.success(request, 'Egreso Creado con Exito')
            return redirect('contable:egresos')

    form = EgresoForm
    context = {
        'form':form,
        'title':'Creacion de un Egreso Nuevo. ',
        'permisos':recorrer_los_permisos_usuario(request),
    } 

    return render(request, template_name, context)