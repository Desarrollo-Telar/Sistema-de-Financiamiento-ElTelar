# FUNCION ENCARGADA DE GENERAR TODAS LAS CUOTAS DE LOS CREDITOS

# MODELOS
from apps.financings.models import Credit, PaymentPlan
from apps.accountings.models import Creditor
# CALCULOS
from apps.financings.calculos import calculo_interes
from dateutil.relativedelta import relativedelta

from django.db import transaction

def generar_todas_las_cuotas_acreedores(codigo_acreedor: str) -> None:
    acreedor = Creditor.objects.filter(codigo_acreedor=codigo_acreedor).first()

    if not acreedor:
        print('ACREEDOR NO ENCONTRADO')
        return
    
    if acreedor.is_paid_off:
        print('ACREEDOR CANCELADO')
        return
    
    lista = []

    primera_cuota = PaymentPlan.objects.filter(acreedor = acreedor).order_by('id').first()

    lista.append(primera_cuota.due_date)

    todas_las_cuotas = PaymentPlan.objects.filter(acreedor = acreedor)
    contador = 0

    for cuota in todas_las_cuotas:
        if cuota == primera_cuota:
            print('ESTA CUOTA NO CUENTA, EL LA PRIMERA CUOTA. VAMOS POR LA SIGUIENTE')
            continue

        cuota.start_date = lista[contador]
        
        cuota.save()
        lista.append(cuota.due_date)
        contador += 1

def generar_todas_las_cuotas_credito(codigo_credito: str) -> None:
    credito = Credit.objects.filter(codigo_credito=codigo_credito).first()

    if not credito:
        print("Crédito no encontrado")
        return
    if credito.is_paid_off:
        print("CREDITO CANCELADO")
        return
    
    """ 
    lista = []

    primera_cuota = PaymentPlan.objects.filter(credit_id = credito).order_by('id').first()

    lista.append(primera_cuota.due_date)

    todas_las_cuotas = PaymentPlan.objects.filter(credit_id = credito)
    contador = 0

    for cuota in todas_las_cuotas:
        if cuota == primera_cuota:
            print('ESTA CUOTA NO CUENTA, EL LA PRIMERA CUOTA. VAMOS POR LA SIGUIENTE')
            continue

        cuota.start_date = lista[contador]
        
        cuota.save()
        lista.append(cuota.due_date)
        contador += 1
    """

