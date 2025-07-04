# DECIMAL
from decimal import Decimal

# DAYS
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta

def calcular_interes(saldo_pendiente, tasa_interes, fecha_inicio, fecha_pago, fecha_emision):
    

    dias_transcurridos = (fecha_pago - fecha_inicio).days
    fecha_vencimiento = fecha_inicio + relativedelta(months=1)
    fecha_gracia = fecha_vencimiento + relativedelta(days=15)
    dias_total = (fecha_vencimiento - fecha_inicio).days
    dias_atrasados = max((fecha_emision - fecha_vencimiento).days, 0)
    if fecha_pago > fecha_gracia: 
        dias_adicionales = dias_total + (dias_atrasados-15)
        dias_transcurridos = dias_adicionales

    interes_generado = (saldo_pendiente * tasa_interes / Decimal(365)) * Decimal(dias_transcurridos)
    
    return interes_generado   

def calcular_mora(saldo_pendiente, tasa_interes, fecha_vencimiento, fecha_pago):
    dias_atraso = (fecha_pago - fecha_vencimiento).days - 15
    if dias_atraso > 0:
        mora_generada = (saldo_pendiente * (tasa_interes / Decimal(365))) * Decimal(dias_atraso)
        return mora_generada
    return Decimal(0)   

def calcular_capital(cuota, interes, monto_credito, plazo_credito, forma_pago, capital_plan):
    if forma_pago == "NIVELADA":
        # Si el interés supera la cuota, se toma el capital del plan de pagos
        return cuota - interes if interes < cuota else capital_plan
    elif forma_pago == "AMORTIZACIONES A CAPITAL":
        return monto_credito / plazo_credito
    return Decimal(0)    