from django.db import models

# Relacion
from apps.customers.models import Customer
from apps.addresses.models import Address
from apps.InvestmentPlan.models import InvestmentPlan
# Create your models here.

class Imagen(models.Model):
    image = models.ImageField("Imagen", blank=True, null=True, upload_to='documents/')
    description = models.TextField("Descripción", blank=True, null=True)
    uploaded_at = models.DateTimeField("Fecha de Creación", auto_now_add=True)

    def __str__(self):
        return self.description or "Sin descripción"

    class Meta:
        verbose_name = "Imagen"
        verbose_name_plural = "Imágenes"

class ImagenCustomer(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    image_id = models.ForeignKey(Imagen, on_delete=models.CASCADE)

    def __str__(self):
        return f"Imagen del Cliente {self.customer_id}"

    class Meta:
        verbose_name = "Imagen del Cliente"
        verbose_name_plural = "Imágenes de Clientes"

class ImagenAddress(models.Model):
    address_id = models.ForeignKey(Address, on_delete=models.CASCADE)
    image_id = models.ForeignKey(Imagen, on_delete=models.CASCADE)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return f"Imagen de la Dirección {self.address_id}"

    class Meta:
        verbose_name = "Imagen de Dirección"
        verbose_name_plural = "Imágenes de Direcciones"

class ImagenGuarantee(models.Model):
    investment_plan_id = models.ForeignKey(InvestmentPlan, on_delete=models.CASCADE)
    image_id = models.ForeignKey(Imagen, on_delete=models.CASCADE)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return f"Imagen de la Garantía {self.address_id}"

    class Meta:
        verbose_name = "Imagen de Garantía"
        verbose_name_plural = "Imágenes de Garantías"

class ImagenOther(models.Model):
    description = models.CharField("Descripción",max_length=150,blank=True, null=True)
    image_id = models.ForeignKey(Imagen, on_delete=models.CASCADE)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)


    class Meta:
        verbose_name = "Otra Imagen"
        verbose_name_plural ="Otras Imágenes"

