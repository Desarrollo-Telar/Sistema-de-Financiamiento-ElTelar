from django.shortcuts import render, get_object_or_404, redirect

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import usuario_activo, permiso_requerido
from django.utils.decorators import method_decorator

# SCRIPTS
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario
from .obtener_credito import obtencion_credito_en_pago

# Models
from apps.financings.models import Payment
from django.db import transaction

@login_required
@usuario_activo
def update_payment(request, id):
    pago = get_object_or_404(Payment, id=id)
    template_name = 'financings/payment/create.html'
    context = {
        'title':'EL TELAR - PAGO'
    }
    return render(request, template_name, context)


@permiso_requerido('puede_revertir_pago')
@transaction.atomic  
def reversion_pago(request, id):
    pago = get_object_or_404(Payment, id=id)
    
    if request.method == 'POST':
        # 1. Revertimos los saldos de la entidad vinculada
        obtencion_credito_en_pago(pago)
        
        # 2. Eliminamos el pago de forma segura dentro de la transacción
        pago.delete()
        
        return redirect('financings:list_payment') 

    template_name = 'financings/payment/reversion_pago.html'
    context = {
        'title': 'EL TELAR - REVERSIÓN DE PAGO',
        'pago': pago,
        'permisos': recorrer_los_permisos_usuario(request),
    }
    return render(request, template_name, context)