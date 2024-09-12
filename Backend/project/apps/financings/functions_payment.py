from apps.financings.functions import realizar_pago
from apps.financings.models import Payment, Banco
from django.shortcuts import get_object_or_404

def generar():
    bancos = Banco.objects.all()

    for banco in bancos:
        pagos = Payment.objects.filter(numero_referencia=banco.referencia)

        if pagos.exists():  # Verifica si hay pagos asociados al banco
            print('REALIZAR PAGOS')

            for pago in pagos:
                banco_referencia = get_object_or_404(Banco, referencia=pago.numero_referencia)

                # Actualiza el monto del pago si no coincide con el del banco
                #if pago.monto != banco_referencia.credito:
                    #pass
                    #pago.monto = banco_referencia.credito
                    #pago.save()

                # Si la transacción está pendiente, se realiza el pago
                if pago.estado_transaccion == 'PENDIENTE':
                    realizar_pago(pago.credit, pago)
