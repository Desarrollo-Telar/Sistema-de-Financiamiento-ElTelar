from django.db import models

# Create your models here.
# Relaciones
from apps.customers.models import Customer

from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.dispatch import receiver


from django.db.models import Q

class Address(models.Model):
    tipo_direccion = [
        ('Dirección de Casa', 'Dirección de Casa'),
        ('Dirección de Trabajo', 'Dirección de Trabajo'),
        ('Dirección Personal', 'Dirección Personal'),
    ]
    
    
    street = models.CharField("Dirección particular o sede social completa", max_length=120, blank=False, null=False)
    number = models.CharField("Zona", max_length=90, blank=False, null=False)
    city = models.CharField("Departamento", max_length=100, blank=False, null=False)
    state = models.CharField("Municipio", max_length=90, blank=False, null=False)    
    country = models.CharField("País", max_length=90, blank=False, null=False, default='GUATEMALA')
    type_address = models.CharField("Tipo de Dirección", choices=tipo_direccion, max_length=90, blank=False, null=False)
    latitud = models.CharField("Latitud", max_length=120, blank=False, null=False)
    longitud = models.CharField("Longitud",max_length=120, blank=False, null=False)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.street}, {self.city} / {self.customer_id}'
    
    def direccion(self):
        return '{} Zona: {} Departamento: {} Municipio: {}'.format(self.street, self.number, self.city, self.state)

    def get_direccion_personal(self):
        if self.type_address == 'Dirección Personal':
            return self.direccion()
        
    def get_municipio_personal(self):
        if self.type_address == 'Dirección Personal':
            return self.state
    
    def get_departamento_personal(self):
        if self.type_address == 'Dirección Personal':
            return self.city
        
    def get_direccion_laboral(self):
        if self.type_address == 'Dirección de Trabajo':
            return self.direccion()
        
    def get_municipio_laboral(self):
        if self.type_address == 'Dirección de Trabajo':
            return self.state
    
    def get_departamento_laboral(self):
        if self.type_address == 'Dirección de Trabajo':
            return self.city

    class Meta:
        verbose_name = "Dirección"
        verbose_name_plural = "Direcciones"



class Departamento(models.Model):
    nombre = models.CharField("Nombre del Departamento", max_length=120, blank=False, null=False)
    def __str__(self):
        return f'{self.nombre}'
        
    class Meta:
        verbose_name ='Departamento'
        verbose_name_plural = 'Departamentos'

class Municiopio(models.Model):
    nombre = models.CharField("Nombre del Municipio", max_length=120, blank=False, null=False, unique=True)
    depart = models.ForeignKey(Departamento, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return f'{self.nombre}'

    class Meta:
        verbose_name ='Municipio'
        verbose_name_plural = 'Municipios'


@receiver(post_save, sender=Address) 
def actualizar_info_direcciones(sender, instance, created, **kwargs): 
    if created: 
        departamento = instance.city 
        municipio = instance.state 
        filtrar_d = Q(nombre__icontains=departamento) | Q(id=departamento) 
        departamento_f = Departamento.objects.filter(filtrar_d).first() 
        filtrar_m = Q(nombre__icontains=municipio) | Q(id=municipio) 
        municipio_f = Municiopio.objects.filter(filtrar_m).first() 
        
        if departamento_f and municipio_f: 
            instance.city = departamento_f.nombre 
            instance.state = municipio_f.nombre 
            instance.save()
