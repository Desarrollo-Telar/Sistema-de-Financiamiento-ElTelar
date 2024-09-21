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
    
    def tasa_mensual(self):
        return self.tasa_interes / 12

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
    numero_referencia = models.CharField('Numero de Referencia', max_length=255)
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
    
    def _calculo_intereses(self):
        monto = self.credit.saldo_pendiente 
        intereses = (monto * self.credit.tasa_interes) 
        self.interes = round(intereses, 2)
        return self.interes

   
    def _calculo_mora(self):
        cuota = self._cuota_pagar()
        return cuota.mora
    
    def _cuota_pagar(self):
        return PaymentPlan.objects.filter(credit_id=self.credit, status=False).order_by('due_date').first()
    
    def credito(self):
        return Credit.objects.get(id=self.credit.id)
    
    def pago(self):
        return Payment.objects.get(id=self.id)

    def realizar_pago(self):
        if self.tipo_pago == 'DESEMBOLSO':
            # registrar en el apartado de desembolso
            return f'REGISTRO DE DESEMBOLSO'
        
        if self.credito().is_paid_off:
            return f'EL CREDITO YA FUE PAGO'

        saldo_pendiente = self.credit.saldo_pendiente
        mora_acumulada = self._cuota_pagar().mora_acumulada
        mora = self._calculo_mora()
        interes = self._calculo_intereses()
        interes_acumulado = self._cuota_pagar().interes_acumulado

        monto_depositado = self.monto

        pagado_mora = 0
        pagado_interes = 0
        pagado_acumulado_mora = 0
        pagado_acumulado_interes = 0
        aporte_capital = 0

        def procesar_pago(tipo, monto_requerido):
            nonlocal monto_depositado, pagado_mora, pagado_interes,pagado_acumulado_mora,pagado_acumulado_interes

            if monto_depositado >= monto_requerido:
                monto_depositado = round(monto_depositado - monto_requerido, 2)
                
                if tipo == 'Mora':
                    pagado_mora += monto_requerido
                elif tipo == 'Interes':
                    pagado_interes += monto_requerido
                elif tipo == 'Mora Acumulada':
                    pagado_acumulado_mora += monto_requerido
                elif tipo == 'Interes Acumulado':
                    pagado_acumulado_interes += monto_requerido
                
                
                return 0
            else:
                saldo = round(monto_requerido - monto_depositado, 2)
                
                if tipo == 'Mora':
                    pagado_mora += monto_depositado
                elif tipo == 'Interes':
                    pagado_interes += monto_depositado
                elif tipo == 'Mora Acumulada':
                    pagado_acumulado_mora += monto_depositado
                elif tipo == 'Interes Acumulado':
                    pagado_acumulado_interes += monto_depositado
               
                
                monto_depositado = 0    
                return saldo
        
        # Procesar pago de mora acumulada
        if mora_acumulada > 0:
            mora_acumulada = procesar_pago('Mora Acumulada',mora_acumulada)
            if mora_acumulada > 0:
                aporte_capital = monto_depositado
                return f'Pago realizado parcialmente. Quedan Q{mora_acumulada} de mora acumulada pendiente.'

        # Procesar pago de mora
        mora = procesar_pago('Mora', mora) 
        if mora > 0:     
            aporte_capital = monto_depositado       
                       
            return f"Pago realizado parcialmente. Quedan Q{mora} de mora pendiente. "

        # Procesar pago de interes acumulado
        if interes_acumulado > 0:
            interes_acumulado  = procesar_pago('Interes Acumulado', interes_acumulado)
            if interes_acumulado > 0:
                aporte_capital = monto_depositado
                return f'Pago realizado parcialmente. Quedan Q{interes_acumulado} de interes acumulado pendiente.'
                
        # Procesar pago de intereses
        interes = procesar_pago('Interes', interes)
        
        if interes > 0:       
            aporte_capital = monto_depositado
            
            return f"Pago realizado parcialmente. Quedan Q{interes} de intereses pendientes. "
        
        aporte_capital = monto_depositado
        saldo_pendiente -= aporte_capital
        return f"Pago realizado con éxito. Q{self.monto} restante. Saldo pendiente total: Q{self.saldo_pendiente}"
    
    def _registrar_pago(self, pagado_mora, pagado_acumulado_mora,pagado_interes,pagado_acumulado_interes ,aporte_capital, saldo_pendiente):
        credito = self.credito()
        pago = self.pago()
        cuota = self._cuota_pagar()

        # VERIFICAR SI EL CREDITO YA FUE PAGADO POR COMPLETO
        if saldo_pendiente <= 0:
            
            credito.is_paid_off = True
            credito.saldo_pendiente = 0
            credito.save()

            return f'EL CREDITO PAGADO COMPLETAMENTE'
        
        credito.saldo_pendiente = saldo_pendiente

        credito.save()
        # ACTUALIZAR EL PAGO PARA REFREGAR LA CANTIDA PAGADA
        pago.mora = pagado_acumulado_mora + pagado_mora
        pago.interes = pagado_acumulado_interes + pagado_interes
        pago.capital = aporte_capital
        pago.estado_transaccion = 'COMPLETADO'
        pago.save()

        # REFLEJAR EN EL ESTADO DE CUENTA
        estado_cuenta = AccountStatement()
        estado_cuenta.abono = self.monto
        estado_cuenta.credit = credito
        estado_cuenta.payment = pago
        estado_cuenta.interest_paid = pagado_interes
        estado_cuenta.late_fee_paid = pagado_mora
        estado_cuenta.capital_paid = aporte_capital
        estado_cuenta.numero_referencia = self.numero_referencia
        estado_cuenta.description = 'PAGO DE CREDITO'
        estado_cuenta.save()

        # GENERAR OTRA CUOTA A PAGAR
        if self.monto >= cuota.installment:
            proxima_cuota = PaymentPlan()
            proxima_cuota.start_date = cuota.due_date
            proxima_cuota.saldo_pendiente = saldo_pendiente
            proxima_cuota.save()


                                   # 0                      -       0                     310              -            300 = 10 de acumulado
        cuota.interes_acumulado = (cuota.interes_acumulado - pagado_acumulado_interes)+ (self._calculo_intereses - pagado_interes  )

                                # 0                         15.2          -       
        cuota.mora_acumulada = (cuota.mora_acumulada - pagado_acumulado_mora)+ (self._calculo_mora - pagado_mora)
        cuota.saldo_pendiente = saldo_pendiente
        cuota.save()



    def __str__(self):
        return f'PAGO {self.numero_referencia} - {self.estado_transaccion}'

# PLAN DE PAGOS
class PaymentPlan(models.Model):
    mes = models.IntegerField('No.Mes',blank=True, null=True,default=1)  
    start_date = models.DateTimeField('Fecha de Inicio') # obligatorio
    due_date = models.DateTimeField('Fecha de Vencimiento',blank=True,null=True)
    outstanding_balance = models.DecimalField('Monto Prestado', max_digits=12, decimal_places=2, default=0) # obligatorio
    mora = models.DecimalField('Mora', max_digits=12, decimal_places=2, default=0)
    interest = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    principal = models.DecimalField('Capital',max_digits=12, decimal_places=2, default=0)
    installment = models.DecimalField('Cuota',max_digits=12, decimal_places=2, default=0)
    status = models.BooleanField(default=False)
    credit_id = models.ForeignKey(Credit, on_delete=models.CASCADE)
    # NUEVOS CAMPOS
    saldo_pendiente = models.DecimalField('Saldo Pendiente',max_digits=12, decimal_places=2, default=0)
    interes_pagado = models.DecimalField('Interes Pagado',max_digits=12, decimal_places=2, default=0)
    mora_pagado = models.DecimalField('Mora Pagada', max_digits=12, decimal_places=2, default=0)
    interes_acumulado = models.DecimalField('Interes Acumulada',max_digits=12, decimal_places=2, default=0)
    mora_acumulada =  models.DecimalField('Mora Acumulada',max_digits=12, decimal_places=2, default=0)
    interes_acumulado_pagado = models.DecimalField('Interes Acumulado Pagado',max_digits=12, decimal_places=2, default=0)
    mora_acumulado_pagado = models.DecimalField('Mora Acumulado Pagada', max_digits=12, decimal_places=2, default=0)
    fecha_limite = models.DateTimeField('Fecha de Limite',blank=True,null=True)
   
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
        mora = (self.saldo_pendiente * self.credit_id.tasa_mensual() ) * self.credit_id.tasa_mora
        
        fecha_actual = datetime.now().date()
         
        if fecha_actual >= self.fecha_limite:
            self.mora = round(mora,2)
        
        return self.mora

    def calculo_interes(self):
        interes = (self.saldo_pendiente * self.credit_id.tasa_mensual())
        self.interest = round(interes,2)
        return self.interest

    def acumulacion_interes(self):
        interes = 12

    def fecha_vencimiento(self):
        self.due_date = self.start_date + relativedelta(months=1)
        return self.due_date
    
    def fecha_limite(self):
        fecha_inicio = datetime.strptime(self.start_date,'%Y-%m-%d')
        self.fecha_limite = fecha_inicio + relativedelta(months=1, days=15)
        return self.fecha_limite.strftime('%Y-%m-%d')
    
    def acumulacion_mora(self):
        self.mora_acumulada -= self.mora_pagado
        return round(self.mora_acumulada,2)
    
    

    def save(self,*args, **kwargs):
        #self.no_mes()
        self.calculo_interes()
        self.calculo_mora()
        #self.fecha_vencimiento()
        #self.fecha_limite()
        #self.acumulacion_mora()
        #self.calculo_interes()
        """
        if self.credit_id.forma_de_pago == 'NIVELADA':
            self.calculo_cuota()
            self.calculo_capital()
        else:
            self.calculo_capital()
            self.calculo_cuota()
        """
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.mes}'
        
    class Meta:
        verbose_name = 'Plan de Pago'
        verbose_name_plural = 'Planes de Pago'

# ESTADOS DE CUENTAS
class AccountStatement(models.Model):
    credit = models.ForeignKey('Credit', on_delete=models.CASCADE, related_name='account_statements')
    payment = models.ForeignKey('Payment', on_delete=models.CASCADE, related_name='account_statement')
    issue_date = models.DateField(default=timezone.now)
    disbursement_paid = models.DecimalField('Desembolso Pagado',max_digits=10, decimal_places=2, default=0.0)
    interest_paid = models.DecimalField('Interes Pagado',max_digits=10, decimal_places=2, default=0.0)
    capital_paid = models.DecimalField('Capital Pagada',max_digits=10, decimal_places=2, default=0.0)
    late_fee_paid = models.DecimalField('Mora Pagada',max_digits=10, decimal_places=2, default=0.0)
    saldo_pendiente = models.DecimalField('Saldo Pendiente', max_digits=12, decimal_places=2, default=0)
    abono = models.DecimalField('Abono', max_digits=12, decimal_places=2, default=0)    
    numero_referencia = models.CharField('Numero de Referencia', max_length=255)
    description = models.TextField('Descripcion',blank=True, null=True )
    

    class Meta:
        verbose_name = "Estado de Cuenta"
        verbose_name_plural = "Estados de Cuentas"


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

    def __str__(self):
        return f'Fecha: {self.fecha} Referencia: {self.referencia} Monto: {self.credito}'

    class Meta:
        verbose_name = 'Banco'
        verbose_name_plural = 'Bancos'


