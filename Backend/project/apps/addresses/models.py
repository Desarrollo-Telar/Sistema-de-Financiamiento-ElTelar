from django.db import models

# Create your models here.
# Relaciones
from apps.customers.models import Customer

class Address(models.Model):
    type_address = [
        ('Dirección de Casa', 'Dirección de Casa'),
        ('Dirección de Trabajo', 'Dirección de Trabajo'),
        ('Dirección Personal', 'Dirección Personal'),
        ]
    street = models.CharField(max_length=90, blank=False, null=False) # Calle
    number= models.CharField(max_length=90, blank=False, null=False) # Numero
    city = models.CharField(max_length=90, blank=False, null=False)# Ciudad
    state = models.CharField(max_length=90, blank=False, null=False)# Estado
    postal_code = models.CharField(max_length=90, blank=False, null=False)# Codigo Postal
    country = models.CharField(max_length=90, blank=False, null=False) # Pais
    type_address = models.CharField(choices=type_address,max_length=90, blank=False, null=False)
    customer_id = models.ForeignKey(Customer, blank=False, null=False, on_delete=models.CASCADE)