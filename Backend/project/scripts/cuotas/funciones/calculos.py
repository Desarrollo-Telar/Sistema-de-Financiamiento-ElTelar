
# CALCULOS
from apps.financings.calculos import calculo_mora, calculo_interes
from decimal import Decimal

def calcular_interes_y_mora(cuota):

    tasa_interes = 0
    interes = 0
    mora = 0
    saldo_pendiente = cuota.saldo_pendiente

    if cuota.credit_id is not None:
        tasa_interes =  cuota.credit_id.tasa_interes
        forma_pago = cuota.credit_id.forma_de_pago

        if not cuota.status:
            mora = Decimal(cuota.mora) + (Decimal(cuota.interest) * Decimal("0.10")) # Por lo establecido la mora es del 10%
        
        

    
    if cuota.acreedor is not None:
        tasa_interes = cuota.acreedor.tasa
    
    if cuota.seguro is not None:
        tasa_interes = cuota.seguro.tasa
    
    interes = calculo_interes(saldo_pendiente, tasa_interes)

    return interes, mora