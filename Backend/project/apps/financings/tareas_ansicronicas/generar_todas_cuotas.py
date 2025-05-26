# FUNCION ENCARGADA DE GENERAR TODAS LAS CUOTAS DE LOS CREDITOS

# MODELOS
from apps.financings.models import Credit, PaymentPlan

# CALCULOS
from apps.financings.calculos import calculo_interes

def generar_todas_las_cuotas_credito(codigo_credito):
    credito = Credit.objects.filter(codigo_credito=codigo_credito).first()

    if credito.is_paid_off:
        print('CREDITO CANCELADO')
        return

    ultima_cuota = PaymentPlan.objects.filter(credit_id=credito).order_by('-id').first()

    plazo = credito.plazo
    plazo_restante = plazo - int(ultima_cuota.mes)
    
    for generar_cuota in range(0,plazo_restante):
        
        interes = calculo_interes(ultima_cuota.saldo_pendiente, credito.tasa_interes)
        
        cuota = PaymentPlan(
            start_date = ultima_cuota.due_date,
            outstanding_balance = ultima_cuota.saldo_pendiente,
            saldo_pendiente = ultima_cuota.saldo_pendiente,
            interest = interes,
            credit_id=credito
        )
        cuota.save()



