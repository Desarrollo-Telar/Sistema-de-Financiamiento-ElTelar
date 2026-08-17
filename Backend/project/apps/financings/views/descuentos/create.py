from django.shortcuts import render, get_object_or_404, redirect

# Models
from apps.financings.models import Credit, PaymentPlan, Descuento

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import usuario_activo, permiso_requerido
from django.utils.decorators import method_decorator

# Scripts
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario

# FORMULARIO
from apps.financings.forms import PaymentPlanForms, BoletaForm

# Manejo de mensajes
from django.contrib import messages


@login_required
@permiso_requerido('puede_aplicar_descuento_cuota')
def aplicacion_descuento_view(request, credit_id, cuota_id):
    template_name = 'financings/descuento/aplicar_descuento.html'

    credito = get_object_or_404(Credit, id=credit_id)
    cuota = get_object_or_404(PaymentPlan, id=cuota_id)
    sucursal = request.session.get('sucursal_id', 1)
    
    # Formateo seguro para inputs numéricos HTML
    interes = str(getattr(cuota, 'interest', 0.00) or 0.00)
    mora = str(getattr(cuota, 'mora', 0.00) or 0.00)
    saldo = str(getattr(cuota, 'saldo_pendiente', 0.00) or 0.00)

    context = {
        'credito': credito,
        'cuota': cuota,
        'sucursal': sucursal,
        'usuario_descuento': request.user,
        'interes_por_cobrar': interes,
        'mora_por_cobrar': mora,   
        'saldo_capital_por_cobrar': saldo,
        'permisos': recorrer_los_permisos_usuario(request),
    }
    return render(request, template_name, context)
