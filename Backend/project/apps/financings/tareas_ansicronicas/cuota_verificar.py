# MODELOS
from apps.financings.models import PaymentPlan

# TIEMPO
from datetime import datetime
from django.utils.timezone import now

async def ver_cuotas_no_cargadas():
    planes = PaymentPlan.objects.filter(cuota_vencida=False)

    for cuota in planes:
        if cuota.fecha_limite.date() < now().date(): 
            print(cuota.id)