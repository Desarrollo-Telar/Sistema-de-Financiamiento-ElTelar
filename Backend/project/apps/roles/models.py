from django.db import models
from django.contrib.auth.models import Permission


# Create your models here.
class Role(models.Model):
    role_name = models.CharField("Nombre del Rol", max_length=100, unique=True)
    permissions = models.ManyToManyField(Permission, blank=True, verbose_name="Permisos")
    description = models.TextField("Descripción", blank=True, null=True)

    def __str__(self):
        return self.role_name

    class Meta:
        verbose_name = "Rol"
        verbose_name_plural = "Roles"




class Meta:

    permissions = [
        ("agregar_usuario", "Tiene permiso de poder agregar un usuario al sistema"),
        ("editar_usuario", "Tiene permiso para editar un usuario del sistema"),
        ("eliminar_usuario","Tiene permiso puede eliminar un usuario del sistema")
    ]
