from django.db import models

# Relaciones
from apps.users.models import User

# Create your models here.
condition = [
        ('Residente temporal','Residente temporal'),
        ('Turista o visitante','Turista o visitante'),
        ('Residente permanente','Residente permanente'),
        ('Permiso de trabajo','Permiso de trabajo'),
        ('Persona en tránsito','Persona en tránsito'),
        ('Permiso consular o similar','Permiso consular o similar'),
        ('Otra','Otra'),
    ]

class ImmigrationStatus(models.Model):
    condition_name = models.CharField(max_length=50, blank=False, null=False, unique=True)
    description = models.TextField()


class Customer(models.Model):
    identification = [
        ('DPI', 'DPI'),
        ('PASAPORTE', 'PASAPORTE'),
        ('OTRO', 'OTRO')
    ]
    genders = [
        ('MASCULINO', 'MASCULINO'),
        ('FEMENINO', 'FEMENINO')
    ]
    type_person = [
        ('Indivicual (PI)', 'Indivicual (PI)'),
        ('Juridica (PJ)', 'Juridica (PJ)')
    ]

    user_id = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE)
    immigration_status_id = models.ForeignKey(ImmigrationStatus, blank=False, null=False, on_delete=models.CASCADE)
    customer_code = models.CharField(max_length=25, blank=False, null=False, unique=True)
    first_name = models.TextField(max_length=100, blank=False, null=False)
    last_name = models.TextField(max_length=100, blank=False, null=False)
    type_identification = models.CharField(choices=identification, default='DPI', max_length=50 )
    identification_number = models.CharField(max_length=15, blank=False, null=False, unique=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    date_birth = models.DateField()
    number_nit = models.CharField(max_length=20, blank=False, null=False, unique=True)
    place_birth = models.CharField(max_length=75, blank=False, null=False) # Lugar de nacimiento
    marital_status =  models.CharField(max_length=50, blank=False, null=False)   # Estado civil
    profession_trade = models.CharField(max_length=75, blank=False, null=False) # Profesion u oficio
    gender = models.CharField(choices=genders, default='MASCULINO', max_length=50)
    nationality = models.CharField(max_length=75, blank=False, null=False, default='Guatemala')
    person_type = models.CharField(choices=type_person, max_length=50)
    creation_date = models.DateTimeField(auto_now_add=True)