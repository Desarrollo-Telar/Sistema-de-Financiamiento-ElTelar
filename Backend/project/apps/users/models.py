from django.db import models
from django.contrib.auth.models import AbstractUser

from datetime import datetime
from django.db.models.signals import pre_save
from django.dispatch import receiver

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
    
    status = models.BooleanField(default=True)
    gender = models.CharField(choices=genders, default='MASCULINO', max_length=50)
    user_code = models.CharField(max_length=25, blank=False, null=False, unique=True)
    nationality = models.CharField(max_length=75, blank=False, null=False, default='Guatemala')
    profile_pic = models.ImageField(upload_to='users/profile_pics/')
    creation_date = models.DateTimeField(auto_now_add=True)



@receiver(pre_save, sender=User)
def set_user_code(sender, instance, *args, **kwargs):
    if instance.user_code:
        # Obtiene la fecha y hora actual
        current_date = datetime.now()

        # Extrae el año de la fecha actual
        current_year = current_date.year  
        user_code_base = f'{current_year}-'
        counter = 1
        user_code = f'{user_code_base}{counter}'
        while User.objects.filter(user_code=user_code).exists():
            counter += 1
            user_code = f'{user_code_base}{counter}'
        instance.user_code = user_code
