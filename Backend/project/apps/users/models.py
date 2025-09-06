# Archivo models de modulo

# Librerias de DJANGO
from django.db import models
from django.contrib.auth.models import AbstractUser

# RELACION DE TABLAS
from apps.roles.models import Role, Permiso
from apps.subsidiaries.models import Subsidiary

# TIEMPO
from datetime import datetime, timedelta

# Creacion de todas las tablas para este modulo
from project.database_store import minio_client

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


    
    type_identification = models.CharField("Tipo de Identificación", choices=tipo_identificacion, default='DPI', max_length=50)
    identification_number = models.CharField("Número de Identificación", max_length=50, blank=False, null=False, unique=True)
    telephone = models.CharField("Teléfono", max_length=20, blank=True, null=True)
    email = models.EmailField("Correo Electrónico", unique=True)
    status = models.BooleanField("Estado", default=True)
    gender = models.CharField("Género", choices=genero, default='MASCULINO', max_length=50)
    user_code = models.CharField("Código de Usuario", max_length=50, blank=False, null=False, unique=True)
    nationality = models.CharField("Nacionalidad", max_length=75, blank=False, null=False, default='Guatemala')
    profile_pic = models.ImageField("Foto de Perfil", blank=True, null=True, upload_to='users/profile_pics/')
    rol = models.ForeignKey(Role, on_delete=models.CASCADE, blank=True, null=True)
    creation_date = models.DateTimeField("Fecha de Creación", auto_now_add=True)
    fecha_actualizacion = models.DateField("Fecha en que se actualizo el usuario", default=datetime.now, null=True, blank=True)
    nit = models.CharField(verbose_name="Numero de NIT", max_length=75, blank=True, null=True)
    sucursal = models.ForeignKey(Subsidiary, on_delete=models.SET_NULL, blank=True, null=True)
    #descripcion = models.TextField(verbose_name="Descripcion de usuario", null=True, blank=True)
    #fecha_nacimiento = models.DateField("Fecha de Nacimiento", blank=True, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}' if self.first_name else self.username

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}' if self.first_name else self.username

    def get_status(self):
        return 'Activo' if self.status else 'Inactivo'

    def get_telephone(self):
        return self.telephone if self.telephone else 'Número de teléfono no registrado'
    
    def get_foto_perfil(self):
        
        try:
            url = minio_client.presigned_get_object(
                bucket_name="asiatrip",
                object_name=self.profile_pic.name,
                expires=timedelta(hours=1)
            )
            return url
        except Exception as e:
            return f'Error: {str(e)}'

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

class PermisoUsuario(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario")
    permiso = models.ForeignKey(Permiso, on_delete=models.CASCADE, verbose_name="Permiso de Usuario")

    def __str__(self):
        return f'{self.user} - {self.permiso}'

    class Meta:
        verbose_name = "Permiso de Usuario"
        verbose_name_plural = "Permisos de Usuarios"




    

