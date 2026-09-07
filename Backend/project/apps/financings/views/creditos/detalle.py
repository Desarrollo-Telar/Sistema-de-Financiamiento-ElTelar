from django.shortcuts import render, get_object_or_404, redirect

# Models
from apps.financings.models import Credit, PaymentPlan
from apps.customers.models import CreditCounselor


# FUNC
from apps.financings.func.obtener_cuota_credito import cuota

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import permiso_requerido

# Manejo de mensajes
from django.contrib import messages


# SCRIPTS 
from .recoleccion_info_detalle import informacion_detalle

### ------------ DETALLE -------------- ###
from apps.financings.tareas_ansicronicas import generar_todas_las_cuotas_credito



def cuota_siguiente(credito):
    # 1. Obtenemos la cuota actual usando tu lógica existente
    cuota_actual = cuota(credito)
    
    if not cuota_actual:
        return None

    # 2. Buscamos la cuota que sigue en el plan de pagos
    # Asumiendo que el orden lógico es por fecha de inicio o por ID
    proxima = PaymentPlan.objects.filter(
        credit_id__id=credito.id,
        start_date__gt=cuota_actual.start_date # Que empiece después de la actual
    ).order_by('start_date').first()
    
    return proxima

@login_required
@permiso_requerido('puede_ver_detalle_credito')
def detail_credit(request,id):
    
    template_name = 'financings/credit/detail.html' # TEMPLATE
    credito= Credit.objects.filter(id=id).first() # DETALLE DEL CREDITO

    if credito is None:
        return redirect('http_404')

    asesor_autenticado = CreditCounselor.objects.filter(usuario=request.user).first()

    if asesor_autenticado is not None and request.user.rol.role_name == 'Asesor de Crédito':
        credito = Credit.objects.filter(id=id, asesor_de_credito=asesor_autenticado).first()

        if credito is None:
            messages.error(request, 'Usted no tiene permitido visualizar el credito de este cliente.')
            return redirect('financings:list_credit')
        
    generar_todas_las_cuotas_credito(credito.codigo_credito)
    
    
    
    siguiente_pago = cuota(credito)

    
    
    if siguiente_pago is not None:
        saldo_actual = siguiente_pago.saldo_pendiente + siguiente_pago.mora + siguiente_pago.interest

        credito.saldo_actual = saldo_actual
        credito.save()

    request.session['cuota_id'] = siguiente_pago.id if siguiente_pago else None
    
    
   
   
    context = informacion_detalle(request,credito, saldo_actual, siguiente_pago)

    return render(request, template_name,context)
