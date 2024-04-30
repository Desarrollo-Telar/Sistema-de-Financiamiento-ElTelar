from django.db import models
from django.contrib.auth.models import AbstractUser



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
    creation_date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    gender = models.CharField(choices=genders, default='MASCULINO', max_length=50)
    user_code = models.CharField(max_length=25, blank=False, null=False, unique=True)
    nationality = models.CharField(max_length=75, blank=False, null=False, default='Guatemala')
    profile_pic = models.ImageField(upload_to='users/profile_pics/')
    created_at = models.DateTimeField(auto_now_add=True)
    
