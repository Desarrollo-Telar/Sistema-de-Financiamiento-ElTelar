from django.shortcuts import render, get_object_or_404, redirect

# Models
from apps.financings.models import Credit, Guarantees, Disbursement,DetailsGuarantees, Banco, Payment, PaymentPlan, AccountStatement, Recibo
from apps.customers.models import Customer


from django.db.models import Q

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import usuario_activo
from django.utils.decorators import method_decorator



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





### ------------ DETALLE -------------- ###
@login_required
@usuario_activo
def detail_credit(request,id):
    template_name = 'financings/credit/detail.html'
    credito= get_object_or_404(Credit,id=id)
    cambiar_plan()
    
    customer_list = get_object_or_404(Customer,id= credito.customer_id.id)
    list_guarantee = Guarantees.objects.filter(credit_id=credito).order_by('-id')
    list_disbursement = Disbursement.objects.filter(credit_id=credito).order_by('-id')

    formatted_date = credito.fecha_inicio.strftime('%Y-%m-%d')
    siguiente_pago = PaymentPlan.objects.filter(credit_id=credito)
    estado_cuenta = AccountStatement.objects.filter(credit=credito)
    pagos = PaymentPlan.objects.filter(credit_id=credito).order_by('-id').first()
    

    
    
    if pagos:
        credito.saldo_pendiente = pagos.saldo_pendiente
        credito.saldo_actual = pagos.saldo_pendiente + pagos.mora + pagos.interest
        credito.save()
    
    
    credit = Credito(credito.proposito,credito.monto,credito.plazo,credito.tasa_interes,credito.forma_de_pago,credito.frecuencia_pago,formatted_date,credito.tipo_credito,1,None,credito.fecha_vencimiento)
    
    plan_pago = PlanPagoos(credit)
    total_garantia = 0
    total_desembolso = 0
    for garantia in list_guarantee:
        total_garantia += garantia.suma_total
    
    for desembolso in list_disbursement:
        total_desembolso +=desembolso.monto_total_desembolso
    
    plan = plan_pago.generar_plan()
   
   
    context = {
        'title':'ELTELAR - CREDITO',
        'credit_list':credito,
        'customer_list':customer_list,
        'plan':plan,
        'list_guarantee':list_guarantee,
        'list_disbursement':list_disbursement,
        'detalle_garantia':DetailsGuarantees.objects.all(),
        'total_garantia':total_garantia,
        'total_desembolso':total_desembolso,
        'estado_cuenta':estado_cuenta,
        'siguiente_pago':siguiente_pago,
        'total_cuota':plan_pago.calcular_total_cuotas(),
        'total_capital':plan_pago.calcular_total_capital(),
        'total_interes':plan_pago.calcular_total_interes()

    }
    return render(request, template_name,context)

@login_required
@usuario_activo
def detallar_desembolso(request,id):
    
    desembolso = get_object_or_404(Disbursement,id=id)
    template_name = 'index.html'
    context = {
        'title':'ELTELAR - DESEMBOLSO {}'.format(desembolso.credit_id)
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


