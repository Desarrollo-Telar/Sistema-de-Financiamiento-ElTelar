# FUNCION ENCARGADA DE GENERAR TODAS LAS CUOTAS DE LOS CREDITOS

# MODELOS
from apps.financings.models import Credit, PaymentPlan
from apps.accountings.models import Creditor
# CALCULOS
from apps.financings.calculos import calculo_interes
from dateutil.relativedelta import relativedelta

from django.db import transaction

# TIEMPO
from datetime import datetime

def generar_todas_las_cuotas_acreedores(codigo_acreedor: str) -> None:
    acreedor = Creditor.objects.filter(codigo_acreedor=codigo_acreedor).first()
    plazo = acreedor.plazo
    tasa_i = acreedor.tasa

    if not acreedor:
        print('ACREEDOR NO ENCONTRADO')
        return
    
    if acreedor.is_paid_off:
        print('ACREEDOR CANCELADO')
        return
    
    lista = []

    primera_cuota = PaymentPlan.objects.filter(acreedor = acreedor).order_by('-id').first()
    plazo_restante = plazo - int(primera_cuota.mes)
    print(plazo_restante)
    lista.append(primera_cuota.due_date)

    todas_las_cuotas = PaymentPlan.objects.filter(acreedor = acreedor)
    contador = 0

    if plazo_restante <= 0:
        print('YA TIENE TODAS LA CUOTAS GENERADAS')
        ahora = datetime.now().date()

        fecha_limite = primera_cuota.fecha_limite.date()

        if fecha_limite < ahora:
            print('POR GENERAR OTRA CUOTA')
            cuota_n = PaymentPlan(
                start_date=primera_cuota.due_date,
                outstanding_balance=primera_cuota.saldo_pendiente,
                interest = calculo_interes(primera_cuota.saldo_pendiente, tasa_i),
                acreedor = acreedor,
                interes_generado = calculo_interes(primera_cuota.saldo_pendiente, tasa_i),
                saldo_pendiente=primera_cuota.saldo_pendiente
            )
            cuota_n.save()

        return

    for cuota in range(0, plazo_restante):
        print('creando cuotas')
        cuota_n = PaymentPlan(
            start_date=lista[contador],
            outstanding_balance=primera_cuota.saldo_pendiente,
            interest = calculo_interes(primera_cuota.saldo_pendiente, tasa_i),
            acreedor = acreedor,
            interes_generado = calculo_interes(primera_cuota.saldo_pendiente, tasa_i),
            saldo_pendiente=primera_cuota.saldo_pendiente
        )
        cuota_n.save()
        lista.append(cuota_n.due_date)
        contador += 1

    

def generar_todas_las_cuotas_credito(codigo_credito: str) -> None:
    credito = Credit.objects.filter(codigo_credito=codigo_credito).first()
    original_day = credito.fecha_inicio.day
    plazo = credito.plazo

    if not credito:
        print("Crédito no encontrado")
        return
    if credito.is_paid_off:
        print("CREDITO CANCELADO")
        return
    
    if credito.estado_judicial:
        print('NO SE PUEDE GENERAR MÁS CUOTAS, SE ENCUENTRA EN ESTADO JUDICIAL')
        return
    
    
    lista = []

    primera_cuota = PaymentPlan.objects.filter(credit_id = credito).order_by('-id').first()
    plazo_restante = plazo - int(primera_cuota.mes)
    
    lista.append(primera_cuota.due_date)

    todas_las_cuotas = PaymentPlan.objects.filter(credit_id = credito)
    contador = 0

    if plazo_restante <= 0:
        print('YA TIENE TODAS LA CUOTAS GENERADAS')
        ahora = datetime.now().date()

        fecha_limite = primera_cuota.fecha_limite.date()

        if fecha_limite < ahora:
            print('POR GENERAR OTRA CUOTA')
            cuota_n = PaymentPlan(
                start_date=primera_cuota.due_date,
                outstanding_balance=primera_cuota.saldo_pendiente,
                interest = calculo_interes(primera_cuota.saldo_pendiente,  credito.tasa_interes),
                credit_id = credito,
                interes_generado = calculo_interes(primera_cuota.saldo_pendiente,  credito.tasa_interes),
                saldo_pendiente=primera_cuota.saldo_pendiente,
                original_day=original_day
            )
            cuota_n.save()
        return

    for cuota in range(0, plazo_restante):
        print('creando cuotas')
        cuota_n = PaymentPlan(
            start_date=lista[contador],
            outstanding_balance=primera_cuota.saldo_pendiente,
            interest = calculo_interes(primera_cuota.saldo_pendiente, credito.tasa_interes),
            credit_id = credito,
            interes_generado = calculo_interes(primera_cuota.saldo_pendiente, credito.tasa_interes),
            saldo_pendiente=primera_cuota.saldo_pendiente,
            original_day=original_day
        )
        cuota_n.save()
        lista.append(cuota_n.due_date)
        contador += 1

    

