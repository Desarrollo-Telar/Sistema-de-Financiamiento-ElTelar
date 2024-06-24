# Archivo models de modulo

# Librerias de DJANGO
from datetime import datetime
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser




import random

# Creacion de todas las tablas para este modulo

# Creacion de tabla de usuario


class User(AbstractUser):
    tipo_identificacion = [
        ('DPI', 'DPI'),
        ('PASAPORTE', 'PASAPORTE'),
        ('OTRO', 'OTRO')
    ]

    genero = [
        ('MASCULINO', 'MASCULINO'),
        ('FEMENINO', 'FEMENINO')
    ]
    roles = [
        ('Administrador','Administrador'),
        ('Administradora','Administradora'),
        ('Programador','Programador'),
        ('Programadora','Programadora'),
        ('Secretaria','Secretaria'),
        ('Secretario','Secretario'),
        ('Contador','Contador'),
        ('Contadora','Contadora'),
    ]
    type_identification = models.CharField("Tipo de Identificación", choices=tipo_identificacion, default='DPI', max_length=50)
    identification_number = models.CharField("Número de Identificación", max_length=15, blank=False, null=False, unique=True)
    telephone = models.CharField("Teléfono", max_length=20, blank=True, null=True)
    email = models.EmailField("Correo Electrónico", unique=True)
    status = models.BooleanField("Estado", default=True)
    gender = models.CharField("Género", choices=genero, default='MASCULINO', max_length=50)
    user_code = models.CharField("Código de Usuario", max_length=25, blank=False, null=False, unique=True)
    nationality = models.CharField("Nacionalidad", max_length=75, blank=False, null=False, default='Guatemala')
    profile_pic = models.ImageField("Foto de Perfil", blank=True, null=True, upload_to='users/profile_pics/')
    rol = models.CharField("Rol de Usuario", choices=roles, max_length=50)
    creation_date = models.DateTimeField("Fecha de Creación", auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}' if self.first_name else self.username

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}' if self.first_name else self.username

    def get_status(self):
        return 'Activo' if self.status else 'Inactivo'

    def get_telephone(self):
        return self.telephone if self.telephone else 'Número de teléfono no registrado'

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"



#Funcion clave para la generacion de codigos de usuario, luego de haberse creado
@receiver(pre_save, sender=User)
def set_user_code(sender, instance, *args, **kwargs):
    if instance.user_code == '':
        # Obtiene la fecha y hora actual
        current_date = datetime.now()

        # Extrae el año de la fecha actual
        current_year = current_date.year  

        # Formato al codigo de usuario
        user_code_base = f'{current_year}-'

        # Contador
        counter = 1

        # Base final del codigo
        # Ejemplo: 2024-1
        user_code = f'{user_code_base}{counter}'

        # Verificar si no existe un codigo igual, si no generar uno nuevo
        while User.objects.filter(user_code=user_code).exists():
            counter += 1
            user_code = f'{user_code_base}{counter}'
            print(instance.user_code)

        # Guardar informacion
        instance.user_code = user_code

#Funcion clave para guardar el nombre de usuario utilizando el email registrado
@receiver(pre_save, sender=User)
def set_username(sender, instance, *args, **kwargs):
    if not instance.username: # Verifica si el username está vacío
        instance.username = instance.email # Usa el email como username si está vacío

# Funcion para permisos de administrador
@receiver(pre_save, sender=User)
def set_rol(sender, instance, *args, **kwargs):
    roles_superuser = ['Administrador', 'Administradora', 'Programador', 'Programadora']
    
    if instance.rol in roles_superuser:
        instance.is_superuser = True 
    elif instance.is_superuser:
        instance.rol = 'Administrador'

