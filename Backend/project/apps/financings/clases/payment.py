from datetime import datetime, timedelta
from .paymentplan import PaymentPlan
from .credit import Credit
from apps.customers.clases.customer import Customer
from apps.InvestmentPlan.clases.investmentPlan import InvestmentPlan

listado = None
class Payment:
    VALID_TRANSACTION_STATES = ["PENDIENTE", "COMPLETADO", "FALLIDO"]

    def __init__(self, credit, monto, numero_referencia, fecha_emision=None, fecha_creacion=None, estado_transaccion='PENDIENTE', descripcion=''):
        self.monto = monto
        self.fecha_emision = fecha_emision or datetime.now()
        self.fecha_creacion = fecha_creacion or datetime.now()
        self.numero_referencia = numero_referencia
        self.estado_transaccion = estado_transaccion
        self.descripcion = descripcion
        self.credit = credit
        self.plan_de_pagos = listado
        self.pagos_realizados = []
        self.mora = 0
        self.interes = 0
        self.capital = 0
    
    @property
    def monto(self):
        return round(self._monto, 2)
    
    @monto.setter
    def monto(self, value):
        self._monto = value

    @property
    def fecha_emision(self):
        return self._fecha_emision

    @fecha_emision.setter
    def fecha_emision(self, value):
        self._fecha_emision = value

    @property
    def estado_transaccion(self):
        return self._estado_transaccion

    @estado_transaccion.setter
    def estado_transaccion(self, value):
        if value in self.VALID_TRANSACTION_STATES:
            self._estado_transaccion = value
        else:
            raise ValueError("Estado no válido")

    def _calculo_intereses(self, dias=None, monto=None):
        monto = monto or self.credit.monto
        dias = dias or 0
        intereses = ((monto * self.credit.tasa_interes) / 365) * dias
        self.interes = round(intereses, 2)
        return self.interes

    def _calculo_cuota(self, intereses=None, capital=None):
        if self.credit.forma_de_pago == 'NIVELADA':
            tasa_mensual = self.credit.tasa_interes / 12
            factor = (1 + tasa_mensual) ** self.credit.plazo
            cuota = (self.credit.monto * tasa_mensual * factor) / (factor - 1)
        else:
            if intereses is None or capital is None:
                raise ValueError("Intereses y capital deben ser proporcionados para calcular la cuota.")
            cuota = intereses + capital
        return round(cuota, 2)

    def _calculo_capital(self, cuota=None, intereses=None):
        if self.credit.forma_de_pago == 'NIVELADA':
            if cuota is not None and intereses is not None:
                self.capital = round(cuota - intereses, 2)
                if self.capital < 0:
                    dato = self._primer_pago_pendiente()
                    self.capital = dato['capital']

                return self.capital
            else:
                raise ValueError("Cuota e intereses deben ser proporcionados para calcular el capital.")
        else:
            self.capital = round(self.credit.monto / self.credit.plazo, 2)
            return self.capital

    def _calculo_mora(self, saldo_pendiente, dias_atrasados):
        tasa_mora_diaria = self.credit.tasa_interes / 365
        mora = saldo_pendiente * tasa_mora_diaria * dias_atrasados
        self.mora = round(mora, 2)
        return self.mora

    def _primer_pago_pendiente(self):
        return next((pago for pago in self.plan_de_pagos if pago['estado'] == 'PENDIENTE'), None)

    def _calcular_total(self):
        primer_pago = self._primer_pago_pendiente()
        
        if primer_pago is None:
            raise ValueError("No hay pagos pendientes para calcular el total.")

        dias_diferencia = max((self.fecha_emision - primer_pago['fecha_inicio']).days,0)
        dias_atrasados = max((self.fecha_emision - primer_pago['fecha_final']).days, 0)
        
        mora = self._calculo_mora(primer_pago['monto_prestado'], dias_atrasados - 15) if dias_atrasados > 15 else 0
        intereses = self._calculo_intereses(dias_diferencia , primer_pago['monto_prestado'])
        print('DIAS DE DIFERENCIA PARA MORA: ',dias_atrasados-15)
        
        if self.credit.forma_de_pago == 'NIVELADA':
            cuota = self._calculo_cuota(intereses=intereses)
            capital = self._calculo_capital(cuota=cuota, intereses=intereses)
        else:
            capital = self._calculo_capital()
            cuota = self._calculo_cuota(intereses=intereses, capital=capital)
        
        return round(mora + intereses + capital, 2)

    def realizar_pago(self):
        total_pagar = self._calcular_total()
        monto_depositado = self.monto
        saldo_pendiente = 0
        print(''.center(60,'-'))
        print(f'Cobro de Mora: Q {self.mora}')
        print(f'Cobro de Interes: Q {self.interes}')
        print(f'Cobro de Capital: Q {self.capital}')
        print(f'TOTAL A CANCELAR: Q {total_pagar}')
        print(''.center(60,'-'))
        
        def procesar_pago(tipo, monto_requerido):
            nonlocal monto_depositado
            if monto_depositado >= monto_requerido:
                monto_depositado = round(monto_depositado - monto_requerido, 2)
                return 0
            else:
                saldo = round(monto_requerido - monto_depositado, 2)
                monto_depositado = 0
                return saldo

        self.mora = procesar_pago('Mora', self.mora)
        if self.mora > 0:
            self.estado_transaccion = "PENDIENTE"
            self.registrar_pago(self.monto)
            return f"Pago realizado parcialmente. Quedan Q{self.mora} de mora pendiente."
        
        self.interes = procesar_pago('Interes', self.interes)
        
        if self.interes > 0:
            self.estado_transaccion = "PENDIENTE"
            self.registrar_pago(self.monto)
            saldo_pendiente += self.interes
            return f"Pago realizado parcialmente. Quedan Q{self.interes} de intereses pendientes."

        self.capital = procesar_pago('Capital', self.capital)
        
        if self.capital > 0:
            self.credit.monto -= monto_depositado
            self.estado_transaccion = "PENDIENTE"
            self.registrar_pago(self.monto)
            return f"Pago realizado parcialmente. Quedan Q{self.capital} de capital pendiente."

        self.estado_transaccion = "COMPLETADO"
        self.registrar_pago(self.monto)
        return f"Pago realizado con éxito. Q{monto_depositado} restante."
        
    def registrar_pago(self, monto):
        # Actualizar el estado del primer pago pendiente
        primer_pago = self._primer_pago_pendiente()
        if primer_pago:
            primer_pago['estado'] = 'COMPLETADO'
            # Actualizar el estado de las cuotas restantes
            for pago in self.plan_de_pagos:
                if pago['estado'] == 'PENDIENTE' and pago['fecha_inicio'] > primer_pago['fecha_inicio']:
                    pago['monto_prestado'] -= monto
                    if pago['monto_prestado'] <= 0:
                        pago['estado'] = 'COMPLETADO'
                    break
        
        # Registrar el pago realizado
        self.pagos_realizados.append({
            'monto': monto,
            'fecha': self.fecha_emision,
            'estado': self.estado_transaccion
        })
        print(f"Registro de pago: Q {monto}")
        print(''.center(60,'-'))
        print(f'DE LA CUOTA: {primer_pago}')
        print(''.center(60,'-'))

    def __str__(self):
        return (f'PAGO:\n\tMonto: Q{self.monto}\n\tFecha De Emision: {self.fecha_emision}\n'
                f'\tNumero de Referencia: {self.numero_referencia}\n\tObservacion: {self.descripcion}\n'
                f'\tEstado: {self.estado_transaccion}\n\tFecha de Registro de Pago: {self.fecha_creacion}')

if __name__ == '__main__':
    fiador = Customer('Juan', 'Lopez', 'lopez@gmail.com', 'DPI', '323846682', '1106369', '42256694', 'RESIDENTE', 'Aprobado', 'MASCULINO', 'AGRONOMO', 'GUATEMALTECA', 'COBAN', '14-03-1995', 'SOLTERO', 'Individual (PI)')
    cliente = Customer('Juan', 'Lopez', 'lopez@gmail.com', 'DPI', '323846682', '1106369', '42256694', 'RESIDENTE', 'Aprobado', 'MASCULINO', 'AGRONOMO', 'GUATEMALTECA', 'COBAN', '14-03-1995', 'SOLTERO', 'Individual (PI)')
    destino = InvestmentPlan('CONSUMO', 1500, 750, 100, cliente)
    credito = Credit(destino.type_of_product_or_service, 10000, 2, 7.5, 'AMORTIZACION A CAPITAL', 'MENSUAL', '2024-03-15', 'CONSUMO', destino, fiador)
    plan_pago = PaymentPlan(credito)
    
    plan = plan_pago.generar_plan()
    
    listado = plan

    pago1 = Payment(credito, monto=300, numero_referencia='REF001', fecha_emision=datetime.strptime('2024-05-01', '%Y-%m-%d'))
    #pago2 = Payment(credito, monto=401.15, numero_referencia='REF001', fecha_emision=datetime.strptime('2024-10-17', '%Y-%m-%d'))
    resultado_pago = pago1.realizar_pago()
    
    print('RESULTADO DEL PAGO 1: ',resultado_pago)
    #resultado_pago = pago2.realizar_pago()
    
    
    #print('RESULTADO DEL PAGO 2: ',resultado_pago)

""" 
    for pago in listado:
        print(pago)
"""   

    
