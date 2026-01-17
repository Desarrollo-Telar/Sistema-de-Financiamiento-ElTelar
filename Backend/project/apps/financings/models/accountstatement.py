
from django.db import models

# TIEMPO
from django.utils import timezone

# MODELOS

from .credit import Credit
from .payment import Payment
from .disbursement import Disbursement
from .payment_plan import PaymentPlan
from apps.accountings.models import Creditor, Insurance

# FORMATO
from apps.financings.formato import formatear_numero
# ESTADOS DE CUENTAS
class AccountStatement(models.Model):
    credit = models.ForeignKey(Credit, on_delete=models.CASCADE, related_name='account_statements', blank=True, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='account_statement', blank=True, null=True)
    disbursement = models.ForeignKey(Disbursement, on_delete=models.CASCADE, related_name='account_statement', blank=True, null=True)
    cuota = models.ForeignKey(PaymentPlan, on_delete=models.CASCADE, related_name='account_statement', blank=True, null=True)

    acreedor = models.ForeignKey(Creditor, on_delete=models.CASCADE, related_name='account_statement', blank=True, null=True)
    seguro = models.ForeignKey(Insurance, on_delete=models.CASCADE, related_name='account_statement', blank=True, null=True)

    issue_date = models.DateField(default=timezone.now)
    disbursement_paid = models.DecimalField('Desembolso Pagado',max_digits=10, decimal_places=2, default=0.0)
    interest_paid = models.DecimalField('Interes Pagado',max_digits=10, decimal_places=2, default=0.0)
    capital_paid = models.DecimalField('Capital Pagada',max_digits=10, decimal_places=2, default=0.0)
    late_fee_paid = models.DecimalField('Mora Pagada',max_digits=10, decimal_places=2, default=0.0)
    saldo_pendiente = models.DecimalField('Saldo Pendiente', max_digits=12, decimal_places=2, default=0)
    abono = models.DecimalField('Abono', max_digits=12, decimal_places=2, default=0)    
    numero_referencia = models.CharField('Numero de Referencia', max_length=255, unique=True)
    description = models.TextField('Descripcion',blank=True, null=True )
    excedente = models.DecimalField("Monto de excedente", decimal_places=2, max_digits=15, blank=True, null=True, default=0)
    es_visible = models.BooleanField("Puede ser visible", default=True, blank=True, null=True)
    creation_date = models.DateTimeField("Fecha de Creación", auto_now_add=True)
    def Fabono(self):
        return formatear_numero(self.abono)
    
    def Fsaldo_pendiente(self):
        return formatear_numero(self.saldo_pendiente)
    
    def Fsaldo_excedente(self):
        return formatear_numero(self.excedente)
    
    def Flate_fee_paid(self):
        return formatear_numero(self.late_fee_paid)
    
    def Finterest_paid(self):
        return formatear_numero(self.interest_paid)

    def Fcapital_paid(self):
        return formatear_numero(self.capital_paid)

    def Fdisbursement_paid(self):
        return formatear_numero(self.disbursement_paid)

    class Meta:
        verbose_name = "Estado de Cuenta"
        verbose_name_plural = "Estados de Cuentas"
    
    def fecha_emision(self):
        if self.payment:
            return self.payment.fecha_emision
        return self.issue_date


    def __str__(self):
        mensajes = f"{self.id}"
       
        return mensajes