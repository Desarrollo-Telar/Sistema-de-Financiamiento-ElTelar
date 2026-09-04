from django.shortcuts import render, get_object_or_404, redirect

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import usuario_activo, permiso_requerido
from django.utils.decorators import method_decorator

# SCRIPTS
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario

# Models
from apps.financings.models import Payment

@login_required
@usuario_activo
def update_payment(request, id):
    pago = get_object_or_404(Payment, id=id)
    template_name = 'financings/payment/create.html'
    context = {
        'title':'EL TELAR - PAGO'
    }
    return render(request, template_name, context)

@login_required
@permiso_requerido('puede_revertir_pago')
def reversion_pago(request, id):
    pago = get_object_or_404(Payment, id=id)
    if request.method == 'POST':
        
        pago.delete()
        return redirect('list_payment') 

    template_name = 'financings/payment/reversion_pago.html'
    context = {
        'title': 'EL TELAR - REVERSIÓN DE PAGO',
        'pago': pago,
        'permisos':recorrer_los_permisos_usuario(request),
    }
    return render(request, template_name, context)