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
        self._agregar = 0
    
    

    @property
    def plazo(self):
        return self.__plazo

    def generar_estado(self):
        return 'VIGENTE'
    
    @property
    def credit(self):
        return self.__credit
    
    @credit.setter
    def credit(self,value):
        self.__credit = value

    @property
    def interes(self):
        return self.__credit.tasa_interes

    @property
    def forma_pago(self):
        return self.__credit.forma_de_pago

    @property
    def monto_inicial(self):
        return round(self.__credit.monto, 2)

    def calculo_intereses(self, dia=None,monto=None):
        if monto is None:
            monto = self.monto_inicial
        #intereses = ((monto * self.interes) / 365)*dia
        print(f'{monto} {self.interes}')
        intereses = ((monto * self.interes) )
        return round(intereses, 2)

    def calculo_cuota(self, interes=None, capital=None):
        if self.forma_pago == 'NIVELADA':
            #default_interes = self.interes / 12
            default_interes = self.interes
            parte1 = (1 + default_interes) ** self.plazo * default_interes
            parte2 = (1 + default_interes) ** self.plazo - 1
            cuota = ((parte1 / parte2) * self.monto_inicial) 
        else:
            cuota = interes + capital
        return round(cuota + self._agregar, 2)

    def calculo_capital(self, cuota=None, intereses=None):
        if self.forma_pago == 'NIVELADA':
            return round(cuota - intereses, 2)
        else:
            return round(self.monto_inicial / self.plazo, 2)

    def mes_inicial(self):
        return self.__credit.fecha_inicio

    def inicial(self):
        mes_inicial = self.mes_inicial()  # Esto debería retornar un objeto 'datetime'
        if isinstance(mes_inicial, str):  # Si mes_inicial es un string, lo conviertes
            mes_inicial = datetime.strptime(mes_inicial, '%Y-%m-%d')
        
        mes_final = mes_inicial + relativedelta(months=1)
        dias_diferencia = (mes_final - mes_inicial).days

        dicio = {
            'mes': 1,
            'fecha_inicio': mes_inicial,
            'fecha_final': mes_final,
            'monto_prestado': self.monto_inicial,
            'mora': 0,
        }
        intereses = self.calculo_intereses(dias_diferencia, self.monto_inicial)
        
        if self.forma_pago == 'NIVELADA':
            cuota = self.calculo_cuota()
            capital = self.calculo_capital(cuota, intereses)
        else:
            capital = self.calculo_capital()
            cuota = self.calculo_cuota(intereses, capital)

        dicio.update({
            'intereses': intereses,
            'capital': capital,
            'cuota': cuota,
            'saldo_pendiente': 0,
            'total': cuota,
            'estado': 'PENDIENTE'
        })
        return dicio

    def generar_plan(self):   
        self.__plan.clear()     
        self.__plan.append(self.inicial())
        plan = [self.inicial()]
        
        for mes in range(2, self.plazo + 1):
            anterior = self.__plan[-1]
            monto_prestado = round(anterior['monto_prestado'] - anterior['capital'], 2)
            
            mes_inicial = anterior['fecha_final']
            mes_final = mes_inicial + relativedelta(months=1)
            dias_diferencia = (mes_final - mes_inicial).days

            intereses = self.calculo_intereses(dias_diferencia,monto_prestado)
            #print(f'MES: {anterior['mes']}, Fecha Inicio: {anterior['fecha_inicio'].strftime('%Y-%m-%d')}, Fecha Final: {anterior['fecha_final'].strftime('%Y-%m-%d')}')
            dicio = {
                'mes': mes,
                'fecha_inicio': mes_inicial,
                'fecha_final': mes_final,
                'monto_prestado': monto_prestado,
                'mora':0,
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
                'cuota': cuota,
                'saldo_pendiente':0,
                'total':cuota,
                'estado':'PENDIENTE'
            })
            self.__plan.append(dicio)
        return self.__plan
    
    def recalcular_capital(self):
        total_cap = 0
        total_monto = self.__credit.monto
        plan = self.generar_plan()
        

        for pago in plan:
            total_cap = round(total_cap + pago['capital'],2)
        
        diferencia = round(total_monto - total_cap,2)
        if diferencia > 0:
            promedio = round(diferencia / self.plazo,2)    
            self._agregar = promedio
            self.__plan.clear()
            plan = self.generar_plan()
       

        return self.__plan
    
    def calcular_total_capital(self):
        total_cap = 0
        plan = self.recalcular_capital()      
        for pago in plan:
            total_cap = round(total_cap + pago['capital'],2)
        
        return round(total_cap,2)
    
    def calcular_total_interes(self):
        plan = self.recalcular_capital()
        total_cap = 0
        for pago in plan:
            total_cap = round(total_cap + pago['intereses'],2)

        return round(total_cap,2)
    
    def calcular_total_cuotas(self):
        plan = self.recalcular_capital()
        total_cuotas = 0
        for pago in plan:
           
            total_cuotas += pago['cuota']
           

        return round(total_cuotas,2)





if __name__ == '__main__':
    fiador = Customer('Juan', 'Lopez', 'lopez@gmail.com', 'DPI', '323846682', '1106369', '42256694', 'RESIDENTE', 'Aprobado', 'MASCULINO', 'AGRONOMO', 'GUATEMALTECA', 'COBAN', '14-03-1995', 'SOLTERO', 'Individual (PI)')
    cliente = Customer('Juan', 'Lopez', 'lopez@gmail.com', 'DPI', '323846682', '1106369', '42256694', 'RESIDENTE', 'Aprobado', 'MASCULINO', 'AGRONOMO', 'GUATEMALTECA', 'COBAN', '14-03-1995', 'SOLTERO', 'Individual (PI)')
    destino = InvestmentPlan('CONSUMO', 1500, 750, 100, cliente)
    credito = Credit(destino.type_of_product_or_service, 50000, 36, 0.1, 'NIVELADA', 'MENSUAL', '2024-09-15', 'CONSUMO', destino, fiador)
    plan_pago = PaymentPlan(credito)

    #print(plan_pago.calculo_cuota())
    plan = plan_pago.recalcular_capital()
    print(plan_pago.calcular_total_cuotas())

    #print(plan_pago.calculo_cuota())
    fecha_inicio = datetime.strptime('2024-09-01','%Y-%m-%d')
    fecha_vencimiento = fecha_inicio + relativedelta(months=1)
    fecha_limite = fecha_inicio + relativedelta(months=1, days=15)
    fecha_vencimiento += relativedelta(days=15)

    print(fecha_limite.strftime('%Y-%m-%d'))
    print(datetime.now().date())
   
    


  
    
