from django.db import models

# Relacion
from apps.customers.models import Customer
from apps.addresses.models import Address
from apps.InvestmentPlan.models import InvestmentPlan
from apps.subsidiaries.models import Subsidiary

# Create your models here.
from django.db.models.signals import post_delete
from django.dispatch import receiver
# SETTINGS OF PROJECT
from project.settings import MEDIA_URL, STATIC_URL
from project import settings
from project.database_store import minio_client  # asegúrate de que esté importado correctamente
from datetime import timedelta
import os

class Imagen(models.Model):
    image = models.ImageField("Imagen", blank=True, null=True, upload_to='documents/')
    description = models.TextField("Descripción", blank=True, null=True)
    uploaded_at = models.DateTimeField("Fecha de Creación", auto_now_add=True)

    def __str__(self):
        return self.description or "Sin descripción"
    
    

    def get_image(self):
        if self.image:
            try:
                return minio_client.presigned_get_object(
                    bucket_name='asiatrip',
                    object_name=self.image.name,
                    expires=timedelta(minutes=30)
                )
            except Exception:
                # Verifica si existe el archivo en el almacenamiento local
                local_path = os.path.join(settings.MEDIA_ROOT, self.image.name)
                if os.path.exists(local_path):
                    return f"{settings.MEDIA_URL}{self.image.name}"
        return None

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

class ImagenSubsidiary(models.Model):
    subsidiary = models.ForeignKey(Subsidiary, on_delete=models.CASCADE)
    image = models.ImageField("Imagen", blank=True, null=True, upload_to='documents/sucursal/')
    description = models.TextField("Descripción", blank=True, null=True)
    uploaded_at = models.DateTimeField("Fecha de Creación", auto_now_add=True)

    def __str__(self):
        return f"Imagen de la sucursal {self.subsidiary}"

    class Meta:
        verbose_name = "Imagen de la Sucursal"
        verbose_name_plural = "Imágenes de las Sucursales"

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
        return self.image_id

    class Meta:
        verbose_name = "Imagen de Garantía"
        verbose_name_plural = "Imágenes de Garantías"

class ImagenOther(models.Model):
    description = models.CharField("Descripción",max_length=150,blank=True, null=True)
    image_id = models.ForeignKey(Imagen, on_delete=models.CASCADE)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return self.description or 'NO TIENE DESCRIPCION'


    class Meta:
        verbose_name = "Otra Imagen"
        verbose_name_plural ="Otras Imágenes"

@receiver(post_delete, sender=Imagen)
def delete_image_files(sender, instance, **kwargs):
    # instance.image es el campo de imagen en tu modelo Imagen
    if instance.image:
        instance.image.delete()