from django.db import models

# Relaciones
from apps.users.models import User

# Signals
from django.db.models.signals import pre_save

# Django
from django.dispatch import receiver
from django.utils import timezone
import random

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

    def __str__(self):
        return self.condition_name
    


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
    status = [
        ('Revisión de documentos', 'Revisión de documentos'),
        ('Aprobado', 'Aprobado'),
        ('No Aprobado', 'No Aprobado'),
        ('Posible Cliente', 'Posible Cliente'),
    ]

    user_id = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE)
    immigration_status_id = models.ForeignKey(ImmigrationStatus, blank=False, null=False, on_delete=models.CASCADE)
    customer_code = models.CharField(max_length=25, blank=False, null=False, unique=True)
    first_name = models.TextField(max_length=100, blank=False, null=False) #
    last_name = models.TextField(max_length=100, blank=False, null=False) #
    type_identification = models.CharField(choices=identification, default='DPI', max_length=50 ) #
    identification_number = models.CharField(max_length=15, blank=False, null=False, unique=True) #
    telephone = models.CharField(max_length=20, blank=True, null=True) #
    email = models.EmailField(unique=True) #
    status = models.CharField(choices=status, default='Posible Cliente', max_length=75)
    date_birth = models.DateField() #
    number_nit = models.CharField(max_length=20, blank=False, null=False, unique=True) # NIT
    place_birth = models.CharField(max_length=75, blank=False, null=False) # Lugar de nacimiento #
    marital_status =  models.CharField(max_length=50, blank=False, null=False)   # Estado civil #
    profession_trade = models.CharField(max_length=75, blank=False, null=False) # Profesion u oficio #
    gender = models.CharField(choices=genders, default='MASCULINO', max_length=50) #
    nationality = models.CharField(max_length=75, blank=False, null=False, default='Guatemala') #
    person_type = models.CharField(choices=type_person, max_length=50) #
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} {} / {}'.format(self.first_name, self.last_name,self.customer_code)
    

#Funcion clave para la generacion de codigos de clientes luego de haberse creado
@receiver(pre_save, sender=Customer)
def set_customer_code(sender, instance, *args, **kwargs):
    if instance.customer_code == '':
        # Obtiene la fecha y hora actual
        current_date = datetime.now()

        # Extrae el año de la fecha actual
        current_year = current_date.year  

        # Formato al codigo de usuario
        customer_code_base = f'{current_year}-'

        # Contador
        counter = 1

        # Base final del codigo
        # Ejemplo: 2024-1
        customer_code = f'{customer_code_base}{counter}'

        # Verificar si no existe un codigo igual, si no generar uno nuevo
        while Customer.objects.filter(customer_code=customer_code).exists():
            counter += 1
            customer_code = f'{customer_code_base}{counter}'
            print(instance.customer_code)

        # Guardar informacion
        instance.customer_code = customer_code