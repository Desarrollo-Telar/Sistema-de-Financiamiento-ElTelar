# Create your models here.
from django.db import models


# Relaciones
from apps.customers.models import Customer
from apps.subsidiaries.models import Subsidiary

from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.dispatch import receiver


from django.db.models import Q

class Address(models.Model):
    tipo_direccion = [
        ('Dirección de Casa', 'Dirección de Casa'),
        ('Dirección de Trabajo', 'Dirección de Trabajo'),
        ('Dirección Personal', 'Dirección Personal'),
        ('Dirección de Sucursal','Dirección de Sucursal'),
    ]
    
    
    street = models.CharField("Dirección particular o sede social completa", max_length=120, blank=False, null=False)
    number = models.CharField("Zona", max_length=90, blank=False, null=False)
    city = models.CharField("Departamento", max_length=100, blank=False, null=False)
    state = models.CharField("Municipio", max_length=90, blank=False, null=False)    
    country = models.CharField("País", max_length=90, blank=False, null=False, default='GUATEMALA')
    type_address = models.CharField("Tipo de Dirección", choices=tipo_direccion, max_length=90, blank=True, null=True)
    latitud = models.CharField("Latitud", max_length=120, blank=False, null=False)
    longitud = models.CharField("Longitud",max_length=120, blank=False, null=False)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)
    subsidiary = models.ForeignKey(Subsidiary, on_delete=models.CASCADE, blank=True, null=True)
    codigo_postal = models.CharField("Codigo Postal", blank=True, null=True, max_length=100)
    creation_date = models.DateTimeField("Fecha de Creación", auto_now_add=True)

    def __str__(self):
        return f'{self.street}, {self.city} '
    
    def direccion(self):
        return '{} Zona: {} Departamento: {} Municipio: {}'.format(self.street, self.number, self.city, self.state)

    class Meta:
        verbose_name = "Dirección"
        verbose_name_plural = "Direcciones"



class Departamento(models.Model):
    nombre = models.CharField("Nombre del Departamento", max_length=120, blank=False, null=False)
    codigo_postal = models.CharField("Codigo Postal", blank=True, null=True, max_length=100)
    creation_date = models.DateTimeField("Fecha de Creación", auto_now_add=True)
    def __str__(self):
        return f'{self.nombre}'
        
    class Meta:
        verbose_name ='Departamento'
        verbose_name_plural = 'Departamentos'

class Municiopio(models.Model):
    nombre = models.CharField("Nombre del Municipio", max_length=120, blank=False, null=False, unique=True)
    depart = models.ForeignKey(Departamento, on_delete=models.CASCADE, blank=False, null=False)
    codigo_postal = models.CharField("Codigo Postal", blank=True, null=True, max_length=100)
    creation_date = models.DateTimeField("Fecha de Creación", auto_now_add=True)
    def __str__(self):
        return f'{self.nombre}'

    class Meta:
        verbose_name ='Municipio'
        verbose_name_plural = 'Municipios'


@receiver(pre_save, sender=Address)
def actualizar_info_direcciones(sender, instance, **kwargs):
    departamento = instance.city
    municipio = instance.state

    print(f'Departamento: {departamento}. Municipio: {municipio}')

    filtrar_d = Q(nombre__icontains=departamento) | Q(id=departamento)
    departamento_f = Departamento.objects.filter(filtrar_d).first()

    print(f'Departamento encontrado: {departamento_f}')

    filtrar_m = Q(nombre__icontains=municipio) | Q(id=municipio)
    municipio_f = Municiopio.objects.filter(filtrar_m).first()

    print(f'Municipio Encontrado: {municipio_f}')

    if departamento_f and municipio_f:
        instance.city = departamento_f.nombre
        instance.state = municipio_f.nombre
