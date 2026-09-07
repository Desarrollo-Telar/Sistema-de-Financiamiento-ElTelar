
from django.db import models
from math import floor
# RELACIONES
from apps.customers.models import Customer, CreditCounselor
from apps.InvestmentPlan.models import InvestmentPlan
from apps.financings.models import Credit
from apps.subsidiaries.models import Subsidiary
from .credito_demandado import CategoriaCreditoDemandado
# FORMATO
from apps.financings.formato import formatear_numero
from decimal import Decimal

# TIEMPO
from datetime import datetime, date
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.db.models import Q


class CondicionesCredito(models.Model):
    rules = [
        ('INTERES FIJO', 'INTERES FIJO'),
        ('CAPITAL FIJO', 'CAPITAL FIJO'),

        ]

    credit = models.ForeignKey(Credit, on_delete=models.CASCADE, related_name='condiciones_credito')
    reglas = models.CharField("Reglas", choices=rules, blank=True, null=True)
    monto = models.DecimalField("Monto", decimal_places=2, max_digits=15, blank=False, null=False)

    def __str__(self):
        return f"Condiciones de Crédito: {self.credit.codigo_credito} - Monto: {formatear_numero(self.monto)}"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['credit', 'reglas'],
                name='unique_regla_por_credito'
            )
        ]