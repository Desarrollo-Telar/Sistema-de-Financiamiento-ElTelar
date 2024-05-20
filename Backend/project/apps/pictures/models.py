from django.db import models

# Relacion
from apps.customers.models import Customer
from apps.addresses.models import Address

# Create your models here.
class Imagen(models.Model):
    image = models.ImageField(blank=True, null=True,upload_to='documents/')
    description = models.TextField(blank=True, null=True)

class ImagenCustomer(models.Model):
    # Aqui se registra la imagenes de aspecto de cliente, como DPI
    customer_id = models.ForeignKey(Customer, blank=False, null=False, on_delete=models.CASCADE)
    image_id = models.ForeignKey(Imagen, blank=False, null=False, on_delete=models.CASCADE)

class ImagenAddress(models.Model):
    # Aqui se registar las imagenes de referencia, Direccion, Imagen de Servicios ( Luz o Teléfono) o Constancia de Residencia
    addres_id = models.ForeignKey(Address, blank=False, null=False, on_delete=models.CASCADE)
    image_id = models.ForeignKey(Imagen, blank=False, null=False, on_delete=models.CASCADE)
""" 
class ImagenGuarantee(models.Model):
    # Aqui se registar las imagenes de referencia, Direccion, Imagen de Servicios ( Luz o Teléfono) o Constancia de Residencia
    addres_id = models.ForeignKey(Address, blank=False, null=False, on_delete=models.CASCADE)
    image_id = models.ForeignKey(Imagen, blank=False, null=False, on_delete=models.CASCADE)
"""
# Falta por agregar imagen de boleta de pago guarantee