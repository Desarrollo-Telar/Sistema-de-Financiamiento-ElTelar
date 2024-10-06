
from django.db import models

# TIEMPO
from django.utils import timezone

# MODELOS

from .payment import Payment
from .disbursement import Disbursement, Credit

# ESTADOS DE CUENTAS
class AccountStatement(models.Model):
    credit = models.ForeignKey(Credit, on_delete=models.CASCADE, related_name='account_statements')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='account_statement', blank=True, null=True)
    disbursement = models.ForeignKey(Disbursement, on_delete=models.CASCADE, related_name='account_statement', blank=True, null=True)
    issue_date = models.DateField(default=timezone.now)
    disbursement_paid = models.DecimalField('Desembolso Pagado',max_digits=10, decimal_places=2, default=0.0)
    interest_paid = models.DecimalField('Interes Pagado',max_digits=10, decimal_places=2, default=0.0)
    capital_paid = models.DecimalField('Capital Pagada',max_digits=10, decimal_places=2, default=0.0)
    late_fee_paid = models.DecimalField('Mora Pagada',max_digits=10, decimal_places=2, default=0.0)
    saldo_pendiente = models.DecimalField('Saldo Pendiente', max_digits=12, decimal_places=2, default=0)
    abono = models.DecimalField('Abono', max_digits=12, decimal_places=2, default=0)    
    numero_referencia = models.CharField('Numero de Referencia', max_length=255, unique=True)
    description = models.TextField('Descripcion',blank=True, null=True )
    

    class Meta:
        verbose_name = "Estado de Cuenta"
        verbose_name_plural = "Estados de Cuentas"
    
    def fecha_emision(self):
        if self.payment:
            return self.payment.fecha_emision
        return self.issue_date


    def __str__(self):
        return f"Estado de cuenta para crédito {self.credit.id} "