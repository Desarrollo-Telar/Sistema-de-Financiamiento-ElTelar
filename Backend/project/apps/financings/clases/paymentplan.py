# CLASE PARA VER LOS PLANES DE PAGOS
from datetime import datetime
from dateutil.relativedelta import relativedelta
from .credit import Credit
from apps.customers.clases.customer import Customer
from apps.InvestmentPlan.clases.investmentPlan import InvestmentPlan

class PaymentPlan:
    contador = 0

    def __init__(self, credit):
        PaymentPlan.contador += 1
        self.__no = PaymentPlan.contador
        self.__credit = credit
        self.__estado_pago = self.generar_estado()
        self.__plan = []
        self.__plazo = int(self.__credit.plazo)

    @property
    def plazo(self):
        return self.__plazo

    def generar_estado(self):
        return 'VIGENTE'

    @property
    def interes(self):
        return self.__credit.tasa_interes

    @property
    def forma_pago(self):
        return self.__credit.forma_de_pago

    @property
    def monto_inicial(self):
        return round(self.__credit.monto, 2)

    def calculo_intereses(self, monto=None):
        if monto is None:
            monto = self.monto_inicial
        intereses = (monto * self.interes) / 12
        return round(intereses, 2)

    def calculo_cuota(self, interes=None, capital=None):
        if self.forma_pago == 'NIVELADA':
            default_interes = self.interes / 12
            parte1 = (1 + default_interes) ** self.plazo * default_interes
            parte2 = (1 + default_interes) ** self.plazo - 1
            cuota = (parte1 / parte2) * self.monto_inicial
        else:
            cuota = interes + capital
        return round(cuota, 2)

    def calculo_capital(self, cuota=None, intereses=None):
        if self.forma_pago == 'NIVELADA':
            return round(cuota - intereses, 2)
        else:
            return round(self.monto_inicial / self.plazo, 2)

    def mes_inicial(self):
        return self.__credit.fecha_inicio

    def inicial(self):
        mes_inicial = self.mes_inicial()
        mes_final = mes_inicial + relativedelta(months=1)
        dicio = {
            'mes': 1,
            'fecha_inicio': mes_inicial,
            'fecha_final': mes_final,
            'monto_prestado': self.monto_inicial
        }
        intereses = self.calculo_intereses(self.monto_inicial)
        if self.forma_pago == 'NIVELADA':
            cuota = self.calculo_cuota()
            capital = self.calculo_capital(cuota, intereses)
        else:
            capital = self.calculo_capital()
            cuota = self.calculo_cuota(intereses, capital)
        dicio.update({
            'intereses': intereses,
            'capital': capital,
            'cuota': cuota
        })
        return dicio

    def generar_plan(self):
        plan = [self.inicial()]
        
        for mes in range(2, self.plazo + 1):
            anterior = plan[-1]
            monto_prestado = round(anterior['monto_prestado'] - anterior['capital'], 2)
            intereses = self.calculo_intereses(monto_prestado)
            mes_inicial = anterior['fecha_final']
            mes_final = mes_inicial + relativedelta(months=1)
            print(f'MES: {anterior['mes']}, Fecha Inicio: {anterior['fecha_inicio'].strftime('%Y-%m-%d')}, Fecha Final: {anterior['fecha_final'].strftime('%Y-%m-%d')}')
            dicio = {
                'mes': mes,
                'fecha_inicio': mes_inicial,
                'fecha_final': mes_final,
                'monto_prestado': monto_prestado,
                'intereses': intereses
            }
            if self.forma_pago == 'NIVELADA':
                cuota = self.calculo_cuota()
                capital = self.calculo_capital(cuota, intereses)
            else:
                capital = round(anterior['capital'], 2)
                cuota = self.calculo_cuota(intereses, capital)
            dicio.update({
                'capital': capital,
                'cuota': cuota
            })
            plan.append(dicio)
        return plan

if __name__ == '__main__':
    fiador = Customer('Juan', 'Lopez', 'lopez@gmail.com', 'DPI', '323846682', '1106369', '42256694', 'RESIDENTE', 'Aprobado', 'MASCULINO', 'AGRONOMO', 'GUATEMALTECA', 'COBAN', '14-03-1995', 'SOLTERO', 'Individual (PI)')
    cliente = Customer('Juan', 'Lopez', 'lopez@gmail.com', 'DPI', '323846682', '1106369', '42256694', 'RESIDENTE', 'Aprobado', 'MASCULINO', 'AGRONOMO', 'GUATEMALTECA', 'COBAN', '14-03-1995', 'SOLTERO', 'Individual (PI)')
    destino = InvestmentPlan('CONSUMO', 1500, 750, 100, cliente)
    credito = Credit(destino.type_of_product_or_service, 117000, 60, 66, 'AMORTIZADA A CAPITAL', 'MENSUAL', '2024-07-17', 'CONSUMO', destino, fiador)
    plan_pago = PaymentPlan(credito)

    plan = plan_pago.generar_plan()
    for pago in plan:
        print(pago)
