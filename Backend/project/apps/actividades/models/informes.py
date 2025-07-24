# Models
from django.db import models

# Relacion
from apps.users.models import User

# TIEMPO
from datetime import datetime
from dateutil.relativedelta import relativedelta

class Informe(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Creador de Informe")
    nombre_reporte = models.CharField(verbose_name="Nombre del Reporte", max_length=100, default="Reporte INVERSIONES INTEGRALES EL TELAR")
    descripcion = models.TextField(verbose_name="Descripcion del Informe", null=True, blank=True)
    fecha_registro = models.DateField(auto_now_add=True)
    fecha_vencimiento = models.DateField()
    tipo_informe = models.CharField(verbose_name="Tipo de Informe", max_length=100, default="Cobranza")
    esta_activo = models.BooleanField(verbose_name="Estado del Informe", default=True)

    class Meta:
        verbose_name = 'Informe'
        verbose_name_plural = 'Informes'

    def calcular_fecha_vencimiento(self):
        self.fecha_vencimiento = self.fecha_registro + relativedelta(days=6)
        return self.fecha_vencimiento

    def save(self,*args, **kwargs):
        self.calcular_fecha_vencimiento()
        super().save(*args, **kwargs)

class DetalleInforme(models.Model):
    reporte = models.ForeignKey(Informe, on_delete=models.CASCADE, verbose_name="Informe")


    class Meta:
        verbose_name = 'Detalle de Informe'
        