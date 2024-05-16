# Archivo models de modulo

# Librerias de DJANGO
from datetime import datetime
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser

# Llamado de tablas para la relacion
from apps.roles.models import Role

import random

# Creacion de todas las tablas para este modulo

# Creacion de tabla de usuario
class User(AbstractUser):
    identification = [
        ('DPI', 'DPI'),
        ('PASAPORTE', 'PASAPORTE'),
        ('OTRO', 'OTRO')
    ]
    genders = [
        ('MASCULINO', 'MASCULINO'),
        ('FEMENINO', 'FEMENINO')
    ]
    type_identification = models.CharField(choices=identification, default='DPI', max_length=50 )
    identification_number = models.CharField(max_length=15, blank=False, null=False, unique=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True)
    status = models.BooleanField(default=True)
    gender = models.CharField(choices=genders, default='MASCULINO', max_length=50)
    user_code = models.CharField(max_length=25, blank=False, null=False, unique=True)
    nationality = models.CharField(max_length=75, blank=False, null=False, default='Guatemala')
    profile_pic = models.ImageField(blank=True, null=True,upload_to='users/profile_pics/')
    creation_date = models.DateTimeField(auto_now_add=True)
    
    

    def __str__(self):
        if(self.first_name==''):
            return '{}'.format(self.username)
        return '{} {}'.format(self.first_name, self.last_name)
    
    def get_full_name(self):
        if(self.first_name==''):
            return '{}'.format(self.username)
        return '{} {}'.format(self.first_name, self.last_name)
    
    def get_status(self):
        if(self.status):
            return 'Activo'
        return 'Inactivo'
    
    def get_telephone(self):
        if not(self.telephone):
            return 'Numero de telefono no registrado'
        return self.telephone

# Creacion de la tabla Usuario Rol
class UserRole(models.Model):
    idUser = models.ForeignKey(User, blank=False, null=False,on_delete=models.CASCADE)
    idRole = models.ForeignKey(Role, blank=False, null=False, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'Rol de {self.idRole} para {self.idUser}'

# Creacion de la tabla de codigos de verificacion
class VerificationToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=timezone.now)

    @classmethod
    def generate_token(cls, user):
        code = ''.join(random.choices('0123456789', k=6))  # Genera un código de 6 dígitos
        return cls.objects.create(user=user, code=code)

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
def set_user_code(sender, instance, *args, **kwargs):
    if not instance.username: # Verifica si el username está vacío
        instance.username = instance.email # Usa el email como username si está vacío
