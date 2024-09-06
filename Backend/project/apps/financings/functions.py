from decimal import Decimal
from datetime import timedelta
from django.utils import timezone
from django.db.models import Sum  # Importar Sum para el cálculo del saldo pendiente
from apps.financings.models import Credit, PaymentPlan, AccountStatement, Payment
from apps.financings.utils import calcular_capital, calcular_interes, calcular_mora
from datetime import datetime, timedelta
def realizar_pago(credito_id, fecha_emision, monto_pago, payment):
    try:
        # Obtener el crédito
        credito = Credit.objects.get(id=credito_id.id)  
        
        # Verificar si el crédito ya está pagado
        if credito.is_paid_off:
            return "Este crédito ya está pagado en su totalidad."

        monto_restante = Decimal(monto_pago)
        fecha_pago = fecha_emision
        mora_pagada_total = Decimal(0)
        interes_pagado_total = Decimal(0)
        capital_pagado_total = Decimal(0)
        
        # Obtener las cuotas pendientes en orden cronológico
        cuotas = PaymentPlan.objects.filter(credit_id=credito, status=False).order_by('due_date')
        
        for cuota in cuotas:
            if monto_restante <= 0:
                break

            # Calcular interés y mora
            interes_generado = calcular_interes(cuota.outstanding_balance, credito.tasa_interes, cuota.start_date, fecha_pago, fecha_emision)
            mora_generada = calcular_mora(cuota.outstanding_balance, cuota.interest, cuota.due_date, fecha_pago)
            cuota.interest = interes_generado
            cuota.mora = mora_generada
            

            # Calcular capital
            capital_calculado = calcular_capital(cuota.outstanding_balance, interes_generado, credito.monto, credito.plazo, credito.forma_de_pago, cuota.principal)
            cuota.principal = capital_calculado

            print(fecha_pago)
            # Aplicar el pago a la mora
            if monto_restante >= cuota.mora:
                mora_pagada_total += cuota.mora
                monto_restante -= cuota.mora
                cuota.outstanding_balance -= cuota.mora
                cuota.mora = Decimal(0)
            else:
                mora_pagada_total += monto_restante
                cuota.mora -= monto_restante
                cuota.outstanding_balance -= monto_restante
                monto_restante = Decimal(0)
                break

            # Aplicar el pago al interés
            if monto_restante >= cuota.interest:
                interes_pagado_total += cuota.interest
                monto_restante -= cuota.interest
                cuota.outstanding_balance -= cuota.interest
                cuota.interest = Decimal(0)
            else:
                interes_pagado_total += monto_restante
                cuota.interest -= monto_restante
                cuota.outstanding_balance -= monto_restante
                monto_restante = Decimal(0)
                break

            # Aplicar el pago al capital
            if monto_restante >= cuota.principal:
                capital_pagado_total += cuota.principal
                monto_restante -= cuota.principal
                cuota.outstanding_balance -= cuota.principal
                cuota.principal = Decimal(0)
                cuota.status = True
            else:
                capital_pagado_total += monto_restante
                cuota.principal -= monto_restante
                cuota.outstanding_balance -= monto_restante
                monto_restante = Decimal(0)
                break

            cuota.save()

        
        if monto_restante > 0 and not cuotas[-1].status:
            for cuota in cuotas:
                if cuota.status:
                    continue
                cuota.outstanding_balance -= monto_restante

                if cuota.outstanding_balance <= 0:
                    cuota.status = True
                    monto_restante = abs(cuota.outstanding_balance)
                    cuota.outstanding_balance = Decimal(0)
                else:
                    monto_restante = Decimal(0)

                cuota.save()

        # Si el saldo pendiente es menor o igual a cero, marcar el crédito como pagado
        saldo_pendiente = PaymentPlan.objects.filter(credit_id=credito, status=False).aggregate(total_balance=Sum('outstanding_balance'))['total_balance'] or 0
        if saldo_pendiente <= 0:
            credito.is_paid_off = True
            credito.save()

        # Registrar el pago
        pagoss = Payment.objects.get(id=payment.id)        
        pagoss.estado_transaccion = 'COMPLETADO'
        pagoss.save()

        # Registrar en el estado de cuenta
        AccountStatement.objects.create(
            credit=credito,
            payment=payment,
            interest_paid=interes_pagado_total,
            capital_paid=capital_pagado_total,
            late_fee_paid=mora_pagada_total,
            description=f"Pago recibido el {payment.fecha_emision}",
            numero_referencia=payment.numero_referencia,
            abono=monto_pago,
            saldo_pendiente=saldo_pendiente
        )

            

        return f"Pago de {monto_pago} realizado exitosamente. Saldo restante: "

    except Credit.DoesNotExist:
        return "Crédito no encontrado."
