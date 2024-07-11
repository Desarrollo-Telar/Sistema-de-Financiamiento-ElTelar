from django.db import models
from apps.customers.models import Customer
from apps.InvestmentPlan.models import InvestmentPlan
# Create your models here.
class Credit(models.Model):  
    formaPago = [
        ('NIVELADA','NIVELADA'),
        ('AMORTAZICACIONES O CAPITAL','AMORTAZICACIONES O CAPITAL')
    ]  
    frecuenciaPago = [
        ('MENSUAL','MENSUAL'),
        ('TRIMESTRAL','TRIMESTRAL'),
        ('SEMANAL','SEMANAL')
    ]
    proposito = models.TextField("Proposito", blank=False, null=False)
    monto = models.DecimalField("Monto", decimal_places=2, max_digits=15, blank=False, null=False)
    plazo = models.IntegerField("Plazo", blank=False, null=False)
    tasa_interes = models.DecimalField("Tasa de Interes", max_digits=5, decimal_places=2, null=False, blank=False)
    forma_de_pago = models.CharField("Forma de Pago", choices=formaPago, max_length=75, blank=False, null=False, default='NIVELADA')
    frecuencia_pago = models.CharField("Frecuencia de Pago", choices=frecuenciaPago, max_length=75, blank=False, null=False, default='NIVELADA')
    fecha_inicio = models.DateField("Fecha de inicio", blank=False, null=False)
    fecha_vencimiento = models.DateField("Fecha de vencimiento", blank=False, null=False)
    tipo_credito = models.CharField("Tipo de Credito",max_length=75, blank=False, null=False)
    codigo_credito = models.CharField("Codigo Credito",max_length=25, blank=False, null=False, unique=True)
    destino_id = models.OneToOneField(InvestmentPlan, on_delete=models.CASCADE, verbose_name='Destino')
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Cliente')
    creation_date = models.DateTimeField("Fecha de Creación", auto_now_add=True)

    class Meta:
        verbose_name = "Credito"
        verbose_name_plural = "Creditos"

