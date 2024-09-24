def calculo_interes(saldo_pendiente, tasa_interes):
    interes = saldo_pendiente * tasa_interes 
    return round(interes,2)

def calculo_mora(saldo_pendiente, tasa_interes):
    mora = saldo_pendiente * (tasa_interes) * 0.1
    return round(mora,2)
    
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