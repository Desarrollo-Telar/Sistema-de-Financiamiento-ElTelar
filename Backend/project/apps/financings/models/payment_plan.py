from django.db import models

# DIAS
from datetime import datetime
from dateutil.relativedelta import relativedelta
import calendar

# DECIMAL
from decimal import Decimal


# MODELOS
from .credit import Credit
from apps.accountings.models import Creditor, Insurance
from apps.subsidiaries.models import Subsidiary

# FORMATO
from apps.financings.formato import formatear_numero


import math

def redondear( valor):
    return math.ceil(valor)

class PaymentPlan(models.Model):
    mes = models.IntegerField('No.Mes',blank=True, null=True,default=0)  
    start_date = models.DateTimeField('Fecha de Inicio') # obligatorio
    due_date = models.DateTimeField('Fecha de Vencimiento',blank=True,null=True)
    outstanding_balance = models.DecimalField('Monto Prestado', max_digits=12, decimal_places=2, default=0) 
    mora = models.DecimalField('Mora', max_digits=12, decimal_places=2, default=0)
    interest = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    principal = models.DecimalField('Capital',max_digits=12, decimal_places=2, default=0)
    principal_pagado = models.DecimalField('Capital Pagado',max_digits=12, decimal_places=2, default=0)
    installment = models.DecimalField('Cuota',max_digits=12, decimal_places=2, default=0)
    status = models.BooleanField(default=False)

    credit_id = models.ForeignKey(Credit, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Credito')
    acreedor = models.ForeignKey(Creditor, on_delete=models.CASCADE, related_name='payment_plan', blank=True, null=True)
    seguro = models.ForeignKey(Insurance, on_delete=models.CASCADE, related_name='payment_plan', blank=True, null=True)

    saldo_pendiente = models.DecimalField('Saldo Pendiente',max_digits=12, decimal_places=2, default=0) # obligatorio
    interes_pagado = models.DecimalField('Interes Pagado',max_digits=12, decimal_places=2, default=0)
    mora_pagado = models.DecimalField('Mora Pagada', max_digits=12, decimal_places=2, default=0)
    fecha_limite = models.DateTimeField('Fecha de Limite',blank=True,null=True)
    cambios = models.BooleanField(default=False)
    numero_referencia = models.CharField('Numero de Referencia', max_length=255, null=True, blank=True, default="NAN")
    cuota_vencida = models.BooleanField(default=False)
    # NUEVOS CAMPOS
    interes_generado = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    capital_generado = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    interes_acumulado_generado = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    mora_acumulado_generado = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    mora_generado = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    # NUEVOS CAMPOS
    paso_por_task = models.BooleanField(default=False)
    sucursal = models.ForeignKey(Subsidiary, on_delete=models.SET_NULL, blank=True, null=True)
    original_day = models.IntegerField(null=True, blank=True)
    creation_date = models.DateTimeField("Fecha de Creación", auto_now_add=True)


    def limite_cobranza_oficina(self):
        calculo = self.due_date + relativedelta(days=11)
        return calculo.date()   


    def formato_cuota_mora(self):
        return formatear_numero(self.mora)
    
    def formato_cuota_mora_generado(self):
        return formatear_numero(self.mora_generado)
    
    def formato_cuota_mora_acumulado_generado(self):
        return formatear_numero(self.mora_acumulado_generado)

    def formato_cuota_interes(self):
        return formatear_numero(self.interest)
    
    def formato_cuota_interes_generado(self):
        return formatear_numero(self.interes_generado)
    
    def formato_cuota_interes_acumulado_generado(self):
        return formatear_numero(self.interes_acumulado_generado)
    
    def formato_cuota_capital(self):
        return formatear_numero(self.calculo_capital())
    
    def formato_cuota_capital_generado(self):
        return formatear_numero(self.capital_generado)

    def formato_saldo_capital_pendiente(self):
        return formatear_numero(self.outstanding_balance)

    def formato_cuota_total(self):
        calculo = redondear(self.total())
        return formatear_numero(calculo)
    
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
        tasa_interes = 0
        if self.credit_id is not None:
            tasa_interes = self.credit_id.tasa_interes
        
        if  self.acreedor is not None:
            tasa_interes = self.acreedor.tasa
        
        if  self.seguro is not None:
            tasa_interes = self.seguro.tasa

        interes = (Decimal(self.saldo_pendiente) * Decimal(tasa_interes))
        si = round(interes,2)
        return si



    def fecha_vencimiento(self):
        # día objetivo (30 o 31 o el que sea)
        target_day = self.original_day or self.start_date.day  

        # mes siguiente
        next_month = self.start_date + relativedelta(months=1)

        # último día del mes siguiente
        last_day = calendar.monthrange(next_month.year, next_month.month)[1]

        # si el mes no tiene el día original, usa el último día
        valid_day = min(target_day, last_day)

        self.due_date = next_month.replace(day=valid_day)
        return self.due_date
    
    def calculo_fecha_limite(self):
        #fecha_inicio = datetime.strptime(self.start_date)
        if self.credit_id is not None:
            self.fecha_limite = self.start_date + relativedelta(months=1, days=16)
        else:
            self.fecha_limite = self.due_date + relativedelta(days=1)
        return self.fecha_limite
    
    def acumulacion_mora(self):
        self.mora_acumulada -= self.mora_pagado
        return round(self.mora_acumulada,2)
    
    def mostrar_fecha_limite(self):
        limite = self.fecha_limite - relativedelta(days=1)
        limite = self.fecha_limite.replace(hour=5, minute=59, second=0, microsecond=0)
        return limite
    
    def mostrar_fecha_limite_mensaje(self):
        limite = self.fecha_limite - relativedelta(days=1)
        
        return limite
    
    def total(self):
        total = 0
        capital = Decimal(self.calculo_capital())
        interes = Decimal(self.interest)
        mora = Decimal(self.mora)
        total = interes + mora + (capital-self.principal)
        return round(total,2)
    
    def calculo_interes_acumulado(self):
        interes_generado = Decimal(self.calculo_interes())
        interes_vencido = Decimal(self.interest) - interes_generado

        if interes_vencido <= 0:
            interes_vencido = 0

        return Decimal(interes_vencido)
    
    def calculo_interes_actual(self):
        interes_vencido = self.calculo_interes_acumulado()
        interes_generado = Decimal(self.interest)

        interes_actual_cuota = abs(interes_generado - interes_vencido)

        
        return Decimal(interes_actual_cuota)


    
    def calculo_capital(self):
        forma_pago = 'NIVELADA'
        tasa_interes = 0
        plazo = 0
        monto_inicial = 0
        gracia = 0

        if self.credit_id is not None:
            forma_pago = self.credit_id.forma_de_pago
            tasa_interes = Decimal(self.credit_id.tasa_interes)   # Aseguramos que sea decimal
            plazo = self.credit_id.plazo
            monto_inicial = Decimal(self.credit_id.monto)
            gracia = self.credit_id.plazo_gracia
        
        if self.acreedor is not None:
            forma_pago = self.acreedor.forma_de_pago
            tasa_interes = Decimal(self.acreedor.tasa)   # Aseguramos que sea decimal
            plazo = self.acreedor.plazo
            monto_inicial = Decimal(self.acreedor.monto)
        
        if  self.seguro is not None:
            forma_pago = self.seguro.forma_de_pago
            tasa_interes = Decimal(self.seguro.tasa)   # Aseguramos que sea decimal
            plazo = self.seguro.plazo
            monto_inicial = Decimal(self.seguro.monto)
        
      
        capital = Decimal(0)
        es_vencimiento_o_mas = self.mes >= plazo
        capital_nuevo = monto_inicial * (Decimal(1) + tasa_interes) ** gracia
        

        
        if forma_pago == 'NIVELADA':
            intereses = Decimal(self.interes_generado)
            cuota = Decimal(self.calculo_cuota())

            if intereses >= cuota:
                intereses = self.calculo_interes()

            capital = round(cuota - intereses, 2)

        elif forma_pago == 'AMORTIZACIONES A CAPITAL':
            capital = round(monto_inicial / plazo, 2)

        elif forma_pago == 'INTERES MENSUAL Y CAPITAL AL VENCIMIENTO':
            # Solo se paga capital en el último mes
            if es_vencimiento_o_mas:                
                return Decimal(self.saldo_pendiente)
            return Decimal(0)

        elif forma_pago == 'INTERES Y CAPITAL AL VENCIMIENTO':
            # Solo se paga capital en el último mes
            # Si estamos dentro del plazo proyectado (mes <= plazo)
            if self.mes < plazo:
                return Decimal(0) # No hay abono a capital antes del vencimiento
            
            if self.mes == plazo:
                return round(capital_nuevo, 2)
                
            # 3. AJUSTE: Si supera lo proyectado (mes > plazo), se vuelve NIVELADA
            # Aquí calculamos el capital como una cuota nivelada normal sobre el saldo
            intereses = self.calculo_interes()
            cuota_nivelada = self.calculo_cuota()
            return round(cuota_nivelada - intereses, 2)
        
        
        return Decimal(capital)

    def calculo_cuota(self):
        forma_pago = 'NIVELADA'
        tasa_interes = 0
        plazo = 0
        monto = 0
        gracia = 0

        if  self.credit_id is not None:
            forma_pago = self.credit_id.forma_de_pago
            tasa_interes = Decimal(self.credit_id.tasa_interes)   # Aseguramos que sea decimal
            plazo = self.credit_id.plazo
            monto = Decimal(self.credit_id.monto)
            gracia = self.credit_id.plazo_gracia
        
        if  self.acreedor is not None:
            forma_pago = self.acreedor.forma_de_pago
            tasa_interes = Decimal(self.acreedor.tasa)   # Aseguramos que sea decimal
            plazo = self.acreedor.plazo
            monto = Decimal(self.acreedor.monto)
        
        if  self.seguro is not None:
            forma_pago = self.seguro.forma_de_pago
            tasa_interes = Decimal(self.seguro.tasa)   # Aseguramos que sea decimal
            plazo = self.seguro.plazo
            monto = Decimal(self.seguro.monto)
        
        es_vencimiento_o_mas = self.mes >= plazo
        

        if forma_pago == 'NIVELADA':
            # Cálculo de la cuota nivelada basado en la fórmula de cuota fija
            default_interes = tasa_interes  # Asumiendo tasa mensual

            parte1 = (1 + default_interes) ** plazo * default_interes
            parte2 = (1 + default_interes) ** plazo - 1
            cuota = (monto * parte1) / parte2
            return round(cuota, 2)
        
        elif forma_pago == 'AMORTIZACIONES A CAPITAL':
            # En el caso de amortización a capital, no llamamos a calculo_capital aquí
            # Capital y cuota se calculan de forma separada
            capital = round(monto / plazo, 2)
            cuota = Decimal(self.interest) + capital
            return round(cuota, 2)
        
        elif forma_pago == 'INTERES MENSUAL Y CAPITAL AL VENCIMIENTO':
            if self.mes == plazo:
                # Último mes: Interés del mes + Total del Capital
                return round(self.interest + monto, 2)
            else:
                # Meses intermedios: Solo el interés
                return round(self.interest, 2)

        elif forma_pago == 'INTERES Y CAPITAL AL VENCIMIENTO':
            if self.mes < plazo:
                return Decimal(0)
            

            # Caso B: Al vencimiento (Mes 5 en tu ejemplo)
            # cuota = capital_nuevo * ( (i * (1+i)^(n-m)) / ((1+i)^(n-m) - 1) )
            if self.mes == plazo:
                capital_nuevo = monto * (Decimal(1) + tasa_interes) ** gracia
                exponente = plazo - gracia # (n - m)
                
                # Si el exponente es 1, la fórmula se simplifica a: capital_nuevo * (1 + i)
                numerador = tasa_interes * (Decimal(1) + tasa_interes) ** exponente
                denominador = (Decimal(1) + tasa_interes) ** exponente - Decimal(1)
                
                if denominador == 0: # Evitar división por cero
                    return round(capital_nuevo * (Decimal(1) + tasa_interes), 2)
                    
                cuota = capital_nuevo * (numerador / denominador)
                return round(cuota, 2)

            # Caso C: Supera lo proyectado (Mora/Ajuste a Nivelada)
            # Calculamos una cuota nivelada estándar sobre el saldo pendiente actual
            saldo = Decimal(self.saldo_pendiente)
            if tasa_interes > 0:
                # Usamos un plazo remanente ficticio o 1 para cobrar el saldo restante
                return round(saldo * (Decimal(1) + tasa_interes), 2)
            return saldo

        return Decimal(0)

    
    def estado_aportacion(self):
        verificacion = self.capital_generado - self.principal 
        if self.credit_id is not None:

            if verificacion <= 0:
                self.credit_id.estado_aportacion = True
                self.credit_id.save()

        if self.acreedor is not None:
            if verificacion <= 0:
                self.acreedor.estado_aportacion = True
                self.acreedor.save()

        if self.seguro is not None:
            if verificacion <= 0:
                self.seguro.estado_aportacion = True
                self.seguro.save()
            
    def _definir_sucursal(self):
        
        if self.credit_id is not None:
            self.sucursal = self.credit_id.sucursal
            return self.sucursal

        if self.acreedor is not None:
            self.sucursal = self.acreedor.sucursal
            return self.sucursal   
        
        if self.seguro is not None:
            self.sucursal = self.seguro.sucursal
            return self.sucursal 
   
    def save(self,*args, **kwargs):
        es_nuevo = self.pk is None

        self.fecha_vencimiento()
        self.calculo_fecha_limite()

        if es_nuevo:
            self.capital_generado = self.calculo_capital()
            self.installment = self.calculo_cuota()
            self.interes_generado = self.calculo_interes()
            
        self._definir_sucursal()
        super().save(*args, **kwargs)
        self.estado_aportacion()
    
    def __str__(self):
        mensaje = None
        if  self.credit_id is not None:
            mensaje = self.credit_id
        
        if  self.acreedor is not None:
            mensaje = self.acreedor
        
        if  self.seguro is not None:
            mensaje = self.seguro

        return f'{mensaje} - Mes: {self.mes}'
        
    class Meta:
        verbose_name = 'Plan de Pago'
        verbose_name_plural = 'Planes de Pago'