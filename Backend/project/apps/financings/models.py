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
            raise ValueError("No hay pagos pendientes para calcular el total.")

       
        dias_total = (cuota.due_date - cuota.start_date).days        

        dias_diferencia = max((self.fecha_emision - cuota.start_date).days, 0)


        dias_atrasados = max((self.fecha_emision - cuota.due_date).days, 0)


        mora = self._calculo_mora(cuota.outstanding_balance, dias_atrasados - 15) if dias_atrasados > 15 else 0

        fecha_gracia = cuota.due_date + relativedelta(days=15)
        

        if self.fecha_emision > fecha_gracia:  # Corrected condition
            dias_adicionales = dias_total + (dias_atrasados-15)
            total_dias = dias_total + dias_adicionales
            intereses = self._calculo_intereses(dias_adicionales, cuota.outstanding_balance)
        
        elif self.fecha_emision <cuota.due_date :
            
            intereses = self._calculo_intereses(dias_diferencia, cuota.outstanding_balance)
        elif self.fecha_emision >=cuota.due_date or self.fecha_emision <= fecha_gracia:
           intereses = self._calculo_intereses(dias_total, cuota.outstanding_balance)

       
        
        if self.credit.forma_de_pago == 'NIVELADA':
            cuota = self._calculo_cuota(intereses=intereses)
            capital = self._calculo_capital(cuota=cuota, intereses=intereses)
        else:
            capital = self._calculo_capital()
            cuota = self._calculo_cuota(intereses=intereses, capital=capital)
        
        return round(mora + intereses + capital, 2)
    
    def realizar_pago(self):
        total_pagar = self._calcular_total()
        monto_depositado = self.monto

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
                elif tipo == 'Capital':
                    pagado_capital += monto_requerido
                
                return 0
            else:
                saldo = round(monto_requerido - monto_depositado, 2)
                
                if tipo == 'Mora':
                    pagado_mora += monto_depositado
                elif tipo == 'Interes':
                    pagado_interes += monto_depositado
                elif tipo == 'Capital':
                    pagado_capital += monto_depositado
                
                monto_depositado = 0    
                return saldo

        # Procesar pago de mora
        self.mora = procesar_pago('Mora', self.mora)
        if self.mora > 0:            
            self.registrar_pago('Mora', pagado_mora,saldo_pendiente)
            print(f"Pago realizado parcialmente. Quedan Q{self.mora} de mora pendiente. ")
            return f"Pago realizado parcialmente. Quedan Q{self.mora} de mora pendiente. "

        # Procesar pago de intereses
        self.interes = procesar_pago('Interes', self.interes)
        if self.interes > 0:            
            self.registrar_pago('Interes', pagado_interes,saldo_pendiente)
            print(f"Pago realizado parcialmente. Quedan Q{self.interes} de intereses pendientes. ")
            return f"Pago realizado parcialmente. Quedan Q{self.interes} de intereses pendientes. "

        # Procesar pago de capital
        self.capital = procesar_pago('Capital', self.capital)
        if self.capital > 0:                      
            self.registrar_pago('Capital', pagado_capital,saldo_pendiente)
            print(f"Pago realizado parcialmente. Quedan Q{self.capital} de capital pendiente.")
            return f"Pago realizado parcialmente. Quedan Q{self.capital} de capital pendiente."

        # Si todo fue pagado completamente
        self.registrar_pago('COMPLETO',self.monto,saldo_pendiente)
        return f"Pago realizado con éxito. Q{monto_depositado} restante."


    def registrar_pago(self,tipo,monto, saldo_pendiente=None):
        cuota = self._cuota_pagar()
        print(monto)
        
        if cuota:
            cuota.status = True  # Marcar la cuota como pagada si el pago cubre todo el saldo pendiente
            cuota.save()  # Guardar la cuota actualizada

        # Crear un nuevo estado de cuenta
        estado_cuenta = AccountStatement()
        estado_cuenta.credit = self.credit
        
        # Registrar el tipo de pago
        if tipo == 'Mora':
            estado_cuenta.late_fee_paid = monto
        elif tipo == 'Interes':
            estado_cuenta.interest_paid = monto
        elif tipo == 'Capital':
            estado_cuenta.capital_paid = monto
        
        estado_cuenta.abono = monto
        
        # Asociar el estado de cuenta con la cuota y el saldo pendiente
        estado_cuenta.saldo_pendiente = saldo_pendiente
        estado_cuenta.numero_referencia = self.numero_referencia
        estado_cuenta.description = 'PAGO DEL CREDITO'
        
        # Asociar el pago al estado de cuenta
        pago = Payment.objects.get(id=self.id)   
        estado_cuenta.payment = pago
        pago.estado_transaccion = 'COMPLETADO'
        pago.save()
        
        # Guardar el estado de cuenta
        estado_cuenta.save()

        # Crear una nueva cuota si es necesario
        nuevo_monto = (cuota.outstanding_balance - cuota.principal) + (saldo_pendiente or 0)
        print('CAPITAL',cuota.principal)
        
        if nuevo_monto > 0:
            # Crear una nueva cuota con el saldo pendiente
            nuevo_fecha_inicio = cuota.due_date
            print(nuevo_fecha_inicio)
            print(nuevo_monto)
            """
            plan = PaymentPlan(
                credit_id=self.credit, 
                start_date=nuevo_fecha_inicio, 
                outstanding_balance=nuevo_monto, 
                
            )
            plan.save()
            """
        else:
            # Marcar el crédito como pagado si no hay saldo pendiente
            credito = Credit.objects.get(id=self.credit.id)
            credito.is_paid_off = True
            credito.save()
        

        



    def __str__(self):
        return f'PAGO {self.numero_referencia} - {self.estado_transaccion}'

# PLAN DE PAGOS
class PaymentPlan(models.Model):
    mes = models.IntegerField('No.Mes',blank=True, null=True)  
    start_date = models.DateTimeField('Fecha de Inicio') # obligatorio
    due_date = models.DateTimeField('Fecha de Vencimiento',blank=True,null=True)
    outstanding_balance = models.DecimalField('Monto Prestado', max_digits=12, decimal_places=2, default=0) # obligatorio
    mora = models.DecimalField('Mora', max_digits=12, decimal_places=2, default=0)
    interest = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    principal = models.DecimalField('Capital',max_digits=12, decimal_places=2, default=0)
    installment = models.DecimalField('Cuota',max_digits=12, decimal_places=2, default=0)
    status = models.BooleanField(default=False)
    credit_id = models.ForeignKey(Credit, on_delete=models.CASCADE)

    def no_mes(self):
        contar = 0
        planes = PaymentPlan.objects.filter(credit_id=self.credit_id)
        if planes:
            for plan in planes:
                contar +=1
            self.mes = contar

        else:
            self.mes = 1
        return self.mes

        

    def fecha_vencimiento(self):
        self.due_date = self.start_date + relativedelta(months=1)
        return self.due_date

    def calculo_interes(self):
        dia = (self.due_date - self.start_date).days
        self.interest = round( ((self.outstanding_balance * self.credit_id.tasa_interes) / 365)*dia,2)

        return round(self.interest,2)
    
    def calculo_cuota(self):
        if self.credit_id.forma_de_pago == 'NIVELADA':
            default_interes = self.credit_id.tasa_interes / 12
            parte1 = (1 + default_interes) ** self.credit_id.plazo * default_interes
            parte2 = (1 + default_interes) ** self.credit_id.plazo - 1
            cuota = (parte1 / parte2) * self.outstanding_balance
            
        else:
            cuota = self.interest + self.principal
        self.installment = round(cuota,2)
        return self.installment 
    
    def calculo_capital(self):
        if self.credit_id.forma_de_pago == 'NIVELADA':
            self.principal = round(self.installment - self.interest, 2)
             
        else:
            self.principal = round(self.credit_id.monto / self.credit_id.plazo, 2)

         
        return self.principal
    
    def save(self,*args, **kwargs):
        self.no_mes()
        self.fecha_vencimiento()
        self.calculo_interes()
        if self.credit_id.forma_de_pago == 'NIVELADA':
            self.calculo_cuota()
            self.calculo_capital()
        else:
            self.calculo_capital()
            self.calculo_cuota()
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
# Señales
@receiver(pre_save, sender=Credit)
def pre_save_credito(sender, instance, **kwargs):
    if not instance.codigo_credito or instance.codigo_credito == '':
        counter = 1
        customer_code = instance.customer_id.customer_code
        credit_code = f'{customer_code} / {counter}'

        while Credit.objects.filter(codigo_credito=credit_code).exists():
            counter += 1
            credit_code = f'{customer_code} / {counter}'

        instance.codigo_credito = credit_code

@receiver(post_save, sender=Credit)
def generar_plan_pagos(sender, instance, created, **kwargs):
    if created:
        plan_pago = PaymentPlan(credit_id=instance,start_date=instance.fecha_inicio, outstanding_balance=instance.monto)
        plan_pago.save()
     

