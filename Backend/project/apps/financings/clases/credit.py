from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from apps.customers.clases.Customer import Customer

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
    def proposito(self):
        return self.__proposito
    
    @property
    def monto(self):
        return self.__monto
    
    @property
    def plazo(self):
        return self.__plazo
    
    @property
    def tasa_interes(self):
        return self.__tasa_interes

    @property
    def forma_de_pago(self):
        return self.__forma_de_pago
    
    @property
    def frecuencia_pago(self):
        return self.__frecuencia_pago

    @property
    def fecha_inicio(self):
        return self.__fecha_inicio
    
    @property
    def fecha_vencimiento(self):
        return self.__fecha_vencimiento
    
    @property
    def tipo_credito(self):
        if self.__destino_id:
            self.__tipo_credito = self.__destino_id.type_of_product_or_service

        return self.__tipo_credito
    
    @property
    def destino_id(self):
        return self.__destino_id
    
    @property
    def customer_id(self):
        return self.__customer_id
    
    @proposito.setter
    def proposito(self,value):
        self.__proposito = value
    
    @monto.setter
    def monto(self,value):
        self.__monto = value
    
    @plazo.setter
    def plazo(self, value):
        self.__plazo = value
    
    @tasa_interes.setter
    def tasa_interes(self,value):
        self.__tasa_interes = value
    
    @forma_de_pago.setter
    def forma_de_pago(self,value):
        frecuenciaPago = ['NIVELADA', 'AMORTIZACIONES A CAPITAL']
        if value in frecuenciaPago:
            self.__forma_de_pago = value
        else:
            print("Frecuencia de pago no válida")
           
    @frecuencia_pago.setter
    def frecuencia_pago(self, value):
        frecuenciaPago = ['MENSUAL', 'TRIMESTRAL', 'SEMANAL']
        if value in frecuenciaPago:
            self.__frecuencia_pago = value
        else:
            print("Frecuencia de pago no válida")

    @fecha_inicio.setter
    def fecha_inicio(self, value):
        formato = '%Y-%m-%d'
        try:
            self.__fecha_inicio = datetime.strptime(value, formato)
        except ValueError:
            self.__fecha_inicio = datetime.now()
    
    @fecha_vencimiento.setter
    def fecha_vencimiento(self,value):
        self.__fecha_vencimiento = value
    
    @tipo_credito.setter
    def tipo_credito(self,value):
        tipoCredito = ['AGROPECURIO Y/O PRODUCTIVO','COMERCIO','SERVICIOS','CONSUMO','VIVIENDA']
        if not value in tipoCredito:
            print('Error de tipo de credito')

        self.__tipo_credito = value
    
    @destino_id.setter
    def destino_id(self,value):
        self.__destino_id = value
    
    @customer_id.setter
    def customer_id(self,value):
        self.__customer_id = value

    def calcular_fecha_vencimiento(self):
        fecha_inicio = self.__fecha_inicio
        plazo = self.__plazo
        fecha_vencimiento = fecha_inicio + relativedelta(months=plazo)
        return fecha_vencimiento.strftime('%Y-%m-%d')
