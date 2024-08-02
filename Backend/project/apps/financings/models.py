from django.db import models
from apps.customers.models import Customer
from apps.InvestmentPlan.models import InvestmentPlan

# Signals
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete

# Django
from django.dispatch import receiver
from django.utils import timezone
import random
from datetime import datetime

# Settings
from project.settings import MEDIA_URL, STATIC_URL

# OS
import os

# Create your models here.
class Credit(models.Model):  
    formaPago = [
        ('NIVELADA','NIVELADA'),
        ('AMORTIZACIONES A CAPITAL','AMORTIZACIONES A CAPITAL')
    ]  
    frecuenciaPago = [
        ('MENSUAL','MENSUAL'),
        ('TRIMESTRAL','TRIMESTRAL'),
        ('SEMANAL','SEMANAL')
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
    forma_de_pago = models.CharField("Forma de Pago", choices=formaPago, max_length=75, blank=False, null=False, default='MENSUAL')
    frecuencia_pago = models.CharField("Frecuencia de Pago", choices=frecuenciaPago, max_length=75, blank=False, null=False, default='NIVELADA')
    fecha_inicio = models.DateField("Fecha de Inicio", blank=False, null=False)
    fecha_vencimiento = models.DateField("Fecha de Vencimiento", blank=False, null=False)
    tipo_credito = models.CharField("Tipo de Credito",choices=credit_type,max_length=75, blank=False, null=False)
    codigo_credito = models.CharField("Codigo Credito",max_length=25, blank=True, null=True)
    destino_id = models.ForeignKey(InvestmentPlan, on_delete=models.SET_NULL, blank=True,null=True ,verbose_name='Destino')
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Cliente')
    creation_date = models.DateTimeField("Fecha de Creación", auto_now_add=True)

    class Meta:
        verbose_name = "Credito"
        verbose_name_plural = "Creditos"

class Disbursement(models.Model):
    formaDesembolso = [
        ('APLICACIÓN GASTOS', 'APLICACIÓN GASTOS'),
        ('APLICACIÓN DE AMPLIACIÓN DE CRÉDITO VIGENTE','APLICACIÓN DE AMPLIACIÓN DE CRÉDITO VIGENTE'),
        ('CANCELACIÓN DE CRÉDITO VIGENTE','CANCELACIÓN DE CRÉDITO VIGENTE')
    ]
    credit_id = models.ForeignKey(Credit,on_delete=models.CASCADE ,verbose_name='Credito')
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
    descripcion = models.TextField("Descripcion",blank=False, null=False)
    suma_total  = models.DecimalField("Suma Total de Garantia", decimal_places=2, max_digits=15)
    credit_id = models.ForeignKey(Credit, on_delete=models.CASCADE, verbose_name="Credito")
    
    class Meta:
        verbose_name = 'Garantia'
        verbose_name_plural = 'Garantias'
    
class DetailsGuarantees(models.Model):
    tipoGarantia = [
        ('HIPOTECA','HIPOTECA'),
        ('DERECHO DE POSESION HIPOTECA','DERECHO DE POSESION HIPOTECA'),
        ('FIADOR','FIADOR'),
        ('CHEQUE','CHEQUE'),
        ('VEHICULO','VEHICULO'),
        ('MOBILIARIA','MOBILIARIA')
    ]
    garantia_id = models.ForeignKey(Guarantees, on_delete=models.CASCADE, verbose_name='Garantia')
    tipo_garantia = models.CharField("Tipo de Garantia", choices=tipoGarantia, max_length=75)
    especificaciones = models.JSONField("Especificaciones")
    valor_cobertura = models.DecimalField("Valor de Cobertura", decimal_places=2, max_digits=15)
    
    class Meta:
        verbose_name = 'Detalle de Garantia'
        verbose_name_plural = 'Detalles de Garantias'



@receiver(pre_save, sender=Credit)
def set_customer_code_and_update_status(sender, instance, **kwargs):
    # Si el código del cliente está vacío o es una cadena vacía, genera uno nuevo
    if not instance.codigo_credito or instance.codigo_credito == '':

        counter = 1
        
        # Generar el código base
        customer_code = instance.customer_id.customer_code
        credit_code = f'{customer_code} / {counter}'

        # Verificar si no existe un código igual, si no, generar uno nuevo
        while Credit.objects.filter(codigo_credito=credit_code).exists():
            counter += 1
            credit_code = f'{customer_code} / {counter}'

        instance.codigo_credito = credit_code
