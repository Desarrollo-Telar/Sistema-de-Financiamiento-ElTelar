from django.shortcuts import render, get_object_or_404, redirect

# Models
from apps.financings.models import Credit, Guarantees, Disbursement,DetailsGuarantees, Banco, Payment, PaymentPlan, AccountStatement, Recibo
from apps.customers.models import Customer
from apps.financings.models import Invoice


from django.db.models import Q

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import usuario_activo
from django.utils.decorators import method_decorator
# Manejo de mensajes
from django.contrib import messages

from datetime import datetime,timedelta
# Obtener la fecha y hora actual
now = datetime.now()
# CLASES
from apps.financings.clases.paymentplan import PaymentPlan as PlanPagoos
from apps.financings.clases.credit import Credit as Credito

# TAREA ASINCRONICO
from apps.financings.task import cambiar_plan

# LIBRERIAS PARA CRUD
from django.views.generic import CreateView
from django.views.generic.list import ListView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic.detail import DetailView
from django.db.models import Q

def formatear_numero(numero):
    # Convertir el número a un formato con coma para miles y punto para decimales
    return f"{numero:,.2f}".replace(".", "X").replace(".", ",").replace("X", ".")

def planPagosCredito(credito):
    formatted_date = credito.fecha_inicio.strftime('%Y-%m-%d')
    credit = Credito(credito.proposito,credito.monto,credito.plazo,credito.tasa_interes,credito.forma_de_pago,credito.frecuencia_pago,formatted_date,credito.tipo_credito,1,None,credito.fecha_vencimiento)
    plan_pago = PlanPagoos(credit)
    return plan_pago

def total_garantia(list_guarantee):
    total_garantia = 0
    for garantia in list_guarantee:
        total_garantia += garantia.suma_total
    
    return formatear_numero(total_garantia)

def total_desembolso(list_disbursement):
    total_desembolso = 0
    for desembolso in list_disbursement:
        total_desembolso +=desembolso.monto_total_desembolso
    
    return formatear_numero(total_desembolso)

def actualizacion(credito):
    pagos = PaymentPlan.objects.filter(credit_id=credito).order_by('-id').first()
    
    # ACTUALIZAR EL SALDO ACTUAL
    if pagos:
        credito.saldo_pendiente = pagos.saldo_pendiente
        credito.saldo_actual = pagos.saldo_pendiente + pagos.mora + pagos.interest
        credito.save()

def total_desembolsos(estado_cuenta):
    contador = 0
    for estado in estado_cuenta:
        contador+=estado.disbursement_paid
    return formatear_numero(contador)

def total_mora_pagada(estado_cuenta):
    contador = 0
    for estado in estado_cuenta:
        contador+=estado.late_fee_paid
    return formatear_numero(contador)

def total_interes_pagada(estado_cuenta):
    contador = 0
    for estado in estado_cuenta:
        contador+=estado.interest_paid
    return formatear_numero(contador)

def total_capital_pagada(estado_cuenta):
    contador = 0
    for estado in estado_cuenta:
        contador+=estado.capital_paid
    return formatear_numero(contador)

### ------------ DETALLE -------------- ###
@login_required
@usuario_activo
def detail_credit(request,id):
    
    template_name = 'financings/credit/detail.html' # TEMPLATE
    credito= get_object_or_404(Credit,id=id) # DETALLE DEL CREDITO
    cambiar_plan() # CAMBIAR AUTOMATICAMENTE PARA PRUEBAS
    
    customer_list = get_object_or_404(Customer,id= credito.customer_id.id) # LISTAR LA INFORMACION DEL CLIENTE

    # LISTAR LAS GARANTIAS REGISTRADAS
    list_guarantee = Guarantees.objects.filter(credit_id=credito).order_by('-id') 

    list_disbursement = Disbursement.objects.filter(credit_id=credito).order_by('-id') # LISTAR DESEMBOLSOS

    
    siguiente_pago = PaymentPlan.objects.filter(credit_id=credito).order_by('-id').first()
    cuotas_vencidas = PaymentPlan.objects.filter(credit_id=credito, cuota_vencida=True)
    estado_cuenta = AccountStatement.objects.filter(credit=credito)
    actualizacion(credito)
    
    
    
    
    

    # PLAN DE PAGOS
    plan = planPagosCredito(credito).generar_plan()
    
   
   
    context = {
        'title':'ELTELAR - CREDITO',
        'credit_list':credito,
        'customer_list':customer_list,
        'plan':plan,
        'list_guarantee':list_guarantee,
        'list_disbursement':list_disbursement,
        'detalle_garantia':DetailsGuarantees.objects.all(),
        'total_garantia':total_garantia(list_guarantee),
        'total_desembolso':total_desembolso(list_disbursement),
        'estado_cuenta':estado_cuenta,
        'siguiente_pago':siguiente_pago,
        'cuotas_vencidas':cuotas_vencidas,
        'total_cuota':formatear_numero(planPagosCredito(credito).calcular_total_cuotas()),
        'total_capital':formatear_numero(planPagosCredito(credito).calcular_total_capital()),
        'total_interes':formatear_numero(planPagosCredito(credito).calcular_total_interes()),
        'total_desembolsos':total_desembolsos(estado_cuenta),
        'total_moras':total_mora_pagada(estado_cuenta),
        'total_intereses':total_interes_pagada(estado_cuenta),
        'total_capitales':total_capital_pagada(estado_cuenta),

    }
    return render(request, template_name,context)

@login_required
@usuario_activo
def detallar_desembolso(request,id):
    
    desembolso = get_object_or_404(Disbursement,id=id)
    boletas = Payment.objects.filter(disbursement=desembolso)
    
    
    template_name = 'financings/disbursement/detail.html'
    context = {
        'title':'ELTELAR - DESEMBOLSO {}'.format(desembolso.credit_id),
        'desembolso':desembolso,
        'boletas':boletas,
    }
    return render(request, template_name, context)
   

@login_required
@usuario_activo
def detallar_recibo(request,id):
    
    pago = get_object_or_404(Payment, id=id)
    
    recibo = get_object_or_404(Recibo, pago=pago)

    

   
    template_name = 'financings/credit/recibo/detail.html'
    context = {
        'title':'ELTELAR - RECIBO',
        'recibo':recibo,
    }
    return render(request, template_name, context)


@login_required
@usuario_activo
def detalle_boleta(request,id):
    pago = get_object_or_404(Payment, id=id)
    template_name = 'financings/payment/detail.html'
    context = {
        'title':f'ELTELAR - BOLETA {pago.numero_referencia}',
        'pago':pago,
    }
    return render(request, template_name, context)

@login_required
@usuario_activo
def detalle_factura(request,id):
    pago = get_object_or_404(Payment, id=id)
    
    recibo = get_object_or_404(Recibo, pago=pago)
    if not recibo.factura:
        messages.error(request, 'Este pago no tiene factura')
        recibo.factura = True
        recibo.save()
    
        factura = Invoice()
        factura.recibo_id = recibo
        factura.save()
        messages.success(request, 'Factura creada')
    
    factura = Invoice.objects.filter(Q(recibo_id=recibo)).first()
    print(factura)
 
    template_name = 'financings/credit/factura/detail.html'
    context = {
        'title':'ELTELAR',
        'factura':factura,
        'recibo':recibo
    }
    return render(request,template_name,context)




@login_required
@usuario_activo
def detalle_estado_cuenta(request,id):
    credito = get_object_or_404(Credit,id=id)
    estado_cuenta = AccountStatement.objects.filter(credit=credito)
    siguiente_pago = PaymentPlan.objects.filter(credit_id=credito).order_by('-id').first()

    template_name = 'financings/credit/estado_cuenta/detail.html'
    actualizacion(credito)
    context = {
        'title':'ELTELAR',
        'credito':credito,
        'estado_cuenta':estado_cuenta,
        'total_desembolsos':total_desembolsos(estado_cuenta),
        'total_moras':total_mora_pagada(estado_cuenta),
        'total_intereses':total_interes_pagada(estado_cuenta),
        'total_capitales':total_capital_pagada(estado_cuenta),
        'dia':now,
        'siguiente_pago':siguiente_pago,
    }

    return render(request,template_name,context)
