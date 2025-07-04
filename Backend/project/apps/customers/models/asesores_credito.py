from django.db import models

# Relacion
from apps.users.models import User

# TIEMPO
from datetime import datetime

# SIGNALS
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

# TIEMPO
from datetime import datetime

class CreditCounselor(models.Model):
    tipo_identificacion = [
        ('DPI', 'DPI'),
        ('PASAPORTE', 'PASAPORTE'),
        ('OTRO', 'OTRO')
    ]

    genero = [
        ('MASCULINO', 'MASCULINO'),
        ('FEMENINO', 'FEMENINO')
    ]

    usuario = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True)
    nombre = models.CharField("Nombre del Asesor", max_length=150, blank=True, null=True)
    apellido = models.CharField("Apellido del Asesor", max_length=150, blank=True, null=True)
    codigo_asesor = models.CharField("Código de Asesor", max_length=50, blank=False, null=False, unique=True)
    type_identification = models.CharField("Tipo de Identificación", choices=tipo_identificacion, default='DPI', max_length=50)
    identification_number = models.CharField("Número de Identificación", max_length=15, blank=False, null=False, unique=True)
    telephone = models.CharField("Teléfono", max_length=20, blank=True, null=True)
    email = models.EmailField("Correo Electrónico", unique=True)
    profile_pic = models.ImageField("Foto de Perfil", blank=True, null=True, upload_to='asesor/profile_pics/')
    creation_date = models.DateTimeField("Fecha de Creación", auto_now_add=True)
    fecha_actualizacion = models.DateField("Fecha en que se actualizo el usuario", default=datetime.now, null=True, blank=True)
    status = models.BooleanField("Estado", default=True)
    gender = models.CharField("Género", choices=genero, default='MASCULINO', max_length=50)
    nit = models.CharField(verbose_name="Numero de NIT", max_length=75, blank=True, null=True)


    class Meta:
        verbose_name = 'Asesor de Crédito'
        verbose_name_plural = 'Asesores de Credito'
    
# Funcion clave para la generacion de codigos de usuario, luego de haberse creado
@receiver(pre_save, sender=CreditCounselor)
def set_user_code(sender, instance, *args, **kwargs):
    if instance.codigo_asesor == '':
        # Obtiene la fecha y hora actual
        current_date = datetime.now()

        # Extrae el año de la fecha actual
        current_year = current_date.year  

        # Formato al codigo de usuario
        user_code_base = f'{current_year}-A'

        # Contador
        counter = 1

        # Base final del codigo
        # Ejemplo: 2024-A1
        user_code = f'{user_code_base}{counter}'

        # Verificar si no existe un codigo igual, si no generar uno nuevo
        while CreditCounselor.objects.filter(codigo_asesor=user_code).exists():
            counter += 1
            user_code = f'{user_code_base}{counter}'
            print(instance.codigo_asesor)

        # Guardar informacion
        instance.codigo_asesor = user_code
    
    if instance.usuario is not None:
        instance.nombre = instance.usuario.first_name
        instance.apellido = instance.usuario.last_name
        instance.type_identification = instance.usuario.type_identification
        instance.identification_number = instance.usuario.identification_number
        instance.telephone = instance.usuario.telephone
        instance.email = instance.usuario.email
        instance.gender = instance.usuario.gender
        instance.nit = instance.usuario.nit
       