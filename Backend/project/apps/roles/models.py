from django.db import models
from django.contrib.auth.models import Permission


# Create your models here.
class Role(models.Model):
    role_name = models.CharField("Nombre del Rol", max_length=100, unique=True)
    description = models.TextField("Descripción", blank=True, null=True)

    def __str__(self):
        return self.role_name

    class Meta:
        verbose_name = "Rol"
        verbose_name_plural = "Roles"




# Creacion de Tabla Permisos
class Permiso(models.Model):
    nombre = models.CharField(verbose_name="Nombre del Permiso", max_length=100, blank=False, null=False)
    descripcion = models.TextField(verbose_name="Descripcion acerca del permiso", blank=True, null=True)
    codigo_permiso = models.CharField(verbose_name="Codigo del Permiso", max_length=75, unique=True)
    estado = models.BooleanField(verbose_name="Estado del Permiso")
    fecha_registro = models.DateTimeField("Fecha de Creación", auto_now_add=True)

    class Meta:
        verbose_name = 'Permiso'
        verbose_name_plural = 'Permisos'