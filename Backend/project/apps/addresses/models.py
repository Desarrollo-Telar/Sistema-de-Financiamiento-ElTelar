from django.db import models

# Create your models here.
# Relaciones
from apps.customers.models import Customer




class Address(models.Model):
    tipo_direccion = [
        ('Dirección de Casa', 'Dirección de Casa'),
        ('Dirección de Trabajo', 'Dirección de Trabajo'),
        ('Dirección Personal', 'Dirección Personal'),
    ]
    
    
    street = models.CharField("Dirección particular o sede social completa", max_length=90, blank=False, null=False)
    number = models.CharField("Zona", max_length=90, blank=False, null=False)
    city = models.CharField("Departamento", max_length=100, blank=False, null=False)
    state = models.CharField("Municipio", max_length=90, blank=False, null=False)    
    country = models.CharField("País", max_length=90, blank=False, null=False, default='GUATEMALA')
    type_address = models.CharField("Tipo de Dirección", choices=tipo_direccion, max_length=90, blank=False, null=False)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.street}, {self.city} / {self.customer_id}'
    
    def direccion(self):
        return '{} Zona: {} Departamento: {} Municipio: {}'.format(self.street, self.number, self.city, self.state)

    class Meta:
        verbose_name = "Dirección"
        verbose_name_plural = "Direcciones"

class Coordinate(models.Model):
    latitud = models.DecimalField("Latitud", max_digits=10, decimal_places=6, blank=False, null=False)
    longitud = models.DecimalField("Longitud", max_digits=10, decimal_places=6, blank=False, null=False)
    address_id = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.address_id} - {self.latitud}, {self.longitud}'

    class Meta:
        verbose_name = "Coordenada"
        verbose_name_plural = "Coordenadas"
