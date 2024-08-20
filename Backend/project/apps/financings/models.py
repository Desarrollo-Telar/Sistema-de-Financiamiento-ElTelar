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

# Create your models here.
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

    def __str__(self):
        return self.codigo_credito

    class Meta:
        verbose_name = "Credito"
        verbose_name_plural = "Creditos"

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

class DetalleDesembolso(models.Model):
    desembolso = models.ForeignKey(Disbursement, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=255)
    cantidad = models.IntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)

    def save(self, *args, **kwargs):
        self.total = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Detalle {self.id} - Desembolso {self.desembolso.id}"

class HistorialDesembolso(models.Model):
    desembolso = models.ForeignKey(Disbursement, on_delete=models.CASCADE)
    fecha_cambio = models.DateTimeField(auto_now_add=True)
    descripcion_cambio = models.CharField(max_length=255)

    def __str__(self):
        return f"Historial {self.id} - Desembolso {self.desembolso.id}"

class Guarantees(models.Model):
    descripcion = models.TextField("Descripcion", blank=False, null=False)
    suma_total = models.DecimalField("Suma Total de Garantia", decimal_places=2, max_digits=15)
    credit_id = models.ForeignKey(Credit, on_delete=models.CASCADE, verbose_name="Credito")

    class Meta:
        verbose_name = 'Garantia'
        verbose_name_plural = 'Garantias'

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

class Payment(models.Model):
    STATUS_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('COMPLETADO', 'Completado'),
        ('FALLIDO', 'Fallido'),
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
    


    def dias_atraso(self):
        # Obtener la última fecha de vencimiento del plan de pago
        ultimo_pago = PaymentPlan.objects.filter(credit=self.credit, status=False).order_by('-fecha_final').first()
        if ultimo_pago:
            fecha_vencimiento = ultimo_pago.fecha_final
        else:
            fecha_vencimiento = self.credit.fecha_vencimiento
        
        # Calcular los días de atraso desde la fecha de vencimiento hasta la fecha de emisión del pago
        dias_atraso = (self.fecha_emision.date() - fecha_vencimiento).days
        return max(dias_atraso, 0)

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
            else:
                raise ValueError("Cuota e intereses deben ser proporcionados para calcular el capital.")
        else:
            self.capital = round(self.credit.monto / self.credit.plazo, 2)
        return self.capital

    def _calculo_mora(self, saldo_pendiente, dias_atrasados):
        tasa_mora_diaria = self.credit.tasa_interes / 365
        mora = saldo_pendiente * tasa_mora_diaria * dias_atrasados
        self.mora = round(mora, 2)
        return self.mora

    def _primer_pago_pendiente(self):
        # Obtener el primer plan de pago cuyo estado es False (pendiente)
        primer_pago_pendiente = PaymentPlan.objects.filter(
            credit=self.credit, 
            status=False
        ).order_by('fecha_inicio').first()

        if primer_pago_pendiente:
            return {
                'fecha_inicio': primer_pago_pendiente.fecha_inicio,
                'fecha_final': primer_pago_pendiente.fecha_final,
                'monto_prestado': primer_pago_pendiente.monto_prestado,
                'mora': primer_pago_pendiente.mora,
                'intereses': primer_pago_pendiente.interes,
                'capital': primer_pago_pendiente.capital,
                'cuota': primer_pago_pendiente.cuota
            }
        return None


    def _calcular_total(self):
        primer_pago = self._primer_pago_pendiente()
        if primer_pago is None:
            raise ValueError("No hay pagos pendientes para calcular el total.")

        dias_diferencia = (self.fecha_emision - primer_pago['fecha_inicio']).days
        dias_atrasados = max((self.fecha_emision - primer_pago['fecha_final']).days, 0)
        
        mora = self._calculo_mora(primer_pago['monto_prestado'], dias_atrasados - 15) if dias_atrasados > 15 else 0
        intereses = self._calculo_intereses(dias_diferencia, primer_pago['monto_prestado'])
        
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
        primer_pago = self._primer_pago_pendiente()

        # Validar que haya un primer pago pendiente
        if primer_pago is None:
            return "No hay pagos pendientes para procesar."

        # Actualizar las propiedades del pago
        dias_diferencia = (self.fecha_emision - primer_pago['fecha_inicio']).days
        dias_atrasados = max((self.fecha_emision - primer_pago['fecha_final']).days, 0)
        
        mora = self._calculo_mora(primer_pago['monto_prestado'], dias_atrasados - 15) if dias_atrasados > 15 else 0
        self.interes = self._calculo_intereses(dias_diferencia, primer_pago['monto_prestado'])
        if self.credit.forma_de_pago == 'NIVELADA':
            cuota = self._calculo_cuota(intereses=self.interes)
            self.capital = self._calculo_capital(cuota=cuota, intereses=self.interes)
        else:
            self.capital = self._calculo_capital()
            cuota = self._calculo_cuota(intereses=self.interes, capital=self.capital)
        
        # Procesar el pago
        mora_restante = procesar_pago('Mora', mora)
        interes_restante = procesar_pago('Interes', self.interes)
        capital_restante = procesar_pago('Capital', self.capital)

        # Actualizar el estado de la transacción
        if mora_restante > 0 or interes_restante > 0 or capital_restante > 0:
            self.estado_transaccion = "PENDIENTE"
            self.registrar_pago(self.monto)
            return f"Pago realizado parcialmente. Mora pendiente: Q{mora_restante}, Intereses pendientes: Q{interes_restante}, Capital pendiente: Q{capital_restante}."

        # Si se ha pagado todo, actualizar el estado a completado
        self.estado_transaccion = "COMPLETADO"
        self.registrar_pago(self.monto)

        # Actualizar el plan de pagos
        self.actualizar_plan_pagos(monto_depositado - (mora + self.interes + self.capital))

        return f"Pago realizado con éxito. Q{monto_depositado - (mora + self.interes + self.capital)} restante."

    def actualizar_plan_pagos(self, saldo_pendiente):
        siguiente_pago = PaymentPlan.objects.filter(credit=self.credit, status=False).order_by('fecha_inicio').first()
        if siguiente_pago:
            if saldo_pendiente > 0:
                # Si hay saldo pendiente, agregarlo a la cuota del siguiente plan de pagos
                siguiente_pago.cuota += saldo_pendiente
            else:
                # Si se ha pagado más de lo necesario, restar el exceso de la cuota del siguiente plan de pagos
                siguiente_pago.cuota -= saldo_pendiente
                if siguiente_pago.cuota < 0:
                    siguiente_pago.cuota = 0
                    siguiente_pago.status = True
            siguiente_pago.save()

    def registrar_pago(self, monto):
        PaymentTransaction.objects.create(
            payment=self,
            transaction_type='PAGO REALIZADO',
            previous_status=self.estado_transaccion,
            new_status=self.estado_transaccion,
            amount=monto,
            mora=self.mora,
            interest=self.interes,
            capital=self.capital,
            remaining_amount=monto - (self.mora + self.interes + self.capital),
            description=self.descripcion
        )




    def _calcular_total(self):
        primer_pago = self._primer_pago_pendiente()
        if primer_pago is None:
            raise ValueError("No hay pagos pendientes para calcular el total.")

        dias_diferencia = (self.fecha_emision - primer_pago['fecha_inicio']).days
        dias_atrasados = max((self.fecha_emision - primer_pago['fecha_final']).days, 0)
        
        mora = self._calculo_mora(primer_pago['monto_prestado'], dias_atrasados - 15) if dias_atrasados > 15 else 0
        intereses = self._calculo_intereses(dias_diferencia, primer_pago['monto_prestado'])
        
        if self.credit.forma_de_pago == 'NIVELADA':
            cuota = self._calculo_cuota(intereses=intereses)
            capital = self._calculo_capital(cuota=cuota, intereses=intereses)
        else:
            capital = self._calculo_capital()
            cuota = self._calculo_cuota(intereses=intereses, capital=capital)
        
        return round(mora + intereses + capital, 2)

   

    def __str__(self):
        return f'PAGO {self.numero_referencia} - {self.estado_transaccion}'

class PaymentPlan(models.Model):
    mes = models.IntegerField('No.Mes')
    fecha_inicio = models.DateTimeField('Fecha de Inicio')
    fecha_final = models.DateTimeField('Fecha de Vencimiento')
    monto_prestado = models.DecimalField('Monto Prestado', max_digits=12, decimal_places=2, default=0)
    mora = models.DecimalField('Mora', max_digits=12, decimal_places=2, default=0)
    interes = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    capital = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    cuota = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.BooleanField(default=False)
    credit_id = models.ForeignKey(Credit, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'Plan de Pago'
        verbose_name_plural = 'Planes de Pago'

class PaymentTransaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('PAGO REALIZADO', 'Pago Realizado'),
        ('PAGO FALLIDO', 'Pago Fallido'),
    ]
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, verbose_name='Pago')
    transaction_type = models.CharField('Tipo de Transacción', max_length=50, choices=TRANSACTION_TYPE_CHOICES)
    previous_status = models.CharField('Estado Anterior', max_length=20)
    new_status = models.CharField('Nuevo Estado', max_length=20)
    amount = models.DecimalField('Monto', max_digits=12, decimal_places=2)
    mora = models.DecimalField('Mora', max_digits=12, decimal_places=2, default=0)
    interest = models.DecimalField('Intereses', max_digits=12, decimal_places=2, default=0)
    capital = models.DecimalField('Capital', max_digits=12, decimal_places=2, default=0)
    remaining_amount = models.DecimalField('Monto Restante', max_digits=12, decimal_places=2, default=0)
    description = models.TextField('Descripcion', blank=True, null=True)
    transaction_date = models.DateTimeField('Fecha de la Transacción', auto_now_add=True)

    class Meta:
        verbose_name = 'Transacción de Pago'
        verbose_name_plural = 'Transacciones de Pago'

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
        credito = Credito(
            instance.proposito, 
            instance.monto, 
            instance.plazo, 
            instance.tasa_interes, 
            instance.forma_de_pago, 
            instance.frecuencia_pago, 
            instance.fecha_inicio, 
            instance.tipo_credito, 
            instance.customer_id
        )
        plan_pago = PlanPago(credito)
        for pago in plan_pago.generar_plan():
            planPago = PaymentPlan(
                mes=pago['mes'],
                fecha_inicio=pago['fecha_inicio'],
                fecha_final=pago['fecha_final'],
                monto_prestado=pago['monto_prestado'],
                mora=pago['mora'],
                interes=pago['intereses'],
                capital=pago['capital'],
                cuota=pago['cuota'],
                credit_id=instance
            )
            planPago.save()

@receiver(post_save, sender=Payment)
def handle_payment_creation(sender, instance, created, **kwargs):
    if created:
        PaymentTransaction.objects.create(
            payment=instance,
            transaction_type='PAGO REALIZADO',
            previous_status='PENDIENTE',
            new_status=instance.estado_transaccion,
            amount=instance.monto,
            mora=instance.mora,
            interest=instance.interes,
            capital=instance.capital,
            remaining_amount=instance.monto - (instance.mora + instance.interes + instance.capital),
            description=instance.descripcion
        )
        print(f"Se ha registrado un nuevo pago con referencia {instance.numero_referencia}")