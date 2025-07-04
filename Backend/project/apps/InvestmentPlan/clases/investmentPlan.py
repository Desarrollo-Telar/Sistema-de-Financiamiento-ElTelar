# CLASE DE DESTINO
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from apps.customers.clases.customer import Customer

class InvestmentPlan:
    contador = 0
    def __init__(self,type_of_product_or_service,total_value_of_the_product_or_service,initial_amount,monthly_amount,customer_id,transfers_or_transfer_of_funds = True,type_of_transfers_or_transfer_of_funds = 'Local',investment_plan_code=None,investment_plan_description=None):
        InvestmentPlan.contador+= 1
        self.__type_of_product_or_service = type_of_product_or_service
        self.__total_value_of_the_product_or_service = total_value_of_the_product_or_service
        self.__investment_plan_description = investment_plan_description
        self.__initial_amount = initial_amount
        self.__monthly_amount = monthly_amount
        self.__transfers_or_transfer_of_funds = transfers_or_transfer_of_funds
        self.__type_of_transfers_or_transfer_of_funds = type_of_transfers_or_transfer_of_funds
        self.__customer_id = customer_id
        self.__investment_plan_code = investment_plan_code  if investment_plan_code else self.codigo_planInversion()
        
        self.id = InvestmentPlan.contador

    @property
    def type_of_product_or_service(self):
        return self.__type_of_product_or_service
    
    @property
    def total_value_of_the_product_or_service(self):
        return self.__total_value_of_the_product_or_service
    
    @property
    def investment_plan_description(self):
        return self.__investment_plan_description
    
    @property
    def initial_amount(self):
        return self.__initial_amount
    
    @property
    def monthly_amount(self):
        return self.__monthly_amount
    
    @property
    def transfers_or_transfer_of_funds(self):
        return self.__transfers_or_transfer_of_funds
    
    @property
    def type_of_transfers_or_transfer_of_funds(self):
        return self.__type_of_transfers_or_transfer_of_funds
    
    @property
    def customer_id(self):
        return self.__customer_id
    
    @property
    def investment_plan_code(self):
        return self.__investment_plan_code
    
    @type_of_product_or_service.setter
    def type_of_product_or_service(self,value):
        tipoCredito = ['AGROPECURIO Y/O PRODUCTIVO','COMERCIO','SERVICIOS','CONSUMO','VIVIENDA']
        if not value in tipoCredito:
            print('Error de tipo de credito')
            
        self.__type_of_product_or_service = value
    
    @total_value_of_the_product_or_service.setter
    def total_value_of_the_product_or_service(self,value):
        self.__total_value_of_the_product_or_service = value
    
    @investment_plan_description.setter
    def investment_plan_description(self,value):
        self.__investment_plan_description = value
    
    @initial_amount.setter
    def initial_amount(self,value):
        self.__initial_amount = value   
    
    @monthly_amount.setter
    def monthly_amount(self,value):
        self.__monthly_amount = value
    
    @transfers_or_transfer_of_funds.setter
    def transfers_or_transfer_of_funds(self,value):
        self.__transfers_or_transfer_of_funds = value
    
    @type_of_transfers_or_transfer_of_funds.setter
    def type_of_transfers_or_transfer_of_funds(self,value):
        self.__type_of_transfers_or_transfer_of_funds = value
    
    @customer_id.setter
    def customer_id(self,value):
        self.__customer_id = value
    

    def codigo_planInversion(self):
        status_suffix = {
            'AGROPECUARIO Y/O PRODUCTIVO': 'A&P',
            'COMERCIO': 'C',
            'SERVICIOS': 'S',
            'CONSUMO': 'C',        
            'VIVIENDA': 'V',
        }
        suffix = status_suffix.get(self.type_of_product_or_service, '')
        resultado = f'{self.__customer_id.codigo_cliente}/{suffix}{InvestmentPlan.contador}'
        return resultado
    
    def __str__(self):
        return f'Plan De Inversion: ID: {self.id},Cliente:{self.__customer_id.codigo_cliente}, codigo_plan_inversion: {self.__investment_plan_code}'


if __name__ == '__main__':    
    cliente = Customer('Juan','Lopez','lopez@gmail.com','DPI','323846682','1106369','42256694','RESIDENTE','Aprobado','MASCULINO','AGRONOMO','GUATEMALTECA','COBAN','14-03-1995','SOLTERO','Indivicual (PI)')
    destino = InvestmentPlan('CONSUMO',1500,750,100,cliente)

    print(destino)

        
        
      
         
        