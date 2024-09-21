from celery import shared_task
from datetime import datetime
from .models import PaymentPlan

def calculo_mora(saldo_pendiente, tasa_interes):
    mora = saldo_pendiente * (tasa_interes/12) * 0.1
    return round(mora,2)

def calculo_interes(saldo_pendiente, tasa_interes):
    interes = saldo_pendiente * (tasa_interes /12)
    return round(interes,2)

@shared_task
def cambiar_plan():
    planes = PaymentPlan.objects.filter(fecha_limite__date=datetime.now().date(), status=False)

    for pago in planes:
        pago.status = True     
        pago.mora += calculo_mora(pago.saldo_pendiente, pago.credit_id.tasa_interes)   
        pago.save()

        interes = calculo_interes(pago.saldo_pendiente,pago.credit_id.tasa_interes)
        interes_acumulado = pago.interest + interes
        
        
        
        # CARGAR UNA NUEVA CUOTA CON POSIBLE ACUMULO DE INTERES Y DE MORA
        nuevo_plan = PaymentPlan(
            saldo_pendiente=pago.saldo_pendiente, 
            credit_id= pago.credit_id, 
            start_date=pago.due_date,
            mora=pago.mora, 
            outstanding_balance=pago.saldo_pendiente,
            interest=interes_acumulado
            )
        nuevo_plan.save()
