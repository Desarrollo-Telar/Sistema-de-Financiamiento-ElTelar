from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

class Credit:
    def __init__(self, proposito, monto, plazo, tasa_interes, forma_de_pago, frecuencia_pago, fecha_inicio, tipo_credito, destino_id, customer_id, fecha_vencimiento=None):
        self.__proposito = proposito
        self.__monto = monto
        self.__plazo = plazo
        self.__tasa_interes = tasa_interes
        self.__forma_de_pago = forma_de_pago
        self.__frecuencia_pago = frecuencia_pago
        self.__fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        self.__fecha_vencimiento = fecha_vencimiento if fecha_vencimiento else self.calcular_fecha_vencimiento()
        self.__tipo_credito = tipo_credito
        self.__destino_id = destino_id
        self.__customer_id = customer_id

    @property
    def frecuencia_pago(self):
        return self.__frecuencia_pago
    
    @frecuencia_pago.setter
    def frecuencia_pago(self, value):
        frecuenciaPago = ['MENSUAL', 'TRIMESTRAL', 'SEMANAL']
        if value in frecuenciaPago:
            self.__frecuencia_pago = value
        else:
            print("Frecuencia de pago no válida")

    @property
    def plazo(self):
        return self.__plazo
    
    @plazo.setter
    def plazo(self, value):
        self.__plazo = value
    
    @property
    def fecha_inicio(self):
        return self.__fecha_inicio
    
    @fecha_inicio.setter
    def fecha_inicio(self, value):
        formato = '%Y-%m-%d'
        try:
            self.__fecha_inicio = datetime.strptime(value, formato)
        except ValueError:
            self.__fecha_inicio = datetime.now()

    def calcular_fecha_vencimiento(self):
        fecha_inicio = self.__fecha_inicio
        plazo = self.__plazo
        fecha_vencimiento = fecha_inicio + relativedelta(months=plazo)
        return fecha_vencimiento.strftime('%Y-%m-%d')
