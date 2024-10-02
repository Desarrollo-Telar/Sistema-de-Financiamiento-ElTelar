from dateutil.relativedelta import relativedelta
from decimal import Decimal

def calculo_interes(saldo_pendiente, tasa_interes):
    # Convertir la tasa de interés a Decimal si no lo es
    tasa_interes_decimal = Decimal(tasa_interes)  # Asegúrate de que tasa_interes sea un float
    interes = saldo_pendiente * tasa_interes_decimal 
    return round(interes, 2)

def calculo_mora(saldo_pendiente, tasa_interes):
    # Convertir la tasa de interés a Decimal si no lo es
    tasa_interes_decimal = Decimal(tasa_interes)  # Asegúrate de que tasa_interes sea un float
    mora = saldo_pendiente * tasa_interes_decimal * Decimal(0.1)
    return round(mora, 2)
    
def calcular_fecha_vencimiento(fecha_inicio):
    # Convertir fecha_inicio a un objeto datetime
    #fecha_inicio = datetime.strptime(fecha_inicio)
    plazo = 1
    # Usar relativedelta para sumar meses al objeto datetime
    fecha_vencimiento = fecha_inicio + relativedelta(months=plazo)
    # Devolver la fecha en formato string
    return fecha_vencimiento

def calcular_fecha_maxima(fecha_inicio):
    
    # Convertir fecha_inicio a un objeto datetime
    #fecha_inicio = datetime.strptime(fecha_inicio)
    plazo = 1
    # Usar relativedelta para sumar meses al objeto datetime
    fecha_limite = fecha_inicio + relativedelta(months=plazo, days= 15)
    # Devolver la fecha en formato string
    return fecha_limite