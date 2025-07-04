from django.db import models
from apps.customers.models import Customer


from apps.financings.models.accountstatement import AccountStatement
from apps.financings.models.credit import Credit
from apps.financings.models.disbursement import Disbursement
from apps.financings.models.guarantees import Guarantees, DetailsGuarantees
from apps.financings.models.payment_plan import PaymentPlan
from apps.financings.models.payment import Payment
from apps.financings.models.recibo import Recibo

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



        

