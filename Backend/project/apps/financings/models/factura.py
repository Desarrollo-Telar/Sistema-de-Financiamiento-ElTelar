from django.db import models

# TIEMPO
from django.utils import timezone

# MODELOS

from .recibo import Recibo

# ESTADOS DE CUENTAS
class Invoice(models.Model):
    issue_date = models.DateField(default=timezone.now)
    numero_factura = models.IntegerField("Numero de Factura")
    recibo_id = models.ForeignKey(Recibo, on_delete=models.CASCADE, verbose_name="Recibo")

    def __str__(self):
        return f'{self.numero_factura}'

    class Meta:
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'
