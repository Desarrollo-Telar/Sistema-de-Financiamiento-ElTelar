from django.db import models
from django.contrib.auth.models import Permission
# Create your models here.
class Role(models.Model):
    role_name = models.CharField(max_length=100, unique=True)
    permissions = models.ManyToManyField('auth.Permission', blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.role_name



class Meta:

    permissions = [
        ("agregar_usuario", "Tiene permiso de poder agregar un usuario al sistema"),
        ("editar_usuario", "Tiene permiso para editar un usuario del sistema"),
        ("eliminar_usuario","Tiene permiso puede eliminar un usuario del sistema")
    ]
