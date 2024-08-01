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
        ('CHEQUE', 'CHEQUE'),
        ('TRANSFERENCIA','TRANSFERENCIA'),
        ('CANCELACION ANTERIOR','CANCELACION ANTERIOR')
    ]
    credit_id = models.ForeignKey(Credit,on_delete=models.CASCADE ,verbose_name='Credito')
    forma_desembolso = models.CharField("Forma de Desmbolso", choices=formaDesembolso, max_length=75, blank=False, null=False)
    monto_desembolso = models.DecimalField("Monto", decimal_places=2, max_digits=15)
    saldo_anterior = models.DecimalField("Monto", decimal_places=2, max_digits=15)
    gasto_administrativo = models.DecimalField("Gasto Administrativo", decimal_places=2, max_digits=15 )
    monto_seguro = models.DecimalField("Monto de Seguro", decimal_places=2, max_digits=15)

    class Meta:
        verbose_name = "Desembolso"
        verbose_name_plural = "Desembolsos"

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
        ('DERECHO DE POSESION','DERECHO DE POSESION'),
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
