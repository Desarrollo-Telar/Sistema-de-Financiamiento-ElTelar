
from django.db import models
from math import floor
# RELACIONES
from apps.customers.models import Customer, CreditCounselor
from apps.InvestmentPlan.models import InvestmentPlan
from apps.subsidiaries.models import Subsidiary
# FORMATO
from apps.financings.formato import formatear_numero
from decimal import Decimal

# TIEMPO
from datetime import datetime
from django.utils import timezone
from dateutil.relativedelta import relativedelta

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
    tasa_mora = models.DecimalField("Tasa de Morosidad", decimal_places=2, max_digits=15, default=0.1)
    saldo_pendiente = models.DecimalField("Saldo Pendiente", decimal_places=2, max_digits=15, default=0)
    saldo_actual = models.DecimalField("Saldo Actual", decimal_places=2, max_digits=15, default=0)
    estado_aportacion = models.BooleanField(blank=True, null=True)
    estados_fechas =  models.BooleanField(blank=True, null=True)
    desembolsado_completo = models.BooleanField(default=False)

    # nuevos atributos
    plazo_restante = models.IntegerField("Plazo", blank=True, null=True, default=0)
    modifico = models.BooleanField(default=False, blank=False, null=False, verbose_name="MOdificacion")
    numero_credito = models.CharField(max_length=100, blank=True, null=True, default=0)
    saldo_sin_modificar = models.DecimalField(max_digits=15, decimal_places=2, default=0, null=True, blank=True)
    

    fecha_actualizacion = models.DateField("Fecha en que se actualizo el credito", default=datetime.now, null=True, blank=True)
    estado_judicial = models.BooleanField(default=False, verbose_name="Estado Judicial")

    valoracion = models.DecimalField(verbose_name="Puntuacion del Credito", decimal_places=2, max_digits=15, blank=True, null=True, default=0)
    excedente = models.DecimalField("Monto de excedente", decimal_places=2, max_digits=15, blank=True, null=True, default=0)

    sucursal = models.ForeignKey(Subsidiary, on_delete=models.SET_NULL, blank=True, null=True)
    asesor_de_credito = models.ForeignKey(CreditCounselor, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Asesor de este Credito")
    numero_identificacion_sucursal = models.CharField(verbose_name="Numero de Identificacion Sucursal por Cliente", max_length=150, blank=True, null=True)
    
    def __str__(self):
        return f'{self.codigo_credito} {self.customer_id}'
    
    def get_star_rating(self):
        estrellas = []
        if self.valoracion is None:
            valor = 0
        else:
            valor = float(self.valoracion)

        enteras = floor(valor)              # Número de estrellas llenas
        decimal = valor - enteras           # Parte decimal para media estrella

        for i in range(1, 6):
            if i <= enteras:
                estrellas.append('full')
            elif i == enteras + 1 and decimal >= 0.5:
                estrellas.append('half')
            else:
                estrellas.append('empty')

        return estrellas
    
    def formato_estado_aportacion(self):
        mensaje = None
        if self.estado_aportacion:
            mensaje = 'VIGENTE'
        elif self.estado_aportacion is None:
            mensaje = 'SIN APORTACIONES'
        else:
            mensaje = 'EN ATRASO'

        return mensaje
    
    def formato_estado_fecha(self):
        return 'VIGENTE' if self.estados_fechas else 'EN ATRASO'
    
    def formato_credito_cancelado(self):
        return 'CANCELADO' if self.is_paid_off else 'VIGENTE'

    def calcular_fecha_vencimiento(self):
        self.fecha_vencimiento = self.fecha_inicio + relativedelta(months=self.plazo)
        return self.fecha_vencimiento

    def tasa_mensual(self):
        convertir =  round(self.tasa_interes * Decimal(100),2)
        return formatear_numero(convertir)
    
    def save(self, *args, **kwargs):
        self.calcular_fecha_vencimiento()
        super().save(*args, **kwargs)
   
    
    def formato_monto(self):
        return formatear_numero(self.monto)
    
    def formato_saldo_pendiente(self):
        return formatear_numero(self.saldo_pendiente)
    
    def formato_saldo_actual(self):
        return formatear_numero(self.saldo_actual)
    
    def formato_saldo_excedente(self):
        return formatear_numero(self.excedente)

    class Meta:
        verbose_name = "Credito"
        verbose_name_plural = "Creditos"
