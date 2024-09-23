from celery import shared_task
from datetime import datetime
from .models import PaymentPlan, Payment

def calculo_mora(saldo_pendiente, tasa_interes):
    mora = saldo_pendiente * (tasa_interes) * 0.1
    return round(mora,2)

def calculo_interes(saldo_pendiente, tasa_interes):
    interes = saldo_pendiente * (tasa_interes )
    return round(interes,2)

@shared_task
def cambiar_plan():
    planes = PaymentPlan.objects.filter(due_date=datetime.now(), status=False)

    for pago in planes:
        # Validar si hay algún pago registrado para este crédito y plan
        boleta = Payment.objects.filter(credit=pago.credit_id)
        if not boleta:
            pago.status = True     
            # Calcular la mora acumulada solo si hay atraso (después de 15 días)
            mora_acumulada = calculo_mora(pago.saldo_pendiente, pago.credit_id.tasa_interes)
            # nueva mora = 15 + 150 
            #pago.mora = pago.mora + mora_acumulada
            pago.mora += mora_acumulada   
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
