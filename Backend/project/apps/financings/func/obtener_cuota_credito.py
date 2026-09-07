# Tiempo
from datetime import datetime,timedelta

from apps.financings.models import PaymentPlan



def cuota(credito):
    dia = datetime.now().date()
    dia_mas_uno = dia + timedelta(days=1)
    cuota_actual = None

    if credito.is_paid_off:
        cuota_actual = PaymentPlan.objects.filter(
        credit_id__id=credito.id).order_by('-id').first()
        
    else:
        cuota_actual = PaymentPlan.objects.filter(
            credit_id__id=credito.id,
            start_date__lte=dia,
            fecha_limite__gte=dia_mas_uno
        ).first()

    
    if cuota_actual is None:
        cuota_actual = PaymentPlan.objects.filter(
        credit_id__id=credito.id).order_by('-id').first()

    return cuota_actual 