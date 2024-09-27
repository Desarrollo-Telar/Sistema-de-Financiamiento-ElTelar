from apps.financings.functions import realizar_pago
from apps.financings.models import Payment, Banco
from django.shortcuts import get_object_or_404
from datetime import datetime
def generar():
    bancos = Banco.objects.all()

    for banco in bancos:
        pagos = Payment.objects.filter(numero_referencia=banco.referencia)

        if pagos.exists():  # Verifica si hay pagos asociados al banco
            for pago in pagos:
                banco_referencia = get_object_or_404(Banco, referencia=pago.numero_referencia)
             
                # Actualiza el monto del pago si no coincide con el del banco
                if pago.monto != banco_referencia.credito:
                    #pass
                    pago.monto = banco_referencia.credito
                    pago.save()
                elif pago.monto != banco_referencia.debito:
                    pago.monto = banco_referencia.debito
                    pago.save()
                elif pago.fecha_emision.strftime('%d/%m/%Y') != banco_referencia.fecha:
                    pago.estado_transaccion = 'FALLIDO'
                    pago.save()

                # Si la transacción está pendiente, se realiza el pago
                if pago.estado_transaccion == 'PENDIENTE' or pago.estado_transaccion == 'Pendiente':
                    realizar_pago(pago.credit, pago)
                #pago.realizar_pago()
