from django.shortcuts import render, get_object_or_404, redirect

# Models
from apps.financings.models import Payment, PaymentPlan, AccountStatement, Recibo
from apps.financings.models import Invoice, Credit

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import usuario_activo, permiso_requerido
from django.utils.decorators import method_decorator

# Scripts
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario
from scripts.INFILE.fact import guardar_xml_recibo

# FORMULARIO
from apps.financings.forms import PaymentPlanForms, BoletaForm

# Manejo de mensajes
from django.contrib import messages

# Create your views here.
@login_required
def reversion_pago(request, id):
    try:
        pago = get_object_or_404(Payment, id=id)
            
        recibo = Recibo.objects.filter(pago=pago).first()

        if recibo is None:
            recibo = Recibo.objects.filter(id=id).first()

            if recibo is None:
                return redirect('http_404')
            
        if request.user.rol.role_name == 'Secretari@':
            if recibo.pago.tipo_pago != 'CREDITO':
                return redirect('http_404')    

    except Payment.DoesNotExist:
        return redirect('http_404')
    
    credito = pago.credit
    
    if credito is None:
        return
    
    pago.delete()
    return redirect('financings:detail_credit', credito.id)