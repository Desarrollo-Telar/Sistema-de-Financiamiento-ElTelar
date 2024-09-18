from celery import shared_task
from datetime import datetime
from .models import PaymentPlan

@shared_task
def cambiar_plan():
    planes = PaymentPlan.objects.filter(fecha_limite__date=datetime.now().date(), status=False)

    for pago in planes:
        pago.status = True
        pago.save()

        nuevo_plan = PaymentPlan(saldo_pendiente=pago.saldo_pendiente, credit_id= pago.credit_id, start_date=pago.due_date,mora_acumulada=pago.mora, outstanding_balance=pago.saldo_pendiente)
        nuevo_plan.save()
