import math
import calendar
from datetime import datetime
from dateutil.relativedelta import relativedelta
from decimal import Decimal
from apps.financings.formato import formatear_numero

# Asumo que formatear_numero está importado
# from apps.financings.formato import formatear_numero 

class PaymentPlan:
    contador = 0

    def __init__(self, credit, fecha_inicio_credito=0):
        PaymentPlan.contador += 1
        self.__no = PaymentPlan.contador
        self.__credit = credit
        self.__estado_pago = self.generar_estado()
        self.__plan = []
        self.__plazo = int(self.__credit.plazo)
        self.__plazo_gracia = int(getattr(self.__credit, 'plazo_gracia', 0))
        self._agregar = 0
        self.original_day = fecha_inicio_credito

    @property
    def plazo(self):
        return self.__plazo

    @property
    def plazo_gracia(self):
        return self.__plazo_gracia

    def generar_estado(self):
        return 'VIGENTE'

    @property
    def interes(self):
        # Asegúrate que el modelo Credit devuelva la tasa mensual decimal (ej. 0.10)
        return self.__credit.tasa_interes

    @property
    def forma_pago(self):
        return self.__credit.forma_de_pago

    @property
    def monto_inicial(self):
        return round(Decimal(self.__credit.monto), 2)

    def redondear(self, valor):
        return math.ceil(valor)

    def next_month_preserving_day(self, current_date):
        target_day = self.original_day if self.original_day != 0 else current_date.day
        next_month = current_date + relativedelta(months=1)
        last_day = calendar.monthrange(next_month.year, next_month.month)[1]
        valid_day = min(target_day, last_day)
        return next_month.replace(day=valid_day)

    def calculo_intereses(self, dia=None, monto=None):
        if monto is None:
            monto = self.monto_inicial

        # Si NO usas días, ignóralo
        intereses = Decimal(monto) * Decimal(self.interes)

        return self.redondear(round(intereses, 2))
    
    def calculo_interes_acumulado( self, saldo_capital_pendiente, n):
    # Convertimos a Decimal para precisión financiera
        tasa = Decimal(str(self.interes))
        saldo = Decimal(str(saldo_capital_pendiente))
        interes_acumulado = Decimal('0')
        
        i = 0
        # Cambiamos == por < para que el ciclo funcione
        while i < n:
            # El interés del mes actual sobre el saldo pendiente
            interes_del_mes = saldo * tasa
            interes_acumulado += interes_del_mes
            
            # El saldo aumenta porque el interés se capitaliza
            saldo += interes_del_mes
            
            i += 1
            print(f'MES: {i}, Interés del mes: {interes_del_mes:.2f}, Acumulado: {interes_acumulado:.2f}')
        
        return interes_acumulado

    def calculo_cuota(self, interes=0, capital=0, mes_actual=None):
        cuota = 0
        plazo = self.plazo

        # 👇 si tienes plazo_gracia en tu modelo
        gracia = int(getattr(self.__credit, 'plazo_gracia', 0))

        if self.forma_pago == 'NIVELADA':
            i = self.interes
            if i > 0:
                parte1 = (1 + i) ** plazo * i
                parte2 = (1 + i) ** plazo - 1
                cuota = (parte1 / parte2) * self.monto_inicial
            else:
                cuota = interes + capital

        elif self.forma_pago == 'AMORTIZACIONES A CAPITAL':
            capital = self.calculo_capital(mes_actual=mes_actual)
            cuota = interes + capital

        elif self.forma_pago == 'INTERES MENSUAL Y CAPITAL AL VENCIMIENTO':
            if mes_actual > gracia:
                plazo -= gracia

                capital = self.redondear(round(self.monto_inicial / plazo, 2))

                cuota = interes + capital
            else:
                cuota = interes

        elif self.forma_pago == 'INTERES Y CAPITAL AL VENCIMIENTO':
            if mes_actual > gracia:
                plazo -= gracia

                capital = self.redondear(round(self.monto_inicial / plazo, 2))

                cuota = interes + capital
            else:
                cuota = 0

        calculo = round(cuota + self._agregar, 2)
        return self.redondear(calculo)
    
    def calculo_capital(self, cuota=None, intereses=None, mes_actual=None):
        plazo = self.plazo
        gracia = int(getattr(self.__credit, 'plazo_gracia', 0))

        if self.forma_pago == 'NIVELADA':
            return self.redondear(round(cuota - intereses, 2))

        elif self.forma_pago == 'AMORTIZACIONES A CAPITAL':
            return self.redondear(round(self.monto_inicial / plazo, 2))

        elif self.forma_pago == 'INTERES MENSUAL Y CAPITAL AL VENCIMIENTO':
            if (mes_actual > gracia):
                plazo -= gracia
                return self.redondear(round(self.monto_inicial / plazo, 2))

            else:
                return 0

        elif self.forma_pago == 'INTERES Y CAPITAL AL VENCIMIENTO':
            if (mes_actual > gracia):
                plazo -= gracia
                return self.redondear(round(self.monto_inicial / plazo, 2))

            else:
                return 0

    def inicial(self):
        mes_inicio = self.__credit.fecha_inicio
        if isinstance(mes_inicio, str):
            mes_inicio = datetime.strptime(mes_inicio, '%Y-%m-%d')
        
        mes_fin = self.next_month_preserving_day(mes_inicio)
        
        monto_p = self.monto_inicial
        intereses = self.calculo_intereses(monto_p)
        cuota = self.calculo_cuota(intereses, 0, 1)
        capital = self.calculo_capital(cuota, intereses, 1)

        return {
            'mes': 1,
            'fecha_inicio': mes_inicio,
            'fecha_final': mes_fin,
            'Ffecha_inicio': mes_inicio.date,
            'Ffecha_final': mes_fin.date,
            'monto_prestado': self.monto_inicial,
            'monto_interes': self.monto_inicial,
            'fmonto_prestado': formatear_numero(self.monto_inicial),
            'mora': 0,
            'intereses': self.redondear(intereses) ,
            'fintereses':formatear_numero(intereses),
            'capital': self.redondear( capital),
            'fcapital':formatear_numero(capital),
            'cuota': cuota,
            'fcuota': formatear_numero(cuota),
            'saldo_pendiente': 0,
            'total': cuota,
            'ftotal': formatear_numero(cuota),
            'estado': 'PENDIENTE'
        }

    def generar_plan(self):
        self.__plan.clear()
        primera = self.inicial()
        self.__plan.append(primera)
        gracia = int(getattr(self.__credit, 'plazo_gracia', 0))
        dias = None

        for mes in range(2, self.plazo + 1):
            anterior = self.__plan[-1]

            
            if self.forma_pago == 'INTERES Y CAPITAL AL VENCIMIENTO':
                if (mes > (gracia +1)):
                   monto_prestado = (
                        anterior['monto_prestado'] - anterior['capital']
                    )
                   intereses = self.calculo_intereses(dias, monto_prestado)
                else:
                    monto_prestado = (
                        anterior['monto_interes'] + anterior['intereses']
                    )
                    intereses = self.calculo_interes_acumulado(anterior['monto_prestado'],mes)
                    #intereses = self.calculo_intereses(dias, monto_prestado) + anterior['intereses']

            elif self.forma_pago == 'INTERES MENSUAL Y CAPITAL AL VENCIMIENTO':
                monto_prestado = (
                    anterior['monto_prestado'] - anterior['capital']
                )
                intereses = self.calculo_intereses(dias, monto_prestado)

            else:
                monto_prestado = (
                    anterior['monto_prestado'] - anterior['capital']
                )
                intereses = self.calculo_intereses(dias, monto_prestado)

            mes_inicial = anterior['fecha_final']
            monto_otorgado =  (
                    anterior['monto_prestado'] - anterior['capital']
                )

            if self.original_day != 0:
                mes_final = self.next_month_preserving_day(mes_inicial)
            else:
                mes_final = mes_inicial + relativedelta(months=1)

            dias = (mes_final - mes_inicial).days

            
            cuota = self.calculo_cuota(intereses, None, mes)
            capital = self.calculo_capital(cuota, intereses, mes)

            dicio = {
                'mes': mes,
                'fecha_inicio': mes_inicial,
                'fecha_final': mes_final,
                'Ffecha_inicio': mes_inicial.date,
                'Ffecha_final': mes_final.date,
                'monto_prestado': monto_otorgado,
                'monto_interes':monto_prestado,
                'fmonto_prestado': formatear_numero(monto_otorgado),
                'mora':0,
                'intereses': intereses,
                'fintereses':formatear_numero(intereses),
                'capital': capital,
                'fcapital':formatear_numero(capital),
                'cuota': cuota,
                'fcuota': formatear_numero(cuota),
                'saldo_pendiente':0,
                'total':cuota,
                'ftotal': formatear_numero(cuota),
                'estado':'PENDIENTE'
            }

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