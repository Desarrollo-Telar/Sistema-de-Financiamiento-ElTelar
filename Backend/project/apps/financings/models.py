from django.db import models
from apps.customers.models import Customer

from .models.accountstatement import AccountStatement
from .models.credit import Credit
from .models.disbursement import Disbursement
from .models.guarantees import Guarantees, DetailsGuarantees
from .models.payment_plan import PaymentPlan
from .models.payment import Payment
from .models.recibo import Recibo

# Create your models here.

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


        

