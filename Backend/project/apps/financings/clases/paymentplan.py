# CLASE PARA VER LOS PLANES DE PAGOS

from .credit import Credit
from apps.customers.clases.customer import Customer
from apps.InvestmentPlan.clases.investmentPlan import InvestmentPlan

class PaymentPlan:
    contador = 0

    def __init__(self, credit_id, fecha_pago=None, monto=None, intereses=None, capital=None, cuota=None):
        PaymentPlan.contador += 1
        self.__no = PaymentPlan.contador
        self.__credit_id = credit_id
        self.__fecha_pago = fecha_pago
        self.__monto = monto
        self.__intereses = intereses
        self.__capital = capital
        self.__estado_pago = self.generar_estado()
        self.__lista = []
        self.__dic = {}
        self.__plazo = int(self.__credit_id.plazo)

    @property
    def plazo(self):
        return self.__plazo

    def generar_estado(self):
        return 'VIGENTE'

    def interes(self):
        return self.__credit_id.tasa_interes

    def formaPago(self):
        return self.__credit_id.forma_de_pago

    def monto_inicial(self):
        return round(self.__credit_id.monto,2)
    
    def calculo_intereses(self,monto):
        intereses = (monto * self.interes()) / 12
        return round(intereses,2)
    
    def calculo_cuota(self):
        default_interes = self.interes() / 12
        parte1 = (1 + default_interes) ** self.__plazo * default_interes
        parte2 = (1 + default_interes) ** self.__plazo - 1
        cuota = (parte1 / parte2) * self.monto_inicial()
        return round(cuota,2)


    def inicial(self):
        intereses = self.calculo_intereses(self.monto_inicial()) 
        cuota = self.calculo_cuota()
        capital = round( cuota - intereses,2)
        dicio = {
            'mes': 1,
            'monto_prestado': round(self.monto_inicial(), 2),
            'intereses': intereses,
            'capital':capital,
            'cuota': cuota,
            
        }
        return dicio

    def generar_plan(self):
        plan = []
        plan.append(self.inicial())
        

        for mes in range(2, self.plazo + 1):
            anterior = plan[mes - 2]
           
            monto_prestado = round(anterior['monto_prestado'] - anterior['capital'],2)
            intereses = self.calculo_intereses(monto_prestado)            
            capital = round( self.calculo_cuota() - intereses,2)

            dicio = {
                'mes':mes,
                'monto_prestado':round(monto_prestado,2),
                'intereses': round(intereses, 2),
                'capital':round(capital,2),
                'cuota':self.calculo_cuota()
            }
            plan.append(dicio)
        return plan
           

            
            

        


if __name__ == '__main__':
    fiador = Customer('Juan', 'Lopez', 'lopez@gmail.com', 'DPI', '323846682', '1106369', '42256694', 'RESIDENTE', 'Aprobado', 'MASCULINO', 'AGRONOMO', 'GUATEMALTECA', 'COBAN', '14-03-1995', 'SOLTERO', 'Indivicual (PI)')
    cliente = Customer('Juan', 'Lopez', 'lopez@gmail.com', 'DPI', '323846682', '1106369', '42256694', 'RESIDENTE', 'Aprobado', 'MASCULINO', 'AGRONOMO', 'GUATEMALTECA', 'COBAN', '14-03-1995', 'SOLTERO', 'Indivicual (PI)')
    destino = InvestmentPlan('CONSUMO', 1500, 750, 100, cliente)
    credito = Credit(destino.type_of_product_or_service, 117000, 60, 66, 'NIVELADA', 'MENSUAL', '2024-07-14', 'CONSUMO', destino, fiador)
    plan_pago = PaymentPlan(credito)
    
    plan = plan_pago.generar_plan()
    for pago in plan:
        print(pago)

   
