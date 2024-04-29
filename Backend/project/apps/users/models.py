from django.db import models
from django.contrib.auth.models import AbstractUser

# Creacion de relaciones
from apps.roles.models import Role

# Creacion de todas las tablas para este modulo

# Creacion de tabla de usuario
class User(AbstractUser):
    identification = [
        ('DPI', 'DPI'),
        ('PASAPORTE', 'PASAPORTE')
    ]
    type_identification = models.CharField(choices=identification, default='DPI', max_length=50 )
    identification_number = models.CharField(max_length=15, blank=False, null=False, unique=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)

# Creacion de tabla Rol y Usuario
class RoleUser(models.Model):
    idRole = models.ForeignKey(Role, blank=False, null=False, on_delete=models.CASCADE)
    idUser = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE)
