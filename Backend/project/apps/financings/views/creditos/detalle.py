from django.shortcuts import render, get_object_or_404, redirect

# Models
from apps.financings.models import Credit, Guarantees, Disbursement,DetailsGuarantees,  PaymentPlan, AccountStatement
from apps.customers.models import CreditCounselor
from django.db.models import Q
from apps.actividades.models import VotacionCredito



# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import permiso_requerido

# Manejo de mensajes
from django.contrib import messages

# Tiempo
from datetime import datetime,timedelta


# SCRIPTS 
from .recoleccion_info_detalle import informacion_detalle

### ------------ DETALLE -------------- ###
from apps.financings.tareas_ansicronicas import generar_todas_las_cuotas_credito


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
    
    
    dia = datetime.now().date()
    dia_mas_uno = dia + timedelta(days=1)
    siguiente_pago = None

    if credito.is_paid_off:
        siguiente_pago = PaymentPlan.objects.filter(
        credit_id__id=credito.id).order_by('-id').first()
        print(siguiente_pago)
    else:
        siguiente_pago = PaymentPlan.objects.filter(
            credit_id__id=credito.id,
            start_date__lte=dia,
            fecha_limite__gte=dia_mas_uno
        ).first()

    print(siguiente_pago)
    if siguiente_pago is None:
        siguiente_pago = PaymentPlan.objects.filter(
        credit_id__id=credito.id).order_by('-id').first()
    
    if siguiente_pago is not None:
        saldo_actual = siguiente_pago.saldo_pendiente + siguiente_pago.mora + siguiente_pago.interest

        credito.saldo_actual = saldo_actual
        credito.save()

    print(siguiente_pago)
    
   
   
    context = informacion_detalle(request,credito, saldo_actual, siguiente_pago)

    return render(request, template_name,context)
