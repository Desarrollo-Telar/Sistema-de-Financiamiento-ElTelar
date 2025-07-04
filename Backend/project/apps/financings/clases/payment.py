# TIEMPO
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# CLASES
from .paymentplan import PaymentPlan
from .credit import Credit
from apps.customers.clases.customer import Customer
from apps.InvestmentPlan.clases.investmentPlan import InvestmentPlan


class Payment:
    VALID_TRANSACTION_STATES = ["PENDIENTE", "COMPLETADO", "FALLIDO"]

    def __init__(self, credit, referencia, monto, fecha_emision, estado='PENDIENTE'):
        self.credit = credit
        self.referencia = referencia
        self.monto = monto
        self.fecha_emision = fecha_emision
        self.estado = estado
    
    def saldo_pendiente(self):
        pass
    
    def calculo_interes(self):
        interes = 12



