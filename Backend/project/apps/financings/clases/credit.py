from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from apps.customers.clases.customer import Customer
from apps.InvestmentPlan.clases.investmentPlan import InvestmentPlan



class Credit:
    contador = 0
    def __init__(self, proposito, monto, plazo, tasa_interes, forma_de_pago, frecuencia_pago, fecha_inicio, tipo_credito,  customer_id,destino_id=None, fecha_vencimiento=None):
        Credit.contador+=1
        self._id = Credit.contador
        self.__proposito = 'NADA'
        self.__monto = monto
        self.__plazo = plazo
        self.__tasa_interes = tasa_interes
        self.__forma_de_pago = forma_de_pago
        self.__frecuencia_pago = frecuencia_pago
        self.__fecha_inicio = fecha_inicio
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
        tasa = float(self.__tasa_interes)

        if tasa > 1:
            return (self.__tasa_interes )/100
        return (self.__tasa_interes)

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
            # Asegúrate de que 'value' se convierta correctamente a 'datetime'
            self.__fecha_inicio = datetime.strptime(value, formato) if isinstance(value, str) else value
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
        # Convertir fecha_inicio a un objeto datetime
        fecha_inicio = datetime.strptime(self.__fecha_inicio, '%Y-%m-%d')
        plazo = self.__plazo
        # Usar relativedelta para sumar meses al objeto datetime
        fecha_vencimiento = fecha_inicio + relativedelta(months=plazo)
        # Devolver la fecha en formato string
        return fecha_vencimiento.strftime('%Y-%m-%d')
    
    def toJson(self):
        js = {
            'proposito':self.__proposito,
            'monto':self.__monto,
            'plazo':self.__plazo,
            'tasa_interes':self.__tasa_interes,
            'forma_de_pago':self.__forma_de_pago,
            'frecuecia_pago':self.__frecuencia_pago,
            'fecha_inicio':self.__fecha_inicio,
            'fecha_vencimiento':self.__fecha_vencimiento,
            'tipo_credito':self.__tipo_credito,
            'destino':self.__destino_id,
            'cliente':self.__customer_id,

        }
        return json.dumps(js, indent=4, ensure_ascii=False)
    
    def __str__(self):
        return f'Credito: \nID:{self._id},\nFecha Inicio: {self.fecha_inicio},\nPlazo: {self.__plazo} meses,\nTasa de Interes: {self.__tasa_interes} %\nFecha de Vencimiento: {self.__fecha_vencimiento},\n'

if __name__ == '__main__':
    fiador = Customer('Juan','Lopez','lopez@gmail.com','DPI','323846682','1106369','42256694','RESIDENTE','Aprobado','MASCULINO','AGRONOMO','GUATEMALTECA','COBAN','14-03-1995','SOLTERO','Indivicual (PI)')
    cliente = Customer('Juan','Lopez','lopez@gmail.com','DPI','323846682','1106369','42256694','RESIDENTE','Aprobado','MASCULINO','AGRONOMO','GUATEMALTECA','COBAN','14-03-1995','SOLTERO','Indivicual (PI)') 
    destino = InvestmentPlan('CONSUMO',1500,750,100,cliente)
    credito = Credit(destino.type_of_product_or_service,destino.total_value_of_the_product_or_service,12,0.05,'NIVELADA','MENSUAL','2024-07-14','CONSUMO',destino,fiador)
    print(credito)

