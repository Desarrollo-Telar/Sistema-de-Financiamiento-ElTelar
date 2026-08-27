from django.db import models

# DIAS
from datetime import datetime
from dateutil.relativedelta import relativedelta
import calendar

# DECIMAL
from decimal import Decimal


# MODELOS
from .credit import Credit
from .payment_plan import PaymentPlan
from apps.subsidiaries.models import Subsidiary
from apps.users.models import User

# FORMATO
from apps.financings.formato import formatear_numero


import math
import uuid


class Descuento(models.Model):
    numero_referencia = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    credit = models.ForeignKey(Credit, on_delete=models.CASCADE, related_name='descuentos')
    cuota = models.ForeignKey(PaymentPlan, on_delete=models.CASCADE, related_name='descuentos')
    sucursal = models.ForeignKey(Subsidiary, on_delete=models.CASCADE, related_name='descuentos')
    fecha_descuento = models.DateTimeField(auto_now_add=True)
    interes_por_cobrar = models.DecimalField(max_digits=10, decimal_places=2)
    mora_por_cobrar = models.DecimalField(max_digits=10, decimal_places=2)
    saldo_capital_por_cobrar = models.DecimalField(max_digits=10, decimal_places=2)
    tipo_descuento = models.CharField(max_length=50)
    motivo_descuento = models.TextField()
    recalcular_cuota = models.BooleanField(default=False)
    usuario_descuento = models.ForeignKey(User, on_delete=models.CASCADE, related_name='descuentos')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)
    data_cuota = models.JSONField(null=True, blank=True)

    class Meta:
        verbose_name = "Descuento"
        verbose_name_plural = "Descuentos"
        ordering = ['-fecha_descuento']

    def __str__(self):
        return f"Descuento {self.numero_referencia} - Interés: {formatear_numero(self.interes_por_cobrar)}, Mora: {formatear_numero(self.mora_por_cobrar)}, Saldo Capital: {formatear_numero(self.saldo_capital_por_cobrar)} - Fecha: {self.fecha_descuento.strftime('%Y-%m-%d %H:%M:%S')}"