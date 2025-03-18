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
            #print('Se estaran evaluando las boletas')
            
            pago = Payment.objects.filter(numero_referencia=boleta.referencia, estado_transaccion="PENDIENTE").first()
            
            

            if pago is None:
                continue
            

            

            
            cambiar_estado = False

            print(f'EN FUNCIONES DE PAGO - GENERAR:{pago}')
            # Comparar montos
            if pago.monto == boleta.credito or pago.monto == boleta.debito:
                print('No hay cambios en monto')
            else:
                if pago.monto != boleta.credito:
                    pago.monto = boleta.credito
                    cambiar_estado = True

                if pago.monto != boleta.debito:
                    pago.monto = boleta.debito
                    cambiar_estado = True
            

            
            if pago.fecha_emision.date() != boleta.fecha:
                cambiar_estado = True
                pago.fecha_emision = boleta.fecha
                #pago.save()

            

            if pago.estado_transaccion in ["PENDIENTE", "Pendiente"]:
                print("Pendiente")
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
                

                     
                if pago.credit or pago.disbursement or pago.cliente or pago.acreedor or pago.seguro:

                    print('procesando al estado de cuenta')
                    print(boleta.referencia)
                    if cambiar_estado:
                        pago.save()
                    realizar_pago(pago)
            
            

            

            
    except Exception as e:
        print(f'Error en funciones 1: {e}')
       