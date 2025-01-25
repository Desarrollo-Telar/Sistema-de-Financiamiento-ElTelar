from apps.financings.functions import realizar_pago
# MODELOS
from apps.financings.models import Payment, Banco
from apps.accountings.models import Income, Egress
from django.shortcuts import get_object_or_404
from datetime import datetime

def generar():
    try:
    
        print('Validando las boletas con bancos')
        boletas = Banco.objects.filter(status=False)
        
        if not boletas:
            print('No hay comprobacion')
            return f'No hay comprobacion aun...'
        
        for boleta in boletas:
            print('Se estaran evaluando las boletas')
            pago = Payment.objects.get(numero_referencia=boleta.referencia)
            

            if not pago :
                print('No hay registro, para la comparacion en bancos')
                return f'No hay registro, para la comparacion en bancos'
            
            if pago.estado_transaccion == 'COMPLETADO':
                print('La boleta ya fue comprobada')
                return f'La boleta ya fue comprobada'
            cambiar_estado = False
                        
                        
                        # Verifica y actualiza el monto del pago
            if pago.monto != boleta.credito:
                pago.monto = boleta.credito
                        
            elif pago.monto != boleta.debito:
                pago.monto = boleta.debito

                        
                        
            if pago.fecha_emision.date() != boleta.fecha:
                cambiar_estado = True
                pago.fecha_emision = boleta.fecha
                        
                        

            # Si se ha modificado el monto o la fecha, guarda el pago
            if cambiar_estado or (pago.monto != boleta.credito or pago.monto != boleta.debito):
                pago.save()

            # Si la transacción está pendiente, se realiza el pago
            if pago.estado_transaccion == 'PENDIENTE' or pago.estado_transaccion == 'Pendiente':
                ingreso = Income.objects.get(numero_referencia=boleta.referencia)
                egreso = Egress.objects.get(numero_referencia=boleta.referencia)

                if ingreso:
                    ingreso.status = True
                    ingreso.save()
                
                if egreso:
                    egreso.status = True
                    egreso.save()
                
                pago.estado_transaccion = 'COMPLETADO'
                boleta.status = True
                boleta.save()
                pago.save()
                            
                if pago.credit or pago.disbursement or pago.cliente or pago.acreedor or pago.seguro:
                    realizar_pago(pago)
    except Exception as e:
        print(f'Error: {e}')
       