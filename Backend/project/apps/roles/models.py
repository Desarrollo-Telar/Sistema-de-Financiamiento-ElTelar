from django.db import models
# Creacion de relaciones
from apps.permissions.models import Permission

# Creacion de todas las tablas para este modulo

# Creacion de la tabla de rol
class Role(models.Model):
    role_name = models.CharField(max_length=75, null=False, blank=False, unique=True)
    description = models.TextField(blank=True)

# Creacion de tabla de Rol y Permiso
class RolePermission(models.Model):
    idRole = models.ForeignKey(Role, blank=False, null=False, on_delete=models.CASCADE)
    idPermission = models.ForeignKey(Permission, blank=False, null=False, on_delete=models.CASCADE)