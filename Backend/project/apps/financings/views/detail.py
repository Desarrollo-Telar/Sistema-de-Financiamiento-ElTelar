from django.shortcuts import render, get_object_or_404, redirect

# Models
from apps.financings.models import Credit, Guarantees, Disbursement,DetailsGuarantees, Banco, Payment, PaymentPlan, AccountStatement, Recibo
from apps.customers.models import Customer, CreditCounselor
from apps.financings.models import Invoice
from apps.documents.models import DocumentGuarantee


from django.db.models import Q

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import usuario_activo, permiso_requerido
from django.utils.decorators import method_decorator
# Manejo de mensajes
from django.contrib import messages

# Tiempo
from datetime import datetime,timedelta

# Scripts
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario

# TAREA ASINCRONICO
from apps.financings.task import comparacion_para_boletas_divididas
from apps.financings.functions_payment import revisar

# LIBRERIAS PARA CRUD
from django.db.models import Q

# SCRIPTS 
from scripts.generadores.formato_numero import formatear_numero
from scripts.generadores.plan import planPagosCredito
from scripts.generadores.actualizaciones_por_credito import total_garantia, total_desembolso, actualizacion, total_desembolsos, total_mora_pagada, total_interes_pagada, total_capital_pagada

from django.http import Http404

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
        credito = Credit.objects.filter(id=id, customer_id__new_asesor_credito=asesor_autenticado).first()

        if credito is None:
            messages.error(request, 'Usted no tiene permitido visualizar el credito de este cliente.')
            return redirect('financings:list_credit')
        
    generar_todas_las_cuotas_credito(credito.codigo_credito)
    #cambiar_plan() # CAMBIAR AUTOMATICAMENTE PARA PRUEBAS
    
    customer_list = get_object_or_404(Customer,id= credito.customer_id.id) # LISTAR LA INFORMACION DEL CLIENTE

    # LISTAR LAS GARANTIAS REGISTRADAS
    list_guarantee = Guarantees.objects.filter(credit_id=credito).order_by('-id') 

    list_disbursement = Disbursement.objects.filter(credit_id=credito).order_by('id') # LISTAR DESEMBOLSOS

    dia = datetime.now().date()
    dia_mas_uno = dia + timedelta(days=1)
    
    siguiente_pago = PaymentPlan.objects.filter(
        credit_id=credito,
        start_date__lte=dia,
        fecha_limite__gte=dia_mas_uno
    ).first()
    cuotas_vencidas = PaymentPlan.objects.filter(credit_id=credito, cuota_vencida=True).order_by('mes')
    estado_cuenta = AccountStatement.objects.filter(credit=credito).order_by('issue_date')
    #actualizacion(credito)
    if siguiente_pago is None:
        siguiente_pago = PaymentPlan.objects.filter(
        credit_id=credito).order_by('-id').first()
    
    print(siguiente_pago.mes)

    saldo_actual = siguiente_pago.saldo_pendiente + siguiente_pago.mora + siguiente_pago.interest

    credito.saldo_actual = saldo_actual
    credito.save()
    
    print(siguiente_pago)
    
    
    
    

    # PLAN DE PAGOS
    plan = planPagosCredito(credito).generar_plan()
    
   
   
    context = {
        'title': f'Detalle del Credito. {credito}',
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
        'permisos':recorrer_los_permisos_usuario(request),

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
        'title':'Detalle del Desembolso. {}'.format(desembolso.credit_id),
        'desembolso':desembolso,
        'boletas':boletas,
        'credit_list':credit_list,
        'customer_list':customer_list,
        'permisos':recorrer_los_permisos_usuario(request),
    }
    return render(request, template_name, context)

@login_required
@usuario_activo
def detallar_garantia(request, id):
    garantia = get_object_or_404(Guarantees, id=id)
    credit_list = Credit.objects.filter(id=garantia.credit_id.id).first()
    customer_list = Customer.objects.get(id=credit_list.customer_id.id)
    detalle_garantia = DetailsGuarantees.objects.filter(garantia_id=garantia)
    documentos = DocumentGuarantee.objects.filter(garantia__in=detalle_garantia)


    template_name = 'financings/guarantee/detail.html'

    context = {
        'credit_list':credit_list,
        'customer_list':customer_list,
        'detalle_garantia':detalle_garantia,
        'garantia':garantia,
        'documentos':documentos,
        'permisos':recorrer_los_permisos_usuario(request),
    }
    return render(request, template_name, context)
   
@login_required
@permiso_requerido('puede_ver_detalle_boleta_pago')
def boleta(request,numero_referencia):
    template_name = 'financings/bank/boleta.html'
    
    boleta = Payment.objects.filter( Q(numero_referencia=numero_referencia)| Q(numero_referencia__regex=rf"^{numero_referencia}-D\d*$"))
    context = {
        'title':'Detalle de la boleta.',
        'boletas':boleta,
        'posicion':numero_referencia,
        'permisos':recorrer_los_permisos_usuario(request),
    }

    return render(request, template_name, context)

@login_required
@usuario_activo
def clasificacion_detallar(request,numero_referencia):
    estado_cuenta = AccountStatement.objects.filter(numero_referencia=numero_referencia).first()

    if not estado_cuenta:
        return redirect('financings:boleta', numero_referencia)

    if estado_cuenta.cuota:
        return redirect('financings:detail_credit',estado_cuenta.credit.id)

    if estado_cuenta.payment:
        return redirect('financings:recibo',estado_cuenta.payment.id)

    if estado_cuenta.disbursement:
        return redirect('financings:detail_disbursement', estado_cuenta.disbursement.id)

    

@login_required
@permiso_requerido('puede_ver_detalle_recibo_pago')
def detallar_recibo(request,id):
    try:
        pago = get_object_or_404(Payment, id=id)
            
        recibo = Recibo.objects.filter(pago=pago).first()

        if recibo is None:
            recibo = Recibo.objects.filter(id=id).first()

            if recibo is None:
                return redirect('http_404')

    except Payment.DoesNotExist:
        return redirect('http_404')

    

   
    template_name = 'financings/credit/recibo/detail.html'
    context = {
        'title':f'Recibo del pago. | {recibo.pago.numero_referencia} |' ,
        'recibo':recibo,
        'permisos':recorrer_los_permisos_usuario(request),
    }
    return render(request, template_name, context)


@login_required
@permiso_requerido('puede_ver_detalle_boleta_pago')
def detalle_boleta(request,id):
    pago = get_object_or_404(Payment, id=id)
    template_name = 'financings/payment/detail.html'

    boleta = Banco.objects.filter(referencia=pago.numero_referencia).first()

    

    if pago.estado_transaccion == "PENDIENTE":
        if pago.numero_referencia.endswith(("-D", "-d")):
            comparacion_para_boletas_divididas()
            return redirect('financings:detalle_boleta', pago.id)

        if boleta is not None:
            revisar(boleta)
            return redirect('financings:detalle_boleta', pago.id)

    context = {
        'title':f'Detalle de la boleta de pago. {pago.numero_referencia}',
        'pago':pago,
        'permisos':recorrer_los_permisos_usuario(request),
        
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
        'factura':factura,
        'recibo':recibo,
        'permisos':recorrer_los_permisos_usuario(request),
    }
    return render(request,template_name,context)




@login_required
@usuario_activo
def detalle_estado_cuenta(request,id):
    credito = get_object_or_404(Credit,id=id)
    estado_cuenta = AccountStatement.objects.filter(credit=credito)
    siguiente_pago = PaymentPlan.objects.filter(credit_id=credito).order_by('-id').first()

    template_name = 'financings/credit/estado_cuenta/detail.html'
    #actualizacion(credito)
    # Obtener la fecha y hora actual
    now = datetime.now()

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
        'permisos':recorrer_los_permisos_usuario(request),
    }

    return render(request,template_name,context)
