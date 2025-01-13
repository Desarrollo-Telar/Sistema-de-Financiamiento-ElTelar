from django.db import models

# MODELOS
from .credit import Credit

# GARANTIA
class Guarantees(models.Model):
    descripcion = models.TextField("Descripcion", blank=False, null=False)
    suma_total = models.DecimalField("Suma Total de Garantia", decimal_places=2, max_digits=15)
    credit_id = models.ForeignKey(Credit, on_delete=models.CASCADE, verbose_name="Credito")

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name = 'Garantia'
        verbose_name_plural = 'Garantias'

# DETALLE DE GARANTIA
class DetailsGuarantees(models.Model):
    tipoGarantia = [
        ('HIPOTECA', 'HIPOTECA'),
        ('DERECHO DE POSESION HIPOTECA', 'DERECHO DE POSESION HIPOTECA'),
        ('FIADOR', 'FIADOR'),
        ('CHEQUE / PAGARE', 'CHEQUE / PAGARE'),
        ('VEHICULO', 'VEHICULO'),
        ('MOBILIARIA', 'MOBILIARIA')
    ]
    garantia_id = models.ForeignKey(Guarantees, on_delete=models.CASCADE, verbose_name='Garantia')
    tipo_garantia = models.CharField("Tipo de Garantia", choices=tipoGarantia, max_length=75)
    especificaciones = models.JSONField("Especificaciones")
    valor_cobertura = models.DecimalField("Valor de Cobertura", decimal_places=2, max_digits=15)

    def __str__(self):
        return self.tipo_garantia

    class Meta:
        verbose_name = 'Detalle de Garantia'
        verbose_name_plural = 'Detalles de Garantias'