from django.db import models

# Relaciones
from apps.customers.models import Customer

# Create your models here.



class InvestmentPlan(models.Model):
    tipo_producto_servicio = [
        ('DERECHOS DE POSESIÓN E HIPOTECA', 'DERECHOS DE POSESIÓN E HIPOTECA'),
        ('FIDUCIARIA', 'FIDUCIARIA'),
        ('PRENDARIA', 'PRENDARIA'),
        ('MOBILIARIA', 'MOBILIARIA'),
        ('FIDEICOMISOS Y PROGRAMAS ADICIONALES', 'FIDEICOMISOS Y PROGRAMAS ADICIONALES'),
        ('PRÉSTAMO', 'PRÉSTAMO')
    ]
    tipo_transferencia = [
        ('Local', 'Local'),
        ('Internacional', 'Internacional')
    ]
    type_of_product_or_service = models.CharField("Tipo de Producto o Servicio", max_length=75,choices=tipo_producto_servicio)
    total_value_of_the_product_or_service = models.DecimalField("Valor Total del Producto o Servicio", max_digits=15, decimal_places=2, blank=False, null=False)
    investment_plan_description = models.TextField("Descripción del Plan de Inversión", blank=True, null=True)
    initial_amount = models.DecimalField("Monto Inicial", max_digits=15, decimal_places=2, blank=False, null=False)
    monthly_amount = models.DecimalField("Monto Mensual", max_digits=15, decimal_places=2, blank=False, null=False)
    transfers_or_transfer_of_funds = models.BooleanField("Transferencias o Traslado de Fondos", blank=False, null=False)
    type_of_transfers_or_transfer_of_funds = models.CharField("Tipo de Transferencia", max_length=75, choices=tipo_transferencia)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.type_of_product_or_service} - {self.customer_id}"

    def description(self):
        return self.investment_plan_description or '----'
    
    def transferencias_o_traslado_de_Fondos(self):
        return 'Si' if self.transfers_or_transfer_of_funds else 'No'
    
    def tipo_transferencia(self):
        return 'Local' if self.transfers_or_transfer_of_funds else 'Internacional'

    class Meta:
        verbose_name = "Plan de Inversión"
        verbose_name_plural = "Planes de Inversión"

 