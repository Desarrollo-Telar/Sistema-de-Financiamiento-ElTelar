from django.db import models

# Relaciones
from apps.users.models import User

# Signals
from django.db.models.signals import pre_save

# Django
from django.dispatch import receiver
from django.utils import timezone
import random
from datetime import datetime

# Settings
from project.settings import MEDIA_URL, STATIC_URL

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
    description = models.TextField(blank=True, null=True)

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

    def get_qr(self):
        codigo = '/media/qr/codigoQr_{}.png'.format(self.customer_code)
        if not codigo:
            return 'No hay info'
        
        

        return codigo


    def __str__(self):
        return '{} {} / {}'.format(self.first_name, self.last_name,self.customer_code)
    

# Función para generar el código de cliente basado en el estado y año actual
def generate_customer_code(status, current_year, counter):
    status_suffix = {
        'Posible Cliente': 'S',
        'No Aprobado': 'N',
        'Aprobado': '',
        'Revisión de documentos': 'D'
    }
    suffix = status_suffix.get(status, '')
    return f'{current_year}-{suffix}{counter}'

@receiver(pre_save, sender=Customer)
def set_customer_code_and_update_status(sender, instance, **kwargs):
    # Si el código del cliente está vacío o es una cadena vacía, genera uno nuevo
    if not instance.customer_code or instance.customer_code == '':
        current_date = datetime.now()
        current_year = current_date.year
        counter = 1
        
        # Generar el código base
        customer_code = generate_customer_code(instance.status, current_year, counter)

        # Verificar si no existe un código igual, si no, generar uno nuevo
        while Customer.objects.filter(customer_code=customer_code).exists():
            counter += 1
            customer_code = generate_customer_code(instance.status, current_year, counter)

        instance.customer_code = customer_code

    # Si el cliente ya existe, verificar si el estado ha cambiado
    elif instance.pk and Customer.objects.filter(pk=instance.pk).exists():
        current_customer = Customer.objects.get(pk=instance.pk)
        if current_customer.status != instance.status:
            current_date = datetime.now()
            current_year = current_date.year
            counter = 1
            
            # Generar el código base
            customer_code = generate_customer_code(instance.status, current_year, counter)

            # Verificar si no existe un código igual, si no, generar uno nuevo
            while Customer.objects.filter(customer_code=customer_code).exists():
                counter += 1
                customer_code = generate_customer_code(instance.status, current_year, counter)

            instance.customer_code = customer_code