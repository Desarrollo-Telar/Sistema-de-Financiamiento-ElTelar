from apps.financings.functions import realizar_pago
from apps.financings.models import Payment, Banco
from django.shortcuts import get_object_or_404
from datetime import datetime
def generar():
    bancos = Banco.objects.all()
    if bancos:

        for banco in bancos:
            pagos = Payment.objects.filter(numero_referencia=banco.referencia)
        

            if pagos.exists():  # Verifica si hay pagos asociados al banco
                for pago in pagos:
                    #banco_referencia = get_object_or_404(Banco, referencia=pago.numero_referencia)
                    banco_referencia = Banco.objects.filter(referencia=pago.numero_referencia)
                
                    # Actualiza el monto del pago si no coincide con el del banco
                    # Inicializa un flag para determinar si se debe cambiar el estado
                    cambiar_estado = False
                    
                    # Verifica y actualiza el monto del pago
                    if pago.monto != banco_referencia.credito:
                        pago.monto = banco_referencia.credito

                    if pago.monto != banco_referencia.debito:
                        pago.monto = banco_referencia.debito

                    # Verifica la fecha de emisión
                    print(banco_referencia.fecha)
                    print(pago.fecha_emision.date())
                    
                    if pago.fecha_emision.date() != banco_referencia.fecha:
                        cambiar_estado = True
                        pago.fecha_emision = banco_referencia.fecha
                        

                    # Si se ha modificado el monto o la fecha, guarda el pago
                    if cambiar_estado or (pago.monto != banco_referencia.credito or pago.monto != banco_referencia.debito):
                        pago.save()
                    


                    # Si la transacción está pendiente, se realiza el pago
                    if pago.estado_transaccion == 'PENDIENTE' or pago.estado_transaccion == 'Pendiente':
                    
                        realizar_pago(pago, pago.credit,  pago.disbursement, pago.cliente)
                        
                    #pago.realizar_pago()
