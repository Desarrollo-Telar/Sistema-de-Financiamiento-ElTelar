from django.db import models

# DIAS
from datetime import datetime
from dateutil.relativedelta import relativedelta


# DECIMAL
from decimal import Decimal


# MODELOS
from .credit import Credit

# FORMATO
from apps.financings.formato import formatear_numero

class Cuota(models.Model):
    mes = models.IntegerField('No.Mes',blank=True, null=True,default=1)  
    start_date = models.DateTimeField('Fecha de Inicio') # obligatorio
    due_date = models.DateTimeField('Fecha de Vencimiento',blank=True,null=True)
    outstanding_balance = models.DecimalField('Monto Prestado', max_digits=12, decimal_places=2, default=0) 
    mora = models.DecimalField('Mora', max_digits=12, decimal_places=2, default=0)
    interest = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    principal = models.DecimalField('Capital',max_digits=12, decimal_places=2, default=0)
    installment = models.DecimalField('Cuota',max_digits=12, decimal_places=2, default=0)
    status = models.BooleanField(default=False)
    credit_id = models.ForeignKey(Credit, on_delete=models.CASCADE)
    # NUEVOS CAMPOS
    saldo_pendiente = models.DecimalField('Saldo Pendiente',max_digits=12, decimal_places=2, default=0) # obligatorio
    interes_pagado = models.DecimalField('Interes Pagado',max_digits=12, decimal_places=2, default=0)
    mora_pagado = models.DecimalField('Mora Pagada', max_digits=12, decimal_places=2, default=0)
    fecha_limite = models.DateTimeField('Fecha de Limite',blank=True,null=True)
    cambios = models.BooleanField(default=False)
    numero_referencia = models.CharField('Numero de Referencia', max_length=255, null=True, blank=True, default="NAN")
    cuota_vencida = models.BooleanField(default=False)

    def formato_cuota_mora(self):
        return formatear_numero(self.mora)

    def formato_cuota_interes(self):
        return formatear_numero(self.interest)
    
    def formato_cuota_capital(self):
        return formatear_numero(self.calculo_capital())
    
    def formato_cuota_total(self):
        return formatear_numero(self.total())
    
    def formato_cuota_saldo_pendiente(self):
        return formatear_numero(self.saldo_pendiente)
   
    def no_mes(self):
        contar = 0
        planes = PaymentPlan.objects.filter(credit_id=self.credit_id)
        if planes:
            for plan in planes:
                contar +=1
            self.mes = contar + 1

        else:
            self.mes = 1
        return self.mes
    
   

    def calculo_interes(self):
        interes = (self.saldo_pendiente * self.credit_id.tasa_interes)
        si = round(interes,2)
        return si

    def acumulacion_interes(self):
        interes = 12

    def fecha_vencimiento(self):
        self.due_date =  self.start_date + relativedelta(months=1)
        return self.due_date
    
    def calculo_fecha_limite(self):
        #fecha_inicio = datetime.strptime(self.start_date)
        self.fecha_limite = self.start_date + relativedelta(months=1, days=16)
        return self.fecha_limite
    
    def acumulacion_mora(self):
        self.mora_acumulada -= self.mora_pagado
        return round(self.mora_acumulada,2)
    
    def mostrar_fecha_limite(self):
        limite = self.fecha_limite - relativedelta(days=1)
        limite = self.fecha_limite.replace(hour=5, minute=59, second=0, microsecond=0)
        return limite
    
    def total(self):
        total = 0
        capital = Decimal(self.calculo_capital())
        interes = Decimal(self.interest)
        mora = Decimal(self.mora)
        total = interes + mora + capital
        return round(total,2)
    
    
    
    def calculo_capital(self):
        forma_pago = self.credit_id.forma_de_pago
        monto_inicial = Decimal(self.credit_id.monto)
        plazo = self.credit_id.plazo
        intereses = Decimal(self.interest)
        capital = 0

        

        if forma_pago == 'NIVELADA':
            cuota = Decimal(self.calculo_cuota())  # Solo llamamos una vez
            if intereses >= cuota:
                intereses = self.calculo_interes()

            #intereses -= self.calculo_interes()
            # Capital es la diferencia entre la cuota y los intereses
            capital = round(cuota - self.calculo_interes(), 2)
             
        else:
            # En el caso de amortización a capital, capital es fijo
            capital =  round(monto_inicial / plazo, 2)

        if self.principal > 0:
            capital = 0
        
        
        return Decimal(capital)

    def calculo_cuota(self):
        forma_pago = self.credit_id.forma_de_pago
        tasa_interes = Decimal(self.credit_id.tasa_interes)   # Aseguramos que sea decimal
        plazo = self.credit_id.plazo
        monto = Decimal(self.credit_id.monto)

        if forma_pago == 'NIVELADA':
            # Cálculo de la cuota nivelada basado en la fórmula de cuota fija
            default_interes = tasa_interes  # Asumiendo tasa mensual
            parte1 = (1 + default_interes) ** plazo * default_interes
            parte2 = (1 + default_interes) ** plazo - 1
            cuota = (monto * parte1) / parte2
        else:
            # En el caso de amortización a capital, no llamamos a calculo_capital aquí
            # Capital y cuota se calculan de forma separada
            capital = round(monto / plazo, 2)
            cuota = Decimal(self.interest) + capital

        return round(cuota, 2)

    
    
   
    def save(self,*args, **kwargs):
        self.fecha_vencimiento()
        self.calculo_fecha_limite()
        self.principal = self.calculo_capital()
        self.installment = self.calculo_cuota()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'CREDITO: {self.credit_id} FECHA INICIO: {self.start_date.strftime('%Y-%m-%d')} FECHA LIMITE: {self.fecha_limite.strftime('%Y-%m-%d')}'
        
    class Meta:
        verbose_name = 'Cuota'
        verbose_name_plural = 'Cuotas'