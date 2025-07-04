# CLASES
from apps.financings.clases.paymentplan import PaymentPlan as PlanPagoos
from apps.financings.clases.credit import Credit as Credito

def planPagosCredito(credito):
    formatted_date = credito.fecha_inicio.strftime('%Y-%m-%d')
    credit = Credito(credito.proposito,credito.monto,credito.plazo,credito.tasa_interes,credito.forma_de_pago,credito.frecuencia_pago,formatted_date,credito.tipo_credito,1,None,credito.fecha_vencimiento)
    plan_pago = PlanPagoos(credit)
    return plan_pago