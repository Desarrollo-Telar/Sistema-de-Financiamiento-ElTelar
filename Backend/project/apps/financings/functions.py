from decimal import Decimal
from datetime import timedelta
from django.utils import timezone
from django.db.models import Sum  # Importar Sum para el cálculo del saldo pendiente
from apps.financings.models import Credit, PaymentPlan, AccountStatement, Payment
from apps.financings.utils import calcular_capital, calcular_interes, calcular_mora

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

            

        return f"Pago de {monto_pago} realizado exitosamente. Saldo restante: "

    except Credit.DoesNotExist:
        return "Crédito no encontrado."
