from django.db import models

# Relaciones
from apps.users.models import User
from .ocupaciones import Occupation
from .profesiones import Profession
from .condiciones_migratoria import ImmigrationStatus

# Signals
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete

# Django
from django.dispatch import receiver
from django.utils import timezone
import random
from datetime import datetime

# Settings
from project.settings import MEDIA_URL, STATIC_URL

# SEND EMAILS
from project.send_mail import send_email_welcome_customer, send_email_new_customer

from apps.customers.task import nuevo_cliente

# QR
from scripts.generate_qr import generate_qr
from datetime import timedelta
from project.database_store import minio_client
# OS
import os

from django.contrib.sites.models import Site
from django.conf import settings

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


    

def set_null_user():
    return User.objects.get_or_create(identification_number='0000000000000',email='desconocido@gmail.com', username='desconocido', password='desconocido134')[0]

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
        ('Individual (PI)', 'Individual (PI)'),
        ('Juridica (PJ)', 'Juridica (PJ)')
    ]
    status = [
        ('Revisión de documentos', 'Revisión de documentos'),
        ('Aprobado', 'Aprobado'),
        ('No Aprobado', 'No Aprobado'),
        ('Posible Cliente', 'Posible Cliente'),
        ('Dar de Baja', 'Dar de Baja'),
    ]

    escolaridad = [
        ('Ninguna','Ninguna'),
        ('Primaria', 'Primaria'),
        ('Basico', 'Basico'),
        ('Diversificado','Diversificado'),
        ('Superior','Superior')
    ]

    escolaridad_superior = [
        ('Terciario', 'Terciario'),
        ('Universitario', 'Universitario'),
        ('Postgrado', 'Postgrado'),
        ('Ninguna','Ninguna')
    ]
    user_id = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET(set_null_user), verbose_name="Usuario")
    immigration_status_id = models.ForeignKey(ImmigrationStatus, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Condición Migratorio")
    customer_code = models.CharField("Código de Cliente", max_length=25, blank=False, null=False, unique=True)
    first_name = models.CharField("Nombre", max_length=100, blank=False, null=False)
    last_name = models.CharField("Apellido", max_length=100, blank=False, null=False)
    type_identification = models.CharField("Tipo de Identificación", choices=identification, default='DPI', max_length=50)
    identification_number = models.CharField("Número de Identificación", max_length=15, blank=False, null=False, unique=True)
    telephone = models.CharField("Teléfono", max_length=20, blank=True, null=True)
    email = models.EmailField("Correo Electrónico")
    status = models.CharField("Estado", choices=status, default='Posible Cliente', max_length=75)
    date_birth = models.DateField("Fecha de Nacimiento", blank=False, null=False)
    number_nit = models.CharField("NIT", max_length=20, blank=False, null=False, unique=True)
    place_birth = models.CharField("Lugar de Nacimiento", max_length=75, blank=False, null=False)
    marital_status = models.CharField("Estado Civil", max_length=50, blank=False, null=False)
    profession_trade = models.CharField("Profesión u Oficio", max_length=75, blank=True, null=True)
    gender = models.CharField("Género", choices=genders, default='MASCULINO', max_length=50)
    nationality = models.CharField("Nacionalidad", max_length=75, blank=False, null=False, default='Guatemala')
    person_type = models.CharField("Tipo de Persona", choices=type_person, max_length=50, blank=False, null=False)
    description = models.TextField("Observaciones",blank=True, null=True )
    creation_date = models.DateTimeField("Fecha de Creación", auto_now_add=True)
    
    asesor  = models.CharField("Asesor del Credito", max_length=100, blank=True, null=True, default="PENDIENTE")
    fehca_vencimiento_de_tipo_identificacion = models.DateField("Fecha de Vencimiento del Tipo de Identificacion", blank=True, null=True,default=datetime.now)
    # NUEVOS CAMPOS
    other_telephone = models.CharField("Otro Numero de Teléfono", max_length=20, blank=True, null=True)
    level_of_education = models.CharField("Nivel de Escolaridad",max_length=100, choices=escolaridad, default='Ninguna', blank=True, null=True)
    level_of_education_superior = models.CharField("Nivel de Escolaridad Superior", max_length=100, choices=escolaridad_superior, default='Ninguna',blank=True, null=True)
    ocupacion = models.ForeignKey(Occupation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Ocupacion")
    profesion = models.ForeignKey(Profession,  on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Profesion")

    def __str__(self):
        return self.get_full_name()

    

    def get_qr(self):
        filename = f'qr/codigoQr_{self.customer_code}.png'
        try:
            url = minio_client.presigned_get_object(
                bucket_name="asiatrip",
                object_name=filename,
                expires=timedelta(hours=1)
            )
            return url
        except Exception as e:
            return f'Error: {str(e)}'
    
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def get_edad(self):
        today = datetime.date.today()
        age = today.year - self.date_birth.year
        if (today.month, today.day) < (self.date_birth.month, self.date_birth.day):
            age -= 1
        return age


    
    
    def fecha_creacion(self):
        
        return self.creation_date.strftime('%d de %B de %y')

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    

# Función para generar el código de cliente basado en el estado y año actual
def generate_customer_code(status, current_year, counter):
    status_suffix = {
        'Posible Cliente': 'S',
        'No Aprobado': 'N',
        'Aprobado': '',
        'Revisión de documentos': 'D',
        'Dar de Baja': 'E',
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

@receiver(post_save, sender=Customer)
def send_message(sender, instance, created, **kwargs):
    customer = instance
    current_site = Site.objects.get_current()
    domain = current_site.domain

    # Verifica si está en HTTPS o HTTP basándose en la configuración
    protocol = 'https' if settings.SECURE_SSL_REDIRECT else 'http'
    
    # Construir la URL completa con el protocolo y el dominio
    filename = f'codigoQr_{customer.customer_code}.png'
    dato = f'{protocol}://{domain}/pdf/{customer.id}/'
    
    generate_qr(dato, filename)

    if created:
        send_email_new_customer(instance)

@receiver(post_delete, sender=Customer)
def delete_image_qr_customer(sender, instance, **kwargs):
    bucket_name = 'asiatrip'
    object_name = f'qr/codigoQr_{instance.customer_code}.png'

    try:
        minio_client.remove_object(bucket_name, object_name)
        print('QR eliminado de MinIO')
    except Exception as e:
        print(f'Error al eliminar QR de MinIO: {str(e)}')
    
