from django.db import models

# MODELOS
from apps.customers.models import Customer
from apps.InvestmentPlan.models import InvestmentPlan

# TIEMPO
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.utils import timezone

# DECIMAL
from decimal import Decimal

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
    tasa_interes = models.DecimalField("Tasa de Interes", max_digits=5, decimal_places=3, null=False, blank=False)
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

        tasa = Decimal(self.tasa_interes) *100
        return round(tasa,2)

        
    def tasa_mensual(self):
        return self.tasa_interes
    
    def fecha_vencimiento(self):
        self.fecha_vencimiento =  self.fecha_inicio + relativedelta(months=self.plazo)
        return self.fecha_vencimiento
    
    def save(self,*args, **kwargs):
        #self.calculo_mora()
        self.fecha_vencimiento()
        self.calculo_fecha_limite()
        #self.calculo_interes()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Credito"
        verbose_name_plural = "Creditos"