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


    def __str__(self):
        return self.codigo_credito

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
        dias_gracia = max(dias_atrasados - 15, 0)
        mora = saldo_pendiente * tasa_mora_diaria * dias_gracia        
        self.mora = round(mora, 2)
        return self.mora
    
    def _cuota_pagar(self):
        return PaymentPlan.objects.filter(credit_id=self.credit, status=False).order_by('due_date').first()
    
    def _calcular_total(self):
        cuota = self._cuota_pagar()
        
        if cuota is None:
            return "No hay pagos pendientes para calcular el total."

       
        dias_total = (cuota.due_date - cuota.start_date).days        

        dias_diferencia = max((self.fecha_emision - cuota.start_date).days, 0)


        dias_atrasados = max((self.fecha_emision - cuota.due_date).days, 0)


        mora = self._calculo_mora(cuota.saldo_pendiente, dias_atrasados - 15) if dias_atrasados > 15 else 0

        fecha_gracia = cuota.due_date + relativedelta(days=15)
        

        if self.fecha_emision > fecha_gracia:  # Corrected condition
            dias_adicionales = dias_total + (dias_atrasados-15)
            total_dias = dias_total + dias_adicionales
            intereses = cuota.interes_acumulado+self._calculo_intereses(dias_adicionales, cuota.saldo_pendiente) - cuota.interes_pagado
        
        elif self.fecha_emision <cuota.due_date :
            
            intereses = cuota.interes_acumulado+self._calculo_intereses(dias_total, cuota.saldo_pendiente) - cuota.interes_pagado
        elif self.fecha_emision >=cuota.due_date or self.fecha_emision <= fecha_gracia:
           intereses = cuota.interes_acumulado+self._calculo_intereses(dias_total, cuota.saldo_pendiente) - cuota.interes_pagado

        total = round(mora + intereses , 2)

        res = {
            'total':total,
            'interes':intereses,
            'mora':mora,
           
        }
        
        return res
    
    def realizar_pago(self):
        total_pagar = self._calcular_total()['total']
        monto_depositado = self.monto
        mora = self._calcular_total()['mora']
        interes = self._calcular_total()['interes']

        # Variables para registrar cuánto se pagó de cada parte
        pagado_mora = 0
        pagado_interes = 0
        pagado_capital = 0
        saldo_pendiente = 0
      
        saldo_pendiente = round(total_pagar-monto_depositado,2)
        

        def procesar_pago(tipo, monto_requerido):
            nonlocal monto_depositado, pagado_mora, pagado_interes, pagado_capital

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
            pagado_capital = monto_depositado
            self.registrar_pago('Mora', pagado_mora,pagado_interes,pagado_capital,self.monto,interes,mora,saldo_pendiente)
            print(f"Pago realizado parcialmente. Quedan Q{mora} de mora pendiente. ")
            return f"Pago realizado parcialmente. Quedan Q{mora} de mora pendiente. "

        # Procesar pago de intereses
        interes = procesar_pago('Interes', interes)
        
        if interes > 0:       
            pagado_capital = monto_depositado     
            self.registrar_pago('Interes', pagado_mora,pagado_interes,pagado_capital,self.monto,interes,mora,saldo_pendiente)
            print(f"Pago realizado parcialmente. Quedan Q{interes} de intereses pendientes. ")
            return f"Pago realizado parcialmente. Quedan Q{interes} de intereses pendientes. "

        

        # Si todo fue pagado completamente
        pagado_capital = monto_depositado
        saldo_pendiente = self._cuota_pagar().saldo_pendiente - pagado_capital
        self.registrar_pago('COMPLETO',pagado_mora,pagado_interes,pagado_capital,self.monto,interes,mora,saldo_pendiente)
        return f"Pago realizado con éxito. Q{monto_depositado} restante."
       

        

    def registrar_pago(self,tipo,pago_mora,pago_interes,pago_capital,monto, interes_acumulado, mora_acumulada,saldo_pendiente=None ):
        cuota = self._cuota_pagar()
        mora = self._calcular_total()['mora']
        interes = self._calcular_total()['interes']
        
        print(f'PAGO DEL CREDITO:\nPAGO MORA: {pago_mora} DE MORA GENERADA: {mora}\nPAGO INTERES: {pago_interes} DE INTERES GENERADO: {interes}\nAPORTACION A CAPITAL: {pago_capital} ')
        

        cuota.interes_pagado = pago_interes
        cuota.mora_pagado = pago_mora
        cuota.saldo_pendiente -= pago_capital
        cuota.interes_acumulado = interes_acumulado
        cuota.mora_acumulada = mora_acumulada

        if self.monto == cuota.installment or self.monto >= cuota.installment:
            cuota.status = True
            cuota.save()
        
            

        # Crear un nuevo estado de cuenta
        estado_cuenta = AccountStatement()
        estado_cuenta.credit = self.credit
        
        # Registrar el tipo de pago
        
        estado_cuenta.late_fee_paid = pago_mora
        
        estado_cuenta.interest_paid = pago_interes
        
        estado_cuenta.capital_paid = pago_capital
        
        estado_cuenta.abono = monto
        
        # Asociar el estado de cuenta con la cuota y el saldo pendiente
        estado_cuenta.saldo_pendiente = saldo_pendiente
        estado_cuenta.numero_referencia = self.numero_referencia
        descrip = f'''
       
        PAGO DEL CREDITO:
        PAGO MORA: Q{pago_mora} DE MORA GENERADA Q{mora}
        PAGO INTERES: Q{pago_interes} DE INTERES GENERADO: Q{interes}
        APORTACION A CAPITAL: Q{pago_capital} '''

        estado_cuenta.description = descrip
        
        # Asociar el pago al estado de cuenta
        pago = Payment.objects.get(id=self.id)   
        estado_cuenta.payment = pago
        pago.estado_transaccion = 'COMPLETADO'
        pago.save()
        
        # Guardar el estado de cuenta
        estado_cuenta.save()

       
        
        
        if cuota.saldo_pendiente > 0:
            # Crear una nueva cuota con el saldo pendiente
            nuevo_fecha_inicio = cuota.due_date
             # Crear una nueva cuota si es necesario
            nuevo_monto = (cuota.outstanding_balance - cuota.principal)
            
           
            plan = PaymentPlan(
                credit_id=self.credit, 
                start_date=nuevo_fecha_inicio, 
                outstanding_balance=nuevo_monto, 
                saldo_pendiente = saldo_pendiente
                
            )
            plan.save()
          
        else:
            # Marcar el crédito como pagado si no hay saldo pendiente
            credito = Credit.objects.get(id=self.credit.id)
            credito.is_paid_off = True
            credito.save()
        

        



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
        
        fecha_actual = datetime.now().strftime('%Y-%m-%d')
         
        if fecha_actual >= self.fecha_limite():
            self.mora = round(mora,2)
        
        return self.mora

    def fecha_vencimiento(self):
        self.due_date = self.start_date + relativedelta(months=1)
        return self.due_date
    
    def fecha_limite(self):
        self.due_date +=   relativedelta(days=15)
        return self.due_date.strftime('%Y-%m-%d')


    def save(self,*args, **kwargs):
        #self.no_mes()
        self.calculo_mora()
        self.fecha_vencimiento()
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
    verificar = models.BooleanField(default=False)

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


