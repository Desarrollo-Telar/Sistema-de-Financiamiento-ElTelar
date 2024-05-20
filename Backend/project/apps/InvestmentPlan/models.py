from django.db import models

# Relaciones
from apps.customers.models import Customer

# Create your models here.
class InvestmentPlan(models.Model):
    type_of_transfers_or_transfer_of_funds = [
        ('Local', 'Local'),
        ('Internacional', 'Internacional')
    ]
    type_of_product_or_service # Tipo de producto o servicio
    total_value_of_the_product_or_service # Valor total del producto o servicio
    investment_plan_description = models.TextField(blank=True, null=True) # Descripción del plan de inversión
    initial_amount  = models.CharField(max_length=75, blank=False, null=False) # Monto Inicial a manejar en el producto o servicios
    monthly_amount = models.CharField(max_length=75, blank=False, null=False) # Monto Mensual a manejar en el producto o servicios
    transfers_or_transfer_of_funds = models.BooleanField(blank=False, null=False) # transferencias o traslado de fondos Si o No
    type_of_transfers_or_transfer_of_funds # tipo de transferencias o traslado de fondos Local o Internacional
    customer_id = models.ForeignKey(Customer, blank=False, null=False, on_delete=models.CASCADE)