

from decimal import Decimal
from dateutil.relativedelta import relativedelta

from .calculos import calculo_interes

from apps.financings.models import PaymentPlan

def procesar_siguiente_cuota(pago, siguiente_cuota, interes,interes_acumulado, mora, dia):
    datos_viejos = {}
    datos_nuevos = {}
    print(f'Interes: {interes}, Saldo Pendiente: {pago.saldo_pendiente}, Interes Acumulado:{interes_acumulado}')
    mes = pago.mes

    if siguiente_cuota is not None:
        

        siguiente_cuota.outstanding_balance = pago.saldo_pendiente
        siguiente_cuota.saldo_pendiente = pago.saldo_pendiente



        if pago.credit_id:
            siguiente_cuota.credit_id = pago.credit_id
            siguiente_cuota.mora = mora 
            siguiente_cuota.interest = interes_acumulado

            fecha_inicio = pago.credit_id.fecha_inicio
            fecha_emision = dia
            fecha_limite = pago.credit_id.fecha_finalizacion_gracia + relativedelta(months=1)
            forma_pago = pago.credit_id.forma_de_pago


            if (
                fecha_limite is not None and
                fecha_inicio <= fecha_emision <= fecha_limite and
                forma_pago == 'INTERES Y CAPITAL AL VENCIMIENTO'
            ):
                tasa_interes =  pago.credit_id.tasa_interes
                tasa = Decimal(tasa_interes) + Decimal (1)
                
                saldo_acumulativo = Decimal(pago.saldo_pendiente) 

                #saldo_acumulativo = Decimal(pago.saldo_pendiente) + Decimal(interes_acumulado)

                
                interes  = calculo_interes(saldo_acumulativo, tasa_interes)
                
                

                if mes > 1: 
                    mora = ( Decimal(interes) * Decimal(mes-1))* Decimal(0.1) 

                    interes_acumulado = (Decimal(interes_acumulado) - mora) 

                mora = ( Decimal(interes) * Decimal(mes))* Decimal(0.1) 

                siguiente_cuota.interest = interes + interes_acumulado + mora


        if pago.seguro:
            siguiente_cuota.seguro = pago.seguro
            siguiente_cuota.interest = interes
        
        if pago.acreedor:
            siguiente_cuota.acreedor = pago.acreedor
            siguiente_cuota.interest = interes

        

        siguiente_cuota.interes_generado =interes
        siguiente_cuota.start_date = pago.due_date
        siguiente_cuota.cambios = True
        siguiente_cuota.save()

        
        

       
        

    else:
        cuota = PaymentPlan()
        cuota.outstanding_balance = pago.saldo_pendiente
        cuota.saldo_pendiente = pago.saldo_pendiente

        if pago.credit_id:
            cuota.credit_id = pago.credit_id
            cuota.interes_generado =interes
            cuota.interest = interes_acumulado
            cuota.mora = mora

            fecha_inicio = pago.credit_id.fecha_inicio
            fecha_emision = dia
            fecha_limite = pago.credit_id.fecha_finalizacion_gracia + relativedelta(months=1)
            forma_pago = pago.credit_id.forma_de_pago


            if (
                fecha_limite is not None and
                fecha_inicio <= fecha_emision <= fecha_limite and
                forma_pago == 'INTERES Y CAPITAL AL VENCIMIENTO'
            ):
                tasa_interes =  pago.credit_id.tasa_interes
                tasa = Decimal(tasa_interes) + Decimal (1)
                
                saldo_acumulativo = Decimal(pago.saldo_pendiente) 

                #saldo_acumulativo = Decimal(pago.saldo_pendiente) + Decimal(interes_acumulado)

                
                interes  = calculo_interes(saldo_acumulativo, tasa_interes)

                if mes > 1: 
                    mora = ( Decimal(interes) * Decimal(mes-1))* Decimal(0.1) 

                    interes_acumulado = (Decimal(interes_acumulado) - mora) 

                mora = ( Decimal(interes) * Decimal(mes))* Decimal(0.1) 

                cuota.interest = interes + interes_acumulado + mora

        if pago.seguro:
            cuota.seguro = pago.seguro
            cuota.interest = interes
        
        if pago.acreedor:
            cuota.acreedor = pago.acreedor
            cuota.interest = interes

        cuota.start_date = pago.due_date
        cuota.save()


def obtener_la_siguiente_cuota(cuota):
    siguiente_cuota = None

    if cuota.credit_id:
        siguiente_cuota = PaymentPlan.objects.filter(
            credit_id=cuota.credit_id,
            fecha_limite__gt=cuota.fecha_limite
            ).order_by('fecha_limite').first()
                

    if cuota.acreedor:
        siguiente_cuota = PaymentPlan.objects.filter(
            acreedor=cuota.acreedor,
            fecha_limite__gt=cuota.fecha_limite
            ).order_by('fecha_limite').first()
                
            
    if cuota.seguro:
        siguiente_cuota = PaymentPlan.objects.filter(
            seguro=cuota.seguro,
            fecha_limite__gt=cuota.fecha_limite
            ).order_by('fecha_limite').first()
                
    return siguiente_cuota