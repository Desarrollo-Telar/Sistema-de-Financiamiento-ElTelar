# BANCOS
from django.db import models

class Banco(models.Model):
    fecha = models.DateField()
    referencia = models.CharField('No.Referencia',max_length=100, unique=True)
    credito = models.DecimalField('Monto', decimal_places=2, max_digits=12)
    debito = models.DecimalField('Debito', decimal_places=2, max_digits=12, default=0)
    
    def __str__(self):
        return f'Fecha: {self.fecha} Referencia: {self.referencia} Monto: {self.credito}'

    class Meta:
        verbose_name = 'Banco'
        verbose_name_plural = 'Bancos'
