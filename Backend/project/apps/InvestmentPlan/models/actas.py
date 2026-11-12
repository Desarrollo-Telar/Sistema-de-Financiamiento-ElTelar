from django.db import models
from apps.InvestmentPlan.models import InvestmentPlan


class Acta(models.Model):
    numero_acta = models.CharField(max_length=100, verbose_name="Número de Acta",  blank=True, null=True)
    fecha_acta = models.DateField(verbose_name="Fecha de Acta")
    acta_activa = models.BooleanField(default=True, verbose_name="Acta Activa")

    def __str__(self):
        return f"Acta {self.numero_acta} - Fecha: {self.fecha_acta}"

class DetalleActa(models.Model):
    acta = models.ForeignKey(Acta, on_delete=models.CASCADE, related_name='detalles', verbose_name="Acta")
    solicitud_credito = models.ForeignKey(InvestmentPlan, on_delete=models.CASCADE, related_name='detalles_acta', verbose_name="Solicitud de Crédito")


    def __str__(self):
        return f"Detalle de Acta {self.acta.numero_acta} - Solicitud: {self.solicitud_credito.investment_plan_code}"