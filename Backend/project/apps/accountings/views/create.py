from django.shortcuts import render, redirect

# Manejo de mensajes
from django.contrib import messages

# Models
from apps.accountings.models import Creditor, Insurance
from apps.financings.models import Payment
from apps.subsidiaries.models import Subsidiary


# HISTORIAL Y BITACORA
from apps.actividades.utils import log_user_action, log_system_event
from scripts.conversion_datos import model_to_dict, cambios_realizados

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
    sucursal = Subsidiary.objects.get(id=request.session['sucursal_id'] ) 
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
            acreedor.sucursal = sucursal
            
            acreedor.save() 


        

            acreedor_dict = model_to_dict(acreedor)
            pago_dict = None
            
            if numero_referencia is not None:
                boleta = Payment(
                    acreedor=acreedor, 
                    fecha_emision=inicio,
                    numero_referencia=numero_referencia,
                    tipo_pago='ACREEDOR',
                    boleta = boleta,
                    monto=monto,
                    descripcion=descripcion,
                    sucursal=sucursal
                    )  
                boleta.save()

                pago_dict = model_to_dict(boleta)
            
            log_user_action(
                request.user,
                'Registro de Acreedor',
                f'El usuario {request.user} ha registrado un acreedor por un monto de Q{monto}',
                request,
                'CONTABILIDAD',
                model_to_dict(acreedor)
            )
            
                
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
    sucursal = Subsidiary.objects.get(id=request.session['sucursal_id'] )
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
            acreedor.sucursal = sucursal
            acreedor.save() 

            dato_dict = model_to_dict(acreedor)

            log_user_action(
                request.user,
                'Registro de Seguro',
                f'El usuario {request.user} ha registrado un seguro por un monto de Q{monto}',
                request,
                'CONTABILIDAD',
                model_to_dict(acreedor)
            )
                
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
    sucursal = Subsidiary.objects.get(id=request.session['sucursal_id'] )  
    template_name = 'contable/create.html'
    if request.method == 'POST':
        form = IngresoForm(request.POST, request.FILES)

        if form.is_valid():
            ingres = form.save(commit=False)

            inicio = form.cleaned_data.get('fecha')
            numero_referencia = form.cleaned_data.get('numero_referencia')
            boleta = form.cleaned_data.get('boleta')
            monto = form.cleaned_data.get('monto')
            descripcion = form.cleaned_data.get('descripcion')
            ingres.sucursal = sucursal
            ingres.save()
            
            
            boleta = Payment(
                
                fecha_emision=inicio,
                numero_referencia=numero_referencia,
                tipo_pago='INGRESO',
                boleta = boleta,
                monto=monto,
                descripcion=descripcion,
                sucursal= sucursal
                )  
            boleta.save()

            dato_dict = model_to_dict(form.instance)
            
            log_user_action(
                request.user,
                'Registro de Ingreso',
                f'El usuario {request.user} ha registrado un ingreso por un monto de Q{monto}',
                request,
                'CONTABILIDAD',
                model_to_dict(ingres)
            )
               
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
    sucursal = Subsidiary.objects.get(id=request.session['sucursal_id'] ) 
    if request.method == 'POST':
        form = EgresoForm(request.POST, request.FILES)
        
        if form.is_valid():
            egre = form.save(commit=False)
            egre.sucursal = sucursal
            inicio = form.cleaned_data.get('fecha')
            numero_referencia = form.cleaned_data.get('numero_referencia')
            boleta = form.cleaned_data.get('boleta')
            monto = form.cleaned_data.get('monto')
            descripcion = form.cleaned_data.get('observaciones')
            codigo_egreso = form.cleaned_data.get('codigo_egreso')
            

            egre.save()
            
            if codigo_egreso != 'ACREEDORES' or codigo_egreso !='PAGO DE SEGUROS':
            
                boletas = Payment(
                    fecha_emision=inicio,
                    numero_referencia=numero_referencia,
                    tipo_pago='EGRESO', 
                    boleta = boleta,
                    monto=monto,
                    descripcion=descripcion,
                    sucursal = sucursal
                    )  
                boletas.save()

            
            log_user_action(
                request.user,
                'Registro de Egresos',
                f'El usuario {request.user} ha registrado un egreso por un monto de Q{monto}',
                request,
                'CONTABILIDAD',
                model_to_dict(egre)
            )
            messages.success(request, 'Egreso Creado con Exito')
            return redirect('contable:egresos')

    form = EgresoForm
    context = {
        'form':form,
        'title':'Creacion de un Egreso Nuevo. ',
        'permisos':recorrer_los_permisos_usuario(request),
    } 

    return render(request, template_name, context)