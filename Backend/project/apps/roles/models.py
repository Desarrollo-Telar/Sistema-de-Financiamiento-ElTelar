from django.db import models
from django.contrib.auth.models import Permission
from apps.users.models import User


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

# Creacion de la tabla Usuario Rol
class UserRole(models.Model):
    idUser = models.ForeignKey(User, blank=False, null=False,on_delete=models.CASCADE, verbose_name='Usuario', related_name='rol_usuario')
    idRole = models.ForeignKey(Role, blank=False, null=False, on_delete=models.CASCADE, verbose_name='Rol', related_name='rol_usuario')
    
    def __str__(self):
        return f'Rol de {self.idRole} para {self.idUser}'

    class Meta:
        verbose_name = "Rol de Usuario"
        verbose_name_plural = "Roles de Usuarios"


class Meta:

    permissions = [
        ("agregar_usuario", "Tiene permiso de poder agregar un usuario al sistema"),
        ("editar_usuario", "Tiene permiso para editar un usuario del sistema"),
        ("eliminar_usuario","Tiene permiso puede eliminar un usuario del sistema")
    ]
