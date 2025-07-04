import json
import sys
import os

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from .credit import Credit
from apps.customers.clases.customer import Customer
from apps.InvestmentPlan.clases.investmentPlan import InvestmentPlan
from .type_guarantee import *


class Guarantee:
    contador = 0
    
    def __init__(self,detalle_garantia, credit_id = None,  descripcion=None):
        Guarantee.contador += 1
        self._count = Guarantee.contador             
        self.__credit_id = credit_id
        self.__description = descripcion
        self.__detalle_garantia = [DetailGuarantee(**dg) for dg in detalle_garantia]
        self.__suma_total = self.calcular_suma_total()
        self.__guarantee = {}
        
    @property
    def credit_id(self):
        return self.__credit_id
    
    @credit_id.setter
    def credit_id(self, credit_id):
        self.__credit_id = credit_id
    
    @property
    def descripcion(self):
        return self.__description
    
    @descripcion.setter
    def descripcion(self, descripcion):
        self.__description = descripcion
    
    @property
    def suma_total(self):
        return self.__suma_total
    
    def calcular_suma_total(self):
        return sum(detalle.valor_cobertura for detalle in self.__detalle_garantia)
    
    def toJSON(self):     
        self.__guarantee['credit_id']=self.__credit_id   
        self.__guarantee['description'] = self.__descripcion
        self.__guarantee['suma_total'] = self.__suma_total
        return json.dumps(self.__guarantee, indent=4)

    def __str__(self):
        resultado = f'Credito ID:\n{self.credit_id},\n\nSuma Total: {self.suma_total}\n\n\n'
        for index, detalle in enumerate(self.__detalle_garantia, start=1):
            resultado += f'  Detalle {index}:\n'
            resultado += f'    Tipo de Garantia: {type(detalle.tipo_garantia).__name__}\n'
            resultado += f'    Valor Cobertura: {detalle.valor_cobertura}\n'
            resultado += f'    Especificaciones: {vars(detalle.tipo_garantia)}\n'
        return resultado


class DetailGuarantee:
    contador = 0

    def __init__(self, tipo_garantia, valor_cobertura=0, especificacion=None):
        DetailGuarantee.contador += 1
        
        self.__tipo_garantia = self.crear_tipo_de_garantia(tipo_garantia, **especificacion)
        self.__valor_cobertura = valor_cobertura
        self._dic = {}

    @property
    def tipo_garantia(self):
        return self.__tipo_garantia

    @property
    def valor_cobertura(self):
        return self.__valor_cobertura

    def crear_tipo_de_garantia(self, tipo_garantia, **kwargs):
        if tipo_garantia == 'Hipoteca' or tipo_garantia == 'HIPOTECA':
            return Hipoteca(**kwargs)
        elif tipo_garantia == 'DERECHO DE POSESIÓN HIPOTECA' or tipo_garantia =='Derecho de posesión hipoteca':
            return DerechoDePosesionHipoteca(**kwargs)
        elif tipo_garantia == 'Fiador':
            return Fiador(**kwargs)
        elif tipo_garantia == 'Cheque':
            return Cheque(**kwargs)
        elif tipo_garantia == 'Vehiculo':
            return Vehiculo(**kwargs)
        elif tipo_garantia == 'Mobiliaria':
            return Mobiliaria(**kwargs)
        else:
            raise ValueError(f"Tipo de garantía desconocido: {tipo_garantia}")

    @property
    def diccionario(self):
        self._dic['tipo_garantia'] = self.__tipo_garantia.diccionario
        return self._dic

    def __str__(self):
        return f'Tipo de Garantía: {type(self.__tipo_garantia).__name__}, Valor de Cobertura: {self.__valor_cobertura}, Especificaciones: {vars(self.__tipo_garantia)}'




if __name__ == '__main__':
    fiador = Customer('Juan', 'Lopez', 'lopez@gmail.com', 'DPI', '323846682', '1106369', '42256694', 'RESIDENTE', 'Aprobado', 'MASCULINO', 'AGRONOMO', 'GUATEMALTECA', 'COBAN', '14-03-1995', 'SOLTERO', 'Indivicual (PI)')
    cliente = Customer('Juan', 'Lopez', 'lopez@gmail.com', 'DPI', '323846682', '1106369', '42256694', 'RESIDENTE', 'Aprobado', 'MASCULINO', 'AGRONOMO', 'GUATEMALTECA', 'COBAN', '14-03-1995', 'SOLTERO', 'Indivicual (PI)') 
    destino = InvestmentPlan('CONSUMO', 1500, 750, 100, cliente)
    credito = Credit(destino.type_of_product_or_service, destino.total_value_of_the_product_or_service, 12, 0.05, 'NIVELADA', 'MENSUAL', '2024-07-14', 'CONSUMO', destino, fiador)
    especificacion = {
        'noEscritura': 125
    }
    
    detalle = [{
        'tipo_garantia': 'HIPOTECA',
        'valor_cobertura': 750,
        'especificacion': especificacion
    },
    
    ]
    garantia = Guarantee(credit_id=credito, detalle_garantia=detalle)
    
    print(garantia)

