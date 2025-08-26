# Models
from django.db import models

# Relacion
from apps.users.models import User
from apps.customers.models import Cobranza

# TIEMPO
import datetime
from dateutil.relativedelta import relativedelta

class Informe(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Creador de Informe")
    nombre_reporte = models.CharField(verbose_name="Nombre del Reporte", max_length=100, default="Reporte INVERSIONES INTEGRALES EL TELAR")
    descripcion = models.TextField(verbose_name="Descripcion del Informe", null=True, blank=True)
    fecha_registro = models.DateField(auto_now_add=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    #tipo_informe = models.CharField(verbose_name="Tipo de Informe", max_length=100, default="Cobranza")
    esta_activo = models.BooleanField(verbose_name="Estado del Informe", default=True)

    class Meta:
        verbose_name = 'Informe'
        verbose_name_plural = 'Informes'

    def calcular_fecha_vencimiento(self):
        if self.fecha_registro:
            next_month = self.fecha_registro + relativedelta(months=1)
            return next_month.replace(day=1)
        return datetime.date.today().replace(day=1) + relativedelta(months=1)

    def save(self, *args, **kwargs):
        self.fecha_vencimiento = self.calcular_fecha_vencimiento()
        super().save(*args, **kwargs)    

    def __str__(self):
        return f'#{self.id} - {self.usuario}'   

class DetalleInformeCobranza(models.Model):
    reporte = models.ForeignKey(Informe, on_delete=models.CASCADE, verbose_name="Informe")
    cobranza = models.ForeignKey(Cobranza, on_delete=models.CASCADE, verbose_name="Cobranza")

    def __str__(self):
        return f'#{self.id} - {self.reporte} {self.cobranza}'

    def _total_registros(self):
        return DetalleInformeCobranza.objects.filter(reporte=self.reporte).count()

    def _total_pendientes_cobranza(self):
        return DetalleInformeCobranza.objects.filter(
            reporte=self.reporte, 
            cobranza__estado_cobranza__icontains="PENDIENTE"
        ).count()

    def _total_vencidos_cobranza(self):
        return DetalleInformeCobranza.objects.filter(
            reporte=self.reporte, 
            cobranza__estado_cobranza__icontains="INCUMPLIDO"
        ).count()

    def _total_completados_cobranza(self):
        return DetalleInformeCobranza.objects.filter(
            reporte=self.reporte, 
            cobranza__estado_cobranza__icontains="COMPLETADO"
        ).count()

    def porcentajes_cobranza(self):
        total = self._total_registros()
        if total == 0:
            return {"pendientes": 0, "vencidos": 0, "completados": 0}

        pendientes = (self._total_pendientes_cobranza() / total) * 100
        vencidos = (self._total_vencidos_cobranza() / total) * 100
        completados = (self._total_completados_cobranza() / total) * 100

        return {
            "pendientes": round(pendientes, 2),
            "vencidos": round(vencidos, 2),
            "completados": round(completados, 2),
        }

    class Meta:
        verbose_name = 'Detalle de Informe'
        