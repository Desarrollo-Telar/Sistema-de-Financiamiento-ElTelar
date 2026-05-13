import os
import django

# Configura el entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

# Tiempo
from datetime import datetime,timedelta

# Modelos
from apps.financings.models import Credit, PaymentPlan

# DECIMAL
from decimal import Decimal

def cuota_actual(credito):
    dia = datetime.now().date()
    dia_mas_uno = dia + timedelta(days=1)
    siguiente_pago = None

    if credito.is_paid_off:
        siguiente_pago = PaymentPlan.objects.filter(
        credit_id__id=credito.id).order_by('-id').first()
        
    else:
        siguiente_pago = PaymentPlan.objects.filter(
            credit_id__id=credito.id,
            start_date__lte=dia,
            fecha_limite__gte=dia_mas_uno
        ).first()

    
    if siguiente_pago is None:
        siguiente_pago = PaymentPlan.objects.filter(
        credit_id__id=credito.id).order_by('-id').first()

    return siguiente_pago 



if __name__ == '__main__':

    creditos = Credit.objects.filter(
        estados_fechas=True, 
        is_paid_off=False)
    
    for credito in creditos:
        cuota = cuota_actual(credito)

        if cuota.mora != 0:
            continue

        tasa_interes = credito.tasa_interes

        saldo_capital_pendiente = cuota.saldo_pendiente

        interes_cuota =  round(Decimal(cuota.interest),2)

        calculo_interes = round( Decimal(saldo_capital_pendiente) * Decimal(tasa_interes), 2)

        if interes_cuota == 0:
            continue

        verificacion = interes_cuota - calculo_interes

        if verificacion != 0:
            print(f'REVISEMOS ESTE CREDITO: {credito.id} porque tiene un resultado: {verificacion}')


