from django.shortcuts import render, get_object_or_404, redirect

# Models
from apps.financings.models import Credit, Guarantees, Disbursement,DetailsGuarantees, Banco, Payment, PaymentPlan, AccountStatement, Recibo
from apps.customers.models import Customer
from apps.financings.models import Invoice
from apps.documents.models import DocumentGuarantee


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
        total_desembolso +=desembolso.total_gastos
    
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
from apps.financings.tareas_ansicronicas import generar_todas_las_cuotas_credito
@login_required
@usuario_activo
def detail_credit(request,id):
    
    template_name = 'financings/credit/detail.html' # TEMPLATE
    credito= get_object_or_404(Credit,id=id) # DETALLE DEL CREDITO
    generar_todas_las_cuotas_credito(credito.codigo_credito)
    cambiar_plan() # CAMBIAR AUTOMATICAMENTE PARA PRUEBAS
    
    customer_list = get_object_or_404(Customer,id= credito.customer_id.id) # LISTAR LA INFORMACION DEL CLIENTE

    # LISTAR LAS GARANTIAS REGISTRADAS
    list_guarantee = Guarantees.objects.filter(credit_id=credito).order_by('-id') 

    list_disbursement = Disbursement.objects.filter(credit_id=credito).order_by('id') # LISTAR DESEMBOLSOS

    dia = datetime.now().date()
    
    
    siguiente_pago = PaymentPlan.objects.filter(
        credit_id=credito,
        start_date__lte=dia,
        fecha_limite__gte=dia
    ).first()
    cuotas_vencidas = PaymentPlan.objects.filter(credit_id=credito, cuota_vencida=True)
    estado_cuenta = AccountStatement.objects.filter(credit=credito).order_by('issue_date')
    #actualizacion(credito)
    saldo_actual = siguiente_pago.saldo_pendiente + siguiente_pago.mora + siguiente_pago.interest

    credito.saldo_actual = saldo_actual
    credito.save()
    
    
    
    
    

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
        'saldo_actual': formatear_numero(saldo_actual),

    }
    return render(request, template_name,context)

@login_required
@usuario_activo
def detallar_desembolso(request,id):
    
    desembolso = get_object_or_404(Disbursement,id=id)
    boletas = Payment.objects.filter(disbursement=desembolso)
    credit_list = Credit.objects.filter(codigo_credito=desembolso.credit_id.codigo_credito).first()
    customer_list = Customer.objects.filter(id=credit_list.customer_id.id).first()
    template_name = 'financings/disbursement/detail.html'
    context = {
        'title':'ELTELAR - DESEMBOLSO {}'.format(desembolso.credit_id),
        'desembolso':desembolso,
        'boletas':boletas,
        'credit_list':credit_list,
        'customer_list':customer_list
    }
    return render(request, template_name, context)

@login_required
@usuario_activo
def detallar_garantia(request, id):
    detalle = get_object_or_404(DetailsGuarantees, garantia_id__id=id)
    #detalle_garantia = DetailsGuarantees.objects.filter(garantia_id=garantia)

    credit_list = Credit.objects.filter(codigo_credito=detalle.garantia_id.credit_id.codigo_credito).first()
    customer_list = Customer.objects.filter(id=credit_list.customer_id.id).first()
    documentos = DocumentGuarantee.objects.filter(garantia=detalle)

    template_name = 'financings/guarantee/detail.html'

    context = {
        'title':'ELTELAR - GARANTIA {}'.format(detalle.garantia_id.credit_id),
        'documentos':documentos,
        'detalle':  detalle,     
        'credit_list':credit_list,
        'customer_list':customer_list
    }
    return render(request, template_name, context)
   
@login_required
@usuario_activo
def boleta(request,numero_referencia):
    template_name = 'financings/bank/boleta.html'
    
    boleta = Payment.objects.filter( Q(numero_referencia=numero_referencia)| Q(numero_referencia__regex=rf"^{numero_referencia}-D\d*$"))
    context = {
        'title':'EL TELAR',
        'boletas':boleta,
        'posicion':numero_referencia
    }

    return render(request, template_name, context)

@login_required
@usuario_activo
def clasificacion_detallar(request,numero_referencia):
    estado_cuenta = AccountStatement.objects.filter(numero_referencia=numero_referencia).first()

    if not estado_cuenta:
        return redirect('financings:boleta', numero_referencia)

    if estado_cuenta.cuota:
        messages.success(request, "CUOTA")
        return redirect('financings:detail_credit',estado_cuenta.credit.id)

    if estado_cuenta.payment:
        messages.success(request, "PAGO")
        return redirect('financings:recibo',estado_cuenta.payment.id)

    if estado_cuenta.disbursement:
        messages.success(request, 'DESEMBOLSO')
        return redirect('financings:detail_disbursement', estado_cuenta.disbursement.id)

    

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
    
    recibo = get_object_or_404(Recibo, id=id)
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
