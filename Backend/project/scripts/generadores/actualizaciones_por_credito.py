# FORMATEADOR DE NUMEROS
from .formato_numero import formatear_numero

# MODELOS
from apps.financings.models import PaymentPlan

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