# BANCOS
from django.db import models

# RELACION
from apps.subsidiaries.models import Subsidiary
# TIEMPO
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
    
    status = models.BooleanField("Status", default=False)
    secuencial = models.CharField('Secuencial',max_length=100,  blank=True)
    cheque= models.CharField('Cheque',max_length=100, blank=True)
    saldo_contable = models.DecimalField('Saldo Contable', decimal_places=2, max_digits=12, default=0)
    saldo_disponible = models.DecimalField('Saldo Disponible', decimal_places=2, max_digits=12, default=0)
    # Nuevos Atributos
    registro_ficticio = models.BooleanField("Registro Ficticio", default=False)
    sucursal = models.ForeignKey(Subsidiary, on_delete=models.SET_NULL, blank=True, null=True)
    
    nombre_del_banco = models.CharField('Nombre del Banco',max_length=100, blank=True, null=True)
    def f_credito(self):
        return formatear_numero(self.credito)
    
    def f_debito(self):
        return formatear_numero(self.debito)

    def f_saldo_contable(self):
        return formatear_numero(self.saldo_contable)
    
    def f_saldo_disponible(self):
        return formatear_numero(self.saldo_disponible)
    
    def __str__(self):
        return f'Fecha: {self.fecha} Referencia: {self.referencia} Monto: {self.credito}'

    class Meta:
        verbose_name = 'Banco'
        verbose_name_plural = 'Bancos'
