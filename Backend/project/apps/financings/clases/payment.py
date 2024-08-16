"""
    CLASE PARA LA GENERACION DE PAGOS SEGUN EL CREDITO
"""
# FECHA
from datetime import datetime

# 
from .credit import Credit
from .paymentplan import PaymentPlan

from apps.customers.clases.customer import Customer
from apps.InvestmentPlan.clases.investmentPlan import InvestmentPlan


class Payment:
    def __init__(self,monto, fecha_emision,numero_referencia,fecha_creacion=datetime.now(), estado_transaccion=False, descripcion='', plan_id=None):
        self._monto = monto
        self._fecha_emision = fecha_emision
        self._fecha_creacion = fecha_creacion
        self._numero_referencia = numero_referencia
        self._estado_transaccion = estado_transaccion
        self._descripcion = descripcion
        self._plan_id = plan_id
    
    # -------- METODOS GET ------------
    @property
    def monto(self):
        return self._monto
    
    @property
    def fecha_emision(self):
        return self._fecha_emision.strftime('%Y-%m-%d')
    
    @property
    def fecha_creacion(self):
        return self._fecha_creacion.strftime('%Y-%m-%d')
    
    @property
    def numero_referencia(self):
        return self._numero_referencia
    
    @property
    def estado_transaccion(self):
        return self._estado_transaccion
    
    @property
    def descripcion(self):
        return self._descripcion
    
    @property
    def plan_id(self):
        return self._plan_id.credit
    
    #----------------- METODOS SETTER --------------------
    @monto.setter
    def monto(self,value):
        self._monto = value
    
    @fecha_emision.setter
    def fecha_emision(self,value):
        self._fecha_emision = value
    
    @numero_referencia.setter
    def numero_referencia(self,value):
        self._numero_referencia = value
    
    @estado_transaccion.setter
    def estado_transaccion(self,value):
        self._estado_transaccion = value
    
    @descripcion.setter
    def descripcion(self,value):
        self._descripcion = value
    
    @plan_id.setter
    def plan_id(self,value):
        self._plan_id = value
    
    # ------------------ TO STRING -------------------
    def __str__(self):
        return f'PAGO:\n\tMonto: Q{self.monto}\n\tFecha De Emision: {self.fecha_emision}\n\tNumero de Referencia: {self.numero_referencia}\n\tObservacion: {self.descripcion}\n\tEstado: {self.estado_transaccion}\n\tFecha de Registro de Pago: {self.fecha_creacion}'


if __name__ == '__main__':
    fiador = Customer('Juan', 'Lopez', 'lopez@gmail.com', 'DPI', '323846682', '1106369', '42256694', 'RESIDENTE', 'Aprobado', 'MASCULINO', 'AGRONOMO', 'GUATEMALTECA', 'COBAN', '14-03-1995', 'SOLTERO', 'Individual (PI)')
    cliente = Customer('Juan', 'Lopez', 'lopez@gmail.com', 'DPI', '323846682', '1106369', '42256694', 'RESIDENTE', 'Aprobado', 'MASCULINO', 'AGRONOMO', 'GUATEMALTECA', 'COBAN', '14-03-1995', 'SOLTERO', 'Individual (PI)')
    destino = InvestmentPlan('CONSUMO', 1500, 750, 100, cliente)
    credito = Credit(destino.type_of_product_or_service, 117000, 60, 66, 'NIVELADA', 'MENSUAL', '2024-07-17', 'CONSUMO', destino, fiador)
    plan_pago = PaymentPlan(credito)
    pago = Payment(5000,datetime.now(),155485)
    print(pago)


