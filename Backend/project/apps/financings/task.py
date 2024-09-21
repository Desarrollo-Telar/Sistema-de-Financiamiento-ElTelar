from celery import shared_task
from datetime import datetime
from .models import PaymentPlan

@shared_task
def cambiar_plan():
    planes = PaymentPlan.objects.filter(fecha_limite__date=datetime.now().date(), status=False)

    for pago in planes:
        pago.status = True        
        pago.save()
        acumulacion_mora = (pago.acumulacion_mora - pago.mora_acumulado_pagado) + (pago.mora - pago.mora_pagado)
        

        nuevo_plan = PaymentPlan(saldo_pendiente=pago.saldo_pendiente, credit_id= pago.credit_id, start_date=pago.due_date,mora_acumulada=acumulacion_mora, outstanding_balance=pago.saldo_pendiente)
        nuevo_plan.save()
