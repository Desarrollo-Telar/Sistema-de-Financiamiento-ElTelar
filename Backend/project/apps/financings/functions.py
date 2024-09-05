
# DECIMAL
from decimal import Decimal

# TIEMPO
from datetime import timedelta
from django.utils import timezone


def realizar_pago(credito_id, fecha_emision,  monto_pago):
    try:
        # Obtener el crédito
        credito = Credit.objects.get(id=credito_id)   

        # Verificar si el crédito ya está pagado
        if credito.is_paid_off:
            return "Este crédito ya está pagado en su totalidad."

        monto_restante = Decimal(monto_pago)
        fecha_pago = fecha_emision
        
        
        # Obtener las cuotas pendientes en orden cronológico
        cuotas = PaymentPlan.objects.filter(credit=credito, status=False).order_by('due_date')
        

        for cuota in cuotas:
            if monto_restante <= 0:
                break



            # Calcular el interés generado hasta la fecha de pago
            interes_generado = calcular_interes(cuota.outstanding_balance, cuota.interest, cuota.start_date, fecha_pago)
            cuota.interest = interes_generado

            # Calcular la mora si es aplicable
            mora_generada = calcular_mora(cuota.outstanding_balance, cuota.interest, cuota.due_date, fecha_pago)
            cuota.mora = mora_generada

            # Calcular el capital según la forma de pago y asegurarse de no superar la cuota con el interés
            capital_calculado = calcular_capital(cuota.outstanding_balance, interes_generado, credito.monto, credito.plazo, credito.forma_de_pago, cuota.principal)

            # Actualizar el capital en la cuota
            cuota.principal = capital_calculado

            # Aplicar a la mora
            if monto_restante >= cuota.mora:
                monto_restante -= cuota.mora
                cuota.outstanding_balance -= cuota.mora
                cuota.mora = Decimal(0)

            else:
                cuota.mora -= monto_restante
                cuota.outstanding_balance -= monto_restante
                monto_restante = Decimal(0)
                break



            # Aplicar al interés
            if monto_restante >= cuota.interest:
                monto_restante -= cuota.interest
                cuota.outstanding_balance -= cuota.interest
                cuota.interest = Decimal(0)

            else:
                cuota.interest -= monto_restante
                cuota.outstanding_balance -= monto_restante
                monto_restante = Decimal(0)
                break

        
            # Aplicar al capital
            if monto_restante >= cuota.principal:
                monto_restante -= cuota.principal
                cuota.outstanding_balance -= cuota.principal
                cuota.principal = Decimal(0)
                cuota.paid = True


            else:
                cuota.principal -= monto_restante
                cuota.outstanding_balance -= monto_restante
                monto_restante = Decimal(0)                
                break
            


            cuota.save()

        # Si hay monto restante después de cubrir la cuota actual, aplicarlo a la siguiente cuota
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

        # Si el monto no cubrió la cuota completa, acumular el saldo pendiente en la próxima cuota
        if monto_restante < 0:
            for i in range(len(cuotas)):
                if not cuotas[i].paid:
                    cuotas[i + 1].outstanding_balance += abs(monto_restante)
                    cuotas[i + 1].save()
                    break

        # Actualizar el saldo total del crédito
        credito.monto -= Decimal(monto_pago) - max(monto_restante, Decimal(0))

        if credito.monto <= 0:
            credito.monto = Decimal(0)
            credito.is_paid_off = True

        credito.save()



        # Registrar el pago
        #Payment.objects.create(credit=credito, monto=monto_pago, numero_referencia, fecha_emision,descripcion)
        
        # Registrar en el estado de cuenta
        """ 
        if pago_realizado == 'COMPLETADO':
            AccountStatement.objects.create(
                credit=credito,
                description=f"Pago recibido",
                amount=monto_pago,
                balance=credito.balance
            )

        """

        return f"Pago de {monto_pago} realizado exitosamente. Saldo restante: {credito.monto}"



    except Credit.DoesNotExist:
        return "Crédito no encontrado."


