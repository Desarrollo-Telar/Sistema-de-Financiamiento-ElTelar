from django.db import models
from apps.customers.models import Customer
from apps.InvestmentPlan.models import InvestmentPlan

# Clases
from apps.financings.clases.credit import Credit as Credito
from apps.financings.clases.paymentplan import PaymentPlan as PlanPago

# Signals
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone

# DIAS
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.utils import timezone

# DECIMAL
from decimal import Decimal

# CALCULOS
from apps.financings.calculos import calculo_mora


from django.shortcuts import render, get_object_or_404, redirect
# Create your models here.
# CREDITO
class Credit(models.Model):
    formaPago = [
        ('NIVELADA', 'NIVELADA'),
        ('AMORTIZACIONES A CAPITAL', 'AMORTIZACIONES A CAPITAL')
    ]
    frecuenciaPago = [
        ('MENSUAL', 'MENSUAL'),
        ('TRIMESTRAL', 'TRIMESTRAL'),
        ('SEMANAL', 'SEMANAL')
    ]
    credit_type = [
        ('AGROPECUARIO Y/O PRODUCTIVO', 'AGROPECUARIO Y/O PRODUCTIVO'),
        ('COMERCIO', 'COMERCIO'),
        ('SERVICIOS', 'SERVICIOS'),
        ('CONSUMO', 'CONSUMO'),
        ('VIVIENDA', 'VIVIENDA')
    ]
    proposito = models.TextField("Proposito", blank=False, null=False)
    monto = models.DecimalField("Monto", decimal_places=2, max_digits=15, blank=False, null=False)
    plazo = models.IntegerField("Plazo", blank=False, null=False)
    tasa_interes = models.DecimalField("Tasa de Interes", max_digits=5, decimal_places=2, null=False, blank=False)
    forma_de_pago = models.CharField("Forma de Pago", choices=formaPago, max_length=75, blank=False, null=False, default='NIVELADA')
    frecuencia_pago = models.CharField("Frecuencia de Pago", choices=frecuenciaPago, max_length=75, blank=False, null=False, default='MENSUAL')
    fecha_inicio = models.DateField("Fecha de Inicio", blank=False, null=False)
    fecha_vencimiento = models.DateField("Fecha de Vencimiento", blank=False, null=False)
    tipo_credito = models.CharField("Tipo de Credito", choices=credit_type, max_length=75, blank=False, null=False)
    codigo_credito = models.CharField("Codigo Credito", max_length=25, blank=True, null=True)
    destino_id = models.ForeignKey(InvestmentPlan, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Destino')
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Cliente')
    creation_date = models.DateTimeField("Fecha de Creación", auto_now_add=True)
    is_paid_off = models.BooleanField(default=False)
    # NUEVOS ATRIBUTOS
    tasa_mora = models.DecimalField("Tasa de Morosidad", decimal_places=2, max_digits=15, default=0.1)
    saldo_pendiente = models.DecimalField("Saldo Pendiente", decimal_places=2, max_digits=15, default=0)
    saldo_actual = models.DecimalField("Saldo Actual", decimal_places=2, max_digits=15, default=0)


    def __str__(self):
        return self.codigo_credito
    
    def tasa_interes_c(self):

        tasa = float(self.tasa_interes)

        if tasa > 1:
            return (self.tasa_interes / 12)/100
        return (self.tasa_interes/12)


    
    def tasa_mensual(self):
        return self.tasa_interes

    class Meta:
        verbose_name = "Credito"
        verbose_name_plural = "Creditos"

# DESEMBOLSO
class Disbursement(models.Model):
    formaDesembolso = [
        ('APLICACIÓN GASTOS', 'APLICACIÓN GASTOS'),
        ('APLICACIÓN DE AMPLIACIÓN DE CRÉDITO VIGENTE', 'APLICACIÓN DE AMPLIACIÓN DE CRÉDITO VIGENTE'),
        ('CANCELACIÓN DE CRÉDITO VIGENTE', 'CANCELACIÓN DE CRÉDITO VIGENTE')
    ]
    credit_id = models.ForeignKey(Credit, on_delete=models.CASCADE, verbose_name='Credito')
    forma_desembolso = models.CharField("Forma de Desembolso", choices=formaDesembolso, max_length=75, blank=False, null=False)
    monto_credito = models.DecimalField("Monto Credito", decimal_places=2, max_digits=15, default=0)
    saldo_anterior = models.DecimalField("Saldo Anterior", decimal_places=2, max_digits=15, default=0)
    honorarios = models.DecimalField("Honorarios", decimal_places=2, max_digits=15, default=0)
    poliza_seguro = models.DecimalField("Poliza de Seguro", decimal_places=2, max_digits=15, default=0)
    monto_total_desembolso = models.DecimalField("Monto Total a Desembolsar", decimal_places=2, max_digits=15, default=0)

    def save(self, *args, **kwargs):
        self.monto_total_desembolso = self.monto_credito - (self.honorarios + self.poliza_seguro + self.saldo_anterior)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Desembolso"
        verbose_name_plural = "Desembolsos"


# GARANTIA
class Guarantees(models.Model):
    descripcion = models.TextField("Descripcion", blank=False, null=False)
    suma_total = models.DecimalField("Suma Total de Garantia", decimal_places=2, max_digits=15)
    credit_id = models.ForeignKey(Credit, on_delete=models.CASCADE, verbose_name="Credito")

    class Meta:
        verbose_name = 'Garantia'
        verbose_name_plural = 'Garantias'

# DETALLE DE GARANTIA
class DetailsGuarantees(models.Model):
    tipoGarantia = [
        ('HIPOTECA', 'HIPOTECA'),
        ('DERECHO DE POSESION HIPOTECA', 'DERECHO DE POSESION HIPOTECA'),
        ('FIADOR', 'FIADOR'),
        ('CHEQUE', 'CHEQUE'),
        ('VEHICULO', 'VEHICULO'),
        ('MOBILIARIA', 'MOBILIARIA')
    ]
    garantia_id = models.ForeignKey(Guarantees, on_delete=models.CASCADE, verbose_name='Garantia')
    tipo_garantia = models.CharField("Tipo de Garantia", choices=tipoGarantia, max_length=75)
    especificaciones = models.JSONField("Especificaciones")
    valor_cobertura = models.DecimalField("Valor de Cobertura", decimal_places=2, max_digits=15)

    class Meta:
        verbose_name = 'Detalle de Garantia'
        verbose_name_plural = 'Detalles de Garantias'

# PAGOS
class Payment(models.Model):
    STATUS_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('COMPLETADO', 'Completado'),
        ('FALLIDO', 'Fallido'),
    ]
    
    TYPE_PAYMENT = [
        ('DESEMBOLSO','DESEMBOLSO'),('CREDITO','CREDITO')
    ]
    credit = models.ForeignKey(Credit, on_delete=models.CASCADE, verbose_name='Credito')
    monto = models.DecimalField('Monto', max_digits=12, decimal_places=2)
    numero_referencia = models.CharField('Numero de Referencia', max_length=255, unique=True)
    fecha_emision = models.DateTimeField('Fecha de Emision', default=timezone.now)
    fecha_creacion = models.DateTimeField("Fecha de Creación", auto_now_add=True)
    estado_transaccion = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDIENTE')
    descripcion = models.TextField(blank=True, null=True)
    mora = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    interes = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    capital = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    boleta = models.FileField("Boleta",blank=True, null=True,upload_to='pagos/boletas/')
    tipo_pago = models.CharField('Tipo de Pago', choices=TYPE_PAYMENT, max_length=75, default='CREDITO')
    
    def fechaEmision(self):
        return datetime.strftime(self.fecha_emision,'%d/%m/%Y')

    def pago(self):
        return Payment.objects.get(id=self.id)

    def credito(self):
        return Credit.objects.get(id=self.credit.id)

    def _cuota_pagar(self):
        """
        PaymentPlan.objects.filter(credit_id=self.credit).order_by('due_date')
        El resultado será una lista de objetos PaymentPlan correspondientes al crédito especificado, ordenados por la fecha de vencimiento, desde la más cercana hasta la más lejana.
        return PaymentPlan.objects.filter(credit_id=self.credit, status=False).order_by('due_date').first()
        """
        cuotas = PaymentPlan.objects.filter(credit_id=self.credit).order_by('fecha_limite')
        for cuota in cuotas:
            encontrada = False
            fecha_inicio = datetime.strftime(cuota.start_date,'%d/%m/%Y')
            fecha_limite = datetime.strftime(cuota.fecha_limite,'%d/%m/%Y')
            fecha_emision = datetime.strftime(self.fecha_emision,'%d/%m/%Y')

            if fecha_inicio <= fecha_emision <= fecha_limite:
                return cuota 

    def _siguiente_cuota(self):
        cuotas = PaymentPlan.objects.filter(credit_id=self.credit).order_by('fecha_limite')
        cuota_actual = None
        for cuota in cuotas:
            
            fecha_inicio = datetime.strftime(cuota.start_date,'%d/%m/%Y')
            fecha_limite = datetime.strftime(cuota.fecha_limite,'%d/%m/%Y')
            fecha_emision = datetime.strftime(self.fecha_emision,'%d/%m/%Y')

            if fecha_inicio <= fecha_emision <= fecha_limite:
                
                cuota_actual = cuota
                continue

            if cuota_actual:
                return cuota

        return None

    def _calculo_intereses(self):
        interes = self._cuota_pagar().interest
        return interes

    def _calculo_mora(self):
        cuota = self._cuota_pagar()
        return cuota.mora
    
    def _calcular_total(self):
        cuota = self._cuota_pagar()
        total = cuota.interest + cuota.mora
        return round(total)
    
  
    

    def realizar_pago(self):
        print('ESTOY REALIZANDO EL PAGO')
        if self.tipo_pago == 'DESEMBOLSO':
            # registrar en el apartado de desembolso
            pago = self.pago()
            pago.estado_transaccion = 'COMPLETADO'
            pago.save()

            return f'REGISTRO DE DESEMBOLSO'
        
        if self.credito().is_paid_off:
            pago = self.pago()
            pago.estado_transaccion = 'FALLIDO'
            pago.descripcion += f'\n\nEL REGISTRO DE ESTA BOLETA ES INVALIDA DEBIDO A QUE EL CREDITO AL CUAL SE ESTA ASOCIANDO YA HA SIDO CANCELADO\n\n'
            pago.save()
            return f'EL CREDITO YA FUE PAGO'
        

        saldo_pendiente = self.credito().saldo_pendiente
        mora = self._calculo_mora()
        interes = self._calculo_intereses()
        monto_depositado = self.monto

        pagado_mora = 0
        pagado_interes = 0
        aporte_capital = 0

        def procesar_pago(tipo, monto_requerido):
            nonlocal monto_depositado, pagado_mora, pagado_interes

            if monto_depositado >= monto_requerido:
                monto_depositado = round(monto_depositado - monto_requerido, 2)
                
                if tipo == 'Mora':
                    pagado_mora += monto_requerido
                elif tipo == 'Interes':
                    pagado_interes += monto_requerido

                
                
                
                return 0
            else:
                saldo = round(monto_requerido - monto_depositado, 2)
                
                if tipo == 'Mora':
                    pagado_mora += monto_depositado
                elif tipo == 'Interes':
                    pagado_interes += monto_depositado

                monto_depositado = 0    
                return saldo
        
        

        # Procesar pago de mora
        mora = procesar_pago('Mora', mora) 
        if mora > 0:     
            aporte_capital = monto_depositado       
            self._registrar_pago(pagado_mora=pagado_mora, pagado_interes=pagado_interes,aporte_capital=aporte_capital,saldo_pendiente=saldo_pendiente)
                       
            return f"Pago realizado parcialmente. Quedan Q{mora} de mora pendiente. "

       
        # Procesar pago de intereses
        interes = procesar_pago('Interes', interes)
        
        if interes > 0:       
            aporte_capital = monto_depositado
            self._registrar_pago(pagado_mora=pagado_mora, pagado_interes=pagado_interes,aporte_capital=aporte_capital,saldo_pendiente=saldo_pendiente)
            return f"Pago realizado parcialmente. Quedan Q{interes} de intereses pendientes. "
        
        aporte_capital = monto_depositado
        saldo_pendiente -= aporte_capital
        self._registrar_pago(pagado_mora=pagado_mora, pagado_interes=pagado_interes,aporte_capital=aporte_capital,saldo_pendiente=saldo_pendiente)
        return f"Pago realizado con éxito. Q{self.monto} restante. Saldo pendiente total: Q{self.saldo_pendiente}"
    
    def _registrar_pago(self, pagado_mora, pagado_interes,aporte_capital, saldo_pendiente):
        credito = self.credito()
        pago = self.pago()
        cuota = self._cuota_pagar()

        # SE GENERA EL RECIBO
        """
        VERIFICAR SI YA EXISTE UN RECIBO ASOCIADO CON EL PAGO O GENERAR UNO NUEVO
        """
        recibos = Recibo.objects.filter(pago=pago)

        if recibos.exists():
            for recibo in recibos:
                # Actualizamos cada recibo existente
                recibo.mora = cuota.mora
                recibo.interes = cuota.interest
                recibo.pago = pago
                recibo.total = self.monto
                recibo.aporte_capital = aporte_capital
                recibo.interes_pagado = pagado_interes
                recibo.mora_pagada = pagado_mora
                recibo.cliente = credito.customer_id
                recibo.save()
        else:
            # Creamos un nuevo recibo si no hay existentes
            recibo = Recibo(
                mora=cuota.mora,
                interes=cuota.interest,
                pago=pago,
                total=self.monto,
                aporte_capital=aporte_capital,
                interes_pagado=pagado_interes,
                mora_pagada=pagado_mora,
                cliente=credito.customer_id
            )
            recibo.save()

        # ACTUALIZAR LA CUOTA QUE SE ESTA CREANDO 
                            # 500 - 100 = 400
        cuota.interest = cuota.interest - pagado_interes
        cuota.interest -=pagado_interes
        cuota.mora -= pagado_mora
        cuota.saldo_pendiente = saldo_pendiente
        cuota.numero_referencia = self.numero_referencia
        cuota.cambios = False
        cuota.save()

        # ACTUALIZAR EL PAGO PARA REFREGAR LA CANTIDA PAGADA
        pago.mora =  pagado_mora
        pago.interes =  pagado_interes
        pago.capital = aporte_capital
        pago.estado_transaccion = 'COMPLETADO'
        pago.save()

        # REFLEJAR EN EL ESTADO DE CUENTA
        estados_cuenta = AccountStatement.objects.filter(payment=pago)

        # Definimos los datos que se asignarán a los estados de cuenta
        datos_estado_cuenta = {
            'abono': self.monto,
            'credit': credito,
            'payment': pago,
            'interest_paid': pagado_interes,
            'late_fee_paid': pagado_mora,
            'capital_paid': aporte_capital,
            'numero_referencia': self.numero_referencia,
            'description': 'PAGO DE CREDITO'
        }

        if estados_cuenta.exists():
            for estado_cuenta in estados_cuenta:
                # Actualizamos cada estado de cuenta existente
                for key, value in datos_estado_cuenta.items():
                    setattr(estado_cuenta, key, value)
                estado_cuenta.save()
        else:
            # Creamos un nuevo estado de cuenta si no hay existentes
            estado_cuenta = AccountStatement(**datos_estado_cuenta)
            estado_cuenta.save()

        # VERIFICAR SI EL CREDITO YA FUE PAGADO POR COMPLETO
        if saldo_pendiente <= 0:
            
            credito.is_paid_off = True
            credito.saldo_pendiente = 0
            credito.save()

            return f'EL CREDITO PAGADO COMPLETAMENTE'
        
        # SE ACTUALIZA EL SALDO PENDIENTE DEL CREDITO
        credito.saldo_pendiente = saldo_pendiente
        credito.save()


        # GENERAR OTRA CUOTA A PAGAR CUANDO EL MONTO DEPOSITADO ES MAYOR QUE EL TOTAL A PAGAR
        def calculo_interes(saldo_pendiente, tasa_interes):
            # CALCULAR TASA DE INTERES NUEVA
            interes = saldo_pendiente * (tasa_interes )
            return round(interes,2)

        if self.monto >= self._calcular_total():
            interes = calculo_interes(saldo_pendiente, credito.tasa_interes)
            siguiente = self._siguiente_cuota()
            mora = calculo_mora(saldo_pendiente, credito.tasa_interes)

            if siguiente:
                # Actualizamos la siguiente cuota si ya existe
                cuota_a_actualizar = siguiente
                cuota_a_actualizar.cambios = True
                cuota_a_actualizar.interest = max(cuota_a_actualizar.interest,cuota_a_actualizar.interest-interes)
                cuota_a_actualizar.mora = max(cuota_a_actualizar.mora, cuota_a_actualizar.mora - mora)
               
            else:
                # Creamos una nueva cuota si no hay una siguiente
                cuota_a_actualizar = PaymentPlan()
                cuota_a_actualizar.interest = interes

            # Ya sea que sea una cuota nueva o la siguiente existente, actualizamos los campos
            cuota_a_actualizar.start_date = cuota.due_date
            cuota_a_actualizar.saldo_pendiente = saldo_pendiente
            cuota_a_actualizar.credit_id  = credito  
            
            cuota_a_actualizar.outstanding_balance = saldo_pendiente

            # Guardamos los cambios (tanto si es una nueva cuota como si es una cuota existente)
            cuota_a_actualizar.save()


        



    def __str__(self):
        return f'PAGO {self.numero_referencia} - {self.estado_transaccion}'

# PLAN DE PAGOS
class PaymentPlan(models.Model):
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
    interes_acumulado = models.DecimalField('Interes Acumulada',max_digits=12, decimal_places=2, default=0)
    mora_acumulada =  models.DecimalField('Mora Acumulada',max_digits=12, decimal_places=2, default=0)
    interes_acumulado_pagado = models.DecimalField('Interes Acumulado Pagado',max_digits=12, decimal_places=2, default=0)
    mora_acumulado_pagado = models.DecimalField('Mora Acumulado Pagada', max_digits=12, decimal_places=2, default=0)
    fecha_limite = models.DateTimeField('Fecha de Limite',blank=True,null=True)
    cambios = models.BooleanField(default=False)
    numero_referencia = models.CharField('Numero de Referencia', max_length=255, unique=True, null=True, blank=True, default="NAN")
   
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
    
    def calculo_mora(self):
        mora = (self.saldo_pendiente * self.credit_id.tasa_interes ) * self.credit_id.tasa_mora
        
        fecha_actual = datetime.now().date()
         
        if fecha_actual >= self.fecha_limite.strftime('%Y-%m-%d'):
            self.mora = round(mora,2)
        
        return self.mora

    def calculo_interes(self):
        interes = (self.saldo_pendiente * self.credit_id.tasa_interes)
        self.interest = round(interes,2)
        return self.interest

    def acumulacion_interes(self):
        interes = 12

    def fecha_vencimiento(self):
        self.due_date =  self.start_date + relativedelta(months=1)
        return self.due_date
    
    def calculo_fecha_limite(self):
        #fecha_inicio = datetime.strptime(self.start_date)
        self.fecha_limite = self.start_date + relativedelta(months=1, days=15)
        return self.fecha_limite
    
    def acumulacion_mora(self):
        self.mora_acumulada -= self.mora_pagado
        return round(self.mora_acumulada,2)
    
    def total(self):
        total = self.mora + self.interest + self.calculo_capital()
        return round(total,2)
    
    def calculo_cuota(self):
        forma_pago = self.credit_id.forma_de_pago
        tasa_interes = self.credit_id.tasa_interes
        plazo = self.credit_id.plazo
        monto = self.credit_id.monto

        if forma_pago == 'NIVELADA':
            #default_interes = self.interes / 12
            default_interes = tasa_interes
            parte1 = (1 + default_interes) ** plazo * default_interes
            parte2 = (1 + default_interes) ** plazo - 1
            cuota = ((parte1 / parte2) * monto) 
        else:
            cuota = interes + capital
        return round(cuota, 2)
    
    def calculo_capital(self):
        forma_pago = self.credit_id.forma_de_pago
        cuota = self.calculo_cuota()
        monto_inicial = self.credit_id.monto
        plazo = self.credit_id.plazo
        intereses = self.interest

        if forma_pago == 'NIVELADA':
            return round(cuota - intereses, 2)
        else:
            return round(monto_inicial / plazo, 2)
    
    
   
    def save(self,*args, **kwargs):
        #self.calculo_mora()
        self.fecha_vencimiento()
        self.calculo_fecha_limite()
        #self.calculo_interes()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.mes}'
        
    class Meta:
        verbose_name = 'Plan de Pago'
        verbose_name_plural = 'Planes de Pago'

# ESTADOS DE CUENTAS
class AccountStatement(models.Model):
    credit = models.ForeignKey(Credit, on_delete=models.CASCADE, related_name='account_statements')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='account_statement', blank=True, null=True)
    disbursement = models.ForeignKey(Disbursement, on_delete=models.CASCADE, related_name='account_statement', blank=True, null=True)
    issue_date = models.DateField(default=timezone.now)
    disbursement_paid = models.DecimalField('Desembolso Pagado',max_digits=10, decimal_places=2, default=0.0)
    interest_paid = models.DecimalField('Interes Pagado',max_digits=10, decimal_places=2, default=0.0)
    capital_paid = models.DecimalField('Capital Pagada',max_digits=10, decimal_places=2, default=0.0)
    late_fee_paid = models.DecimalField('Mora Pagada',max_digits=10, decimal_places=2, default=0.0)
    saldo_pendiente = models.DecimalField('Saldo Pendiente', max_digits=12, decimal_places=2, default=0)
    abono = models.DecimalField('Abono', max_digits=12, decimal_places=2, default=0)    
    numero_referencia = models.CharField('Numero de Referencia', max_length=255, unique=True)
    description = models.TextField('Descripcion',blank=True, null=True )
    

    class Meta:
        verbose_name = "Estado de Cuenta"
        verbose_name_plural = "Estados de Cuentas"
    
    def fecha_emision(self):
        if self.payment:
            return self.payment.fecha_emision
        return self.issue_date


    def __str__(self):
        return f"Estado de cuenta para crédito {self.credit.id} - Pago {self.payment.numero_referencia}"

# ALERTAS
class Alert(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='Cliente')
    message = models.CharField(max_length=150, blank=True, null=True, verbose_name='Mensaje')

    def __str__(self):
        return f'QUERIDO CLIENTE: {self.customer} LE RECORDAMOS: {self.message}'

    class Meta:
        verbose_name = 'Alerta'
        verbose_name_plural = 'Alertas'

# BANCOS
class Banco(models.Model):
    fecha = models.DateField()
    referencia = models.CharField('No.Referencia',max_length=100, unique=True)
    credito = models.DecimalField('Monto', decimal_places=2, max_digits=12)

    debito = models.DecimalField('Debito', decimal_places=2, max_digits=12, default=0)
    
    def __str__(self):
        return f'Fecha: {self.fecha} Referencia: {self.referencia} Monto: {self.credito}'

    class Meta:
        verbose_name = 'Banco'
        verbose_name_plural = 'Bancos'

# RECIBO
from num2words import num2words
class Recibo(models.Model):
    fecha = models.DateField('Fecha De Recibo',default=timezone.now)
    recibo = models.IntegerField("No. Recibo", default=0)
    cliente = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Customer")
    pago = models.ForeignKey(Payment, on_delete=models.CASCADE, verbose_name="Pago")
    interes = models.DecimalField("Interes",max_digits=12, decimal_places=2, default=0)
    interes_pagado = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    mora = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    mora_pagada = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    aporte_capital = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total  = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    factura = models.BooleanField(default=False)

    def total_letras(self):
        total = num2words(self.total,lang='es')
        return f'{total} Quetzales'
    
    def interes_pagado_letras(self):
        interes = num2words(self.interes_pagado,lang='es')
        return f'{interes} Quetzales'

    def mora_pagada_letras(self):
        mora = num2words(self.mora_pagada,lang='es')
        return f'{mora} Quetzales'
    
    def aporte_capital_letras(self):
        capital = num2words(self.aporte_capital,lang='es')
        return f'{capital} Quetzales'
        



    







