# CLASE PARA VER LOS PLANES DE PAGOS

from .credit import Credit
from apps.customers.clases.customer import Customer
from apps.InvestmentPlan.clases.investmentPlan import InvestmentPlan

class PaymentPlan:
    contador = 0
    def __init__(self,credit_id ,fecha_pago=None,monto=None,intereses=None,capital=None,cuota=None):
        PaymentPlan.contador+=1
        self.__no = PaymentPlan.contador
        self.__credit_id = credit_id
        self.__fecha_pago = fecha_pago 
        self.__monto = monto
        self.__intereses = intereses
        self.__mora = mora
        self.__capital = capital
        self.__estado_pago = self.generar_estado()
    
    def generar_estado(self):
        estados = ['VIGENTE','EN ATRASO']
        return 'VIGENTE'
    
    def plazo(self):
        cantidad_plazo = self.__credit_id.plazo
    
    def interes(self):
        tasa_interes = self.__credit_id.tasa_interes
        

    
    

if __name__ == '__main__':
    fiador = Customer('Juan','Lopez','lopez@gmail.com','DPI','323846682','1106369','42256694','RESIDENTE','Aprobado','MASCULINO','AGRONOMO','GUATEMALTECA','COBAN','14-03-1995','SOLTERO','Indivicual (PI)')
    cliente = Customer('Juan','Lopez','lopez@gmail.com','DPI','323846682','1106369','42256694','RESIDENTE','Aprobado','MASCULINO','AGRONOMO','GUATEMALTECA','COBAN','14-03-1995','SOLTERO','Indivicual (PI)') 
    destino = InvestmentPlan('CONSUMO',1500,750,100,cliente)
    credito = Credit(destino.type_of_product_or_service,destino.total_value_of_the_product_or_service,12,5,'NIVELADA','MENSUAL','2024-07-14','CONSUMO',destino,fiador)
    print(credito.tasa_interes)