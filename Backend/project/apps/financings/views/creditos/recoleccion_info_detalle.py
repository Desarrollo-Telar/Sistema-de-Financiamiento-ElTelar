
# SCRIPTS
from scripts.generadores.plan import planPagosCredito
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario
from scripts.generadores.formato_numero import formatear_numero
from scripts.generadores.actualizaciones_por_credito import total_garantia, total_desembolso,  total_desembolsos, total_mora_pagada, total_interes_pagada, total_capital_pagada


# MODELO
from apps.customers.models import Customer, HistorialCobranza, Cobranza
from apps.financings.models import  Guarantees, Disbursement,DetailsGuarantees,  PaymentPlan, AccountStatement
from apps.actividades.models import VotacionCredito


# forms
from apps.actividades.forms.votaciones import VotacionCreditoForm

def informacion_detalle(request, credito, saldo_actual, siguiente_pago):

    # LISTAR LA INFORMACION DEL CLIENTE
    customer_list = Customer.objects.filter(id=credito.customer_id.id).first()

    # PLAN DE PAGOS
    plan = planPagosCredito(credito).generar_plan()

    # LISTAR LAS GARANTIAS REGISTRADAS
    list_guarantee = Guarantees.objects.filter(credit_id=credito).order_by('-id') 

    # LISTAR DESEMBOLSOS
    list_disbursement = Disbursement.objects.filter(credit_id=credito).order_by('id') 

    # LISTAR CUOTAS VENCIDAS
    cuotas_vencidas = PaymentPlan.objects.filter(credit_id=credito, cuota_vencida=True).order_by('mes')

    # LISTAR EL ESTADO DE CUENTA
    estado_cuenta = AccountStatement.objects.filter(credit=credito).order_by('issue_date')

    # HISTORIAL DE COBRANZAS
    cobranzas = Cobranza.objects.filter(credito=credito)
    
    
    historial_cobranza = HistorialCobranza.objects.filter(cobranza__in=cobranzas).order_by('-fecha_cambio')

    

    contexto = {
        'title': f'Detalle del Credito. {credito}',
        'credit_list':credito,
        'customer_list':customer_list,
        'customer_code':customer_list.customer_code,
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
        'form':VotacionCreditoForm(),
        'comentarios':VotacionCredito.objects.filter(credito=credito).order_by('-id'),
        'historial_cobranza':historial_cobranza
       

    }
    return contexto