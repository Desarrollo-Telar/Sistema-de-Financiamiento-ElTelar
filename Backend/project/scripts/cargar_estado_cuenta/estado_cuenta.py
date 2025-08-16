# Modelos
from apps.financings.models import AccountStatement, Credit, Banco, Payment, Recibo
from apps.customers.models import Customer

def creacion_pago(numero_referencia, fecha, monto, credito):
    banco = Banco.objects.filter(referencia=numero_referencia).first()

    if banco is not None:
        banco.credito=monto
        banco.fecha=fecha
        banco.status = True
        banco.registro_ficticio = False
        banco.save()
    else:
        banco = Banco.objects.create(
            referencia=numero_referencia,
            credito=monto,
            fecha=fecha,
            status = True,
            registro_ficticio = False
        )

    pago = Payment.objects.filter(numero_referencia=numero_referencia).first()

    if pago is not None:
        pago.credit=credito
        pago.monto=monto
        pago.numero_referencia=numero_referencia
        pago.fecha_emision=fecha
        pago.estado_transaccion='COMPLETADO'
        pago.save()
        return pago

    return Payment.objects.create(
        credit=credito,
        monto=monto,
        numero_referencia=numero_referencia,
        fecha_emision=fecha,
        estado_transaccion='COMPLETADO'
    )


def creacion_recibo(fecha, cliente, pago, interes_pagado, aporte_capital, total):

    recibo = Recibo.objects.filter(pago=pago).first()

    if recibo is not None:
        recibo.fecha=fecha
        recibo.cliente=cliente
        recibo.pago=pago
        recibo.interes=interes_pagado
        recibo.interes_pagado=interes_pagado
        recibo.aporte_capital=aporte_capital
        recibo.total=total
        recibo.save()
        return recibo
    
    return Recibo.objects.create(
        fecha=fecha,
        cliente=cliente,
        pago=pago,
        interes=interes_pagado,
        interes_pagado=interes_pagado,
        aporte_capital=aporte_capital,
        total=total
    )

def creacion_estado_cuenta(credit, payment, issue_date, interest_paid, capital_paid, saldo_pendiente, abono, numero_referencia):

    estado_cuenta = AccountStatement.objects.filter(numero_referencia=numero_referencia).first()

    if estado_cuenta is not None:
        estado_cuenta.credit=credit
        estado_cuenta.payment=payment
        estado_cuenta.issue_date=issue_date
        estado_cuenta.interest_paid=interest_paid
        estado_cuenta.capital_paid=capital_paid
        estado_cuenta.saldo_pendiente=saldo_pendiente
        estado_cuenta.abono=abono
        estado_cuenta.numero_referencia=numero_referencia
        estado_cuenta.description='PAGO DE CREDITO'

        estado_cuenta.save()
        return estado_cuenta

    return AccountStatement.objects.create(
        credit=credit,
        payment=payment,
        issue_date=issue_date,
        interest_paid=interest_paid,
        capital_paid=capital_paid,
        saldo_pendiente=saldo_pendiente,
        abono=abono,
        numero_referencia=numero_referencia,
        description='PAGO DE CREDITO'
    )

def migracion_datos():
    credito = Credit.objects.get(id=347)
    cliente = Customer.objects.get(id=credito.customer_id.id)

    listado_referencias = [
        {
            'num_refe':'2110682117',
            'fecha':'2024-09-29',
            'monto':2277,
            'interes_pagado':1875,
            'aporte_capital':402,
            'estado_transaccion':'COMPLETADO',
            'registro_ficticio':True,
            'saldo_pendiente':24598,
        },
        {
            'num_refe':'1087125150',
            'fecha':'2024-10-28',
            'monto':2277,
            'interes_pagado': 1300,
            'aporte_capital':700,
            'estado_transaccion':'COMPLETADO',
            'registro_ficticio':True,
            'saldo_pendiente':(3000 - 700),
        },
        {
            'num_refe':'2096697146',
            'fecha':'2024-12-14',
            'monto':1000,
            'interes_pagado': 0,
            'aporte_capital':1000,
            'estado_transaccion':'COMPLETADO',
            'registro_ficticio':True,
            'saldo_pendiente':1300,
        },
        {
            'num_refe':'1690720350',
            'fecha':'2025-04-24',
            'monto':200,
            'interes_pagado': 200,
            'aporte_capital':0,
            'estado_transaccion':'COMPLETADO',
            'registro_ficticio':True,
            'saldo_pendiente':1300,
        },
        {
            'num_refe':'2020565486',
            'fecha':'2025-05-05',
            'monto':300,
            'interes_pagado': (190+110),
            'aporte_capital':0,
            'estado_transaccion':'COMPLETADO',
            'registro_ficticio':True,
            'saldo_pendiente':1300,
        }
        
       
        
    ]

    for migrar in listado_referencias:
        pago = creacion_pago(
            migrar['num_refe'], migrar['fecha'],migrar['monto'], credito
        )

        creacion_recibo(
            migrar['fecha'],cliente, pago, migrar['interes_pagado'], migrar['aporte_capital'],migrar['monto']
        )

        creacion_estado_cuenta(
            credito, pago,  migrar['fecha'], migrar['interes_pagado'],  migrar['aporte_capital'], migrar['saldo_pendiente'],migrar['monto'],migrar['num_refe']
        )