from django.db import models

# MODELO
from .credit import Credit

# FORMATO
from apps.financings.formato import formatear_numero

# DESEMBOLSO
class Disbursement(models.Model):
    formaDesembolso = [
        ('APLICACIÓN GASTOS', 'APLICACIÓN GASTOS'),
        ('APLICACIÓN DE AMPLIACIÓN DE CRÉDITO VIGENTE', 'APLICACIÓN DE AMPLIACIÓN DE CRÉDITO VIGENTE'),
        ('CANCELACIÓN DE CRÉDITO VIGENTE', 'CANCELACIÓN DE CRÉDITO VIGENTE'),
        ('DESEMBOLSAR', 'DESEMBOLSAR')
    ]
    credit_id = models.ForeignKey(Credit, on_delete=models.CASCADE, verbose_name='Credito')
    forma_desembolso = models.CharField("Forma de Desembolso", choices=formaDesembolso, max_length=75, blank=False, null=False)
    monto_credito = models.DecimalField("Monto Credito", decimal_places=2, max_digits=15, default=0)
    monto_credito_agregar = models.DecimalField("Monto Credito Agregar", decimal_places=2, max_digits=15, default=0)
    monto_credito_cancelar = models.DecimalField("Monto Credito Cancelar", decimal_places=2, max_digits=15, default=0) 
    saldo_anterior = models.DecimalField("Saldo Anterior", decimal_places=2, max_digits=15, default=0)
    honorarios = models.DecimalField("Honorarios", decimal_places=2, max_digits=15, default=0)
    poliza_seguro = models.DecimalField("Poliza de Seguro", decimal_places=2, max_digits=15, default=0)
    monto_desembolsado = models.DecimalField("Monto Desembolsado", decimal_places=2, max_digits=15, default=0)
    total_gastos  = models.DecimalField("Total de gastos", decimal_places=2, max_digits=15, default=0)
    monto_total_desembolso = models.DecimalField("Monto Total a Desembolsar", decimal_places=2, max_digits=15, default=0)
    total_t = models.DecimalField("Total de totales", decimal_places=2, max_digits=15, default=0)
    description = models.TextField("Descripcion", blank=True, null=True)
    creation_date = models.DateTimeField("Fecha de Creación", auto_now_add=True)
    #Nuevos atributos
    #credito_cancelado = models.ForeignKey(Credit, on_delete=models.CASCADE, verbose_name='Credito', blank=True, null=True)

    
    def f_monto_credito(self):
        return formatear_numero(self.monto_credito)

    def f_monto_credito_agregar(self):
        return formatear_numero(self.monto_credito_agregar)
    
    def f_monto_credito_cancelar(self):
        return formatear_numero(self.monto_credito_cancelar)
    
    def f_saldo_anterior(self):
        return formatear_numero(self.saldo_anterior)
    
    def f_honorarios(self):
        return formatear_numero(self.honorarios)
    
    def f_poliza_seguro(self):
        return formatear_numero(self.poliza_seguro)
    
    def f_monto_desembolsado(self):
        return formatear_numero(self.monto_desembolsado)
    
    def f_total_gastos(self):
        return formatear_numero(self.total_gastos)
    
    def f_monto_total_desembolso(self):
        return formatear_numero(self.monto_total_desembolso)

    def __str__(self):
        return f'{self.forma_desembolso}'

    class Meta:
        verbose_name = "Desembolso"
        verbose_name_plural = "Desembolsos"