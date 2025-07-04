from django.shortcuts import render, redirect

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import permiso_requerido

# Scripts
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario

# Formulario
from apps.financings.forms import BoletaForm

# Modelos
from apps.financings.models import Credit

# MENSAJES
from django.contrib import messages

@login_required
@permiso_requerido('puede_crear_boleta_pago')
def create_payment(request):
    template_name = 'financings/payment/create.html'
    context = {
        'title':'Creacion de Boleta Nueva',
        'permisos':recorrer_los_permisos_usuario(request),
    }
    return render(request, template_name, context)

@login_required
@permiso_requerido('puede_crear_boleta_pago')
def create_payment_credit(request, id):

    # Obtener al credito
    credito = Credit.objects.filter(id=id).first()

    if credito is None:
        return redirect('actividades:cerrar_pestania')
    
    if credito.is_paid_off:
        messages.error(request,'Este Credito Se Encuentra Cancelado')
        return redirect('actividades:cerrar_pestania')

    # Formulario
    form = BoletaForm

    if request.method == 'POST':
        form = BoletaForm(request.POST, request.FILES)

        if form.is_valid():
            documento = form.save(commit=False)
            documento.credit = credito
            documento.tipo_pago = 'CREDITO'
            documento.save()
            messages.success(request, 'Se ha guardado la boleta. ')

            return redirect('financings:detail_credit', credito.id)






    template_name = 'financings/payment/create_boleta_credit.html'

    

    context = {
        'form':form,
        'title':'Creacion de Boleta Nueva',
        'permisos':recorrer_los_permisos_usuario(request),
    }
    return render(request, template_name, context)