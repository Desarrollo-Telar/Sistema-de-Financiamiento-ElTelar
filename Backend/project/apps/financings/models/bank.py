# BANCOS
from django.db import models
from datetime import datetime

# FORMATO
from apps.financings.formato import formatear_numero

class Banco(models.Model):
    fecha = models.DateField()
    referencia = models.CharField('No.Referencia',max_length=100, unique=True)
    credito = models.DecimalField('Monto', decimal_places=2, max_digits=12)
    debito = models.DecimalField('Debito', decimal_places=2, max_digits=12, default=0)
    descripcion = models.TextField('Descripción', blank=True, null=True)
    creation_date = models.DateTimeField("Fecha de Creación", auto_now_add=True)

    def f_credito(self):
        return formatear_numero(self.credito)
    
    def f_debito(self):
        return formatear_numero(self.debito)
    
    def __str__(self):
        return f'Fecha: {self.fecha} Referencia: {self.referencia} Monto: {self.credito}'

    class Meta:
        verbose_name = 'Banco'
        verbose_name_plural = 'Bancos'
