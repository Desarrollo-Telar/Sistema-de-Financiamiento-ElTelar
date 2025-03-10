from apps.financings.functions import realizar_pago
# MODELOS
from apps.financings.models import Payment, Banco
from apps.accountings.models import Income, Egress
from django.shortcuts import get_object_or_404
from datetime import datetime

def generar():
    try:
    
        print('Validando las boletas con bancos')
        boletas = Banco.objects.all()
        
        if not boletas:
            print('No hay comprobacion')
            return
        
        for boleta in boletas:
            print('Se estaran evaluando las boletas')
            
            pago = Payment.objects.filter(numero_referencia=boleta.referencia).first()
            if not pago:
                continue
            
            if pago.estado_transaccion == 'COMPLETADO':
                continue
            cambiar_estado = False
            cambia = False

            if pago.monto == boleta.credito or pago.monto == boleta.debito:
                print('No hay cambios')

            elif pago.monto != boleta.credito:
                pago.monto = boleta.credito
                cambia = True
                pago.save()
                        
            elif pago.monto != boleta.debito:
                pago.monto = boleta.debito
                cambia = True
                pago.save()
            

            
            if pago.fecha_emision.date() != boleta.fecha:
                cambiar_estado = True
                pago.fecha_emision = boleta.fecha
                pago.save()

            

            if pago.estado_transaccion == 'PENDIENTE' or pago.estado_transaccion == 'Pendiente':
                
                ingreso = Income.objects.filter(numero_referencia=boleta.referencia).first()
                egreso = Egress.objects.filter(numero_referencia=boleta.referencia).first()

                if ingreso:
                    ingreso.status = True
                    ingreso.save()
                    pago.estado_transaccion = 'COMPLETADO'
                    
                
                if egreso:
                    egreso.status = True
                    egreso.save()
                    pago.estado_transaccion = 'COMPLETADO'

                if pago.tipo_pago == "EGRESO" or pago.tipo_pago == "INGRESO": 
                    pago.estado_transaccion = "COMPLETADO"
                
                
                #pago.estado_transaccion = 'COMPLETADO'
                #boleta.status = True
                boleta.save()
                pago.save()

                     
                if pago.credit or pago.disbursement or pago.cliente or pago.acreedor or pago.seguro:

                    print('procesando al estado de cuenta')
                    print(boleta.referencia)
                    realizar_pago(pago)
            
                

            

            
    except Exception as e:
        print(f'Error en funciones: {e}')
       