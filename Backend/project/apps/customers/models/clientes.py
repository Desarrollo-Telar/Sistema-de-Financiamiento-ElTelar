from django.db import models

# Relaciones
from apps.users.models import User
from .ocupaciones import Occupation
from .profesiones import Profession
from .condiciones_migratoria import ImmigrationStatus
from .asesores_credito import CreditCounselor
from apps.subsidiaries.models import Subsidiary


# Django
from datetime import datetime
from datetime import timedelta
from project.database_store import minio_client

import uuid
from math import floor
from num2words import num2words

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
    identification_number = models.CharField("Número de Identificación", max_length=50, blank=False, null=False, unique=True)
    telephone = models.CharField("Teléfono", max_length=50, blank=True, null=True)
    email = models.EmailField("Correo Electrónico")
    status = models.CharField("Estado", choices=status, default='Posible Cliente', max_length=75)
    date_birth = models.DateField("Fecha de Nacimiento", blank=False, null=False)
    number_nit = models.CharField("NIT", max_length=50, blank=False, null=False, unique=True)
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
    
    other_telephone = models.CharField("Otro Numero de Teléfono", max_length=20, blank=True, null=True)
    level_of_education = models.CharField("Nivel de Escolaridad",max_length=100, choices=escolaridad, default='Ninguna', blank=True, null=True)
    level_of_education_superior = models.CharField("Nivel de Escolaridad Superior", max_length=100, choices=escolaridad_superior, default='Ninguna',blank=True, null=True)
    ocupacion = models.ForeignKey(Occupation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Ocupacion")
    profesion = models.ForeignKey(Profession,  on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Profesion")
    new_asesor_credito = models.ForeignKey(CreditCounselor, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Asesor de este Credito")

    uuid = models.UUIDField(verbose_name="Token Cliente",default=uuid.uuid4,  blank=True, null=True)
    completado = models.BooleanField(verbose_name="Estado de Registro", default=True)

    lugar_emision_tipo_identificacion_departamento = models.CharField(verbose_name="Lugar de Emision (Departamento)", max_length=100, blank=True, null=True, default='Alta Verapaz')
    lugar_emision_tipo_identificacion_municipio = models.CharField(verbose_name="Lugar de Emision (Municipio)", max_length=100, blank=True, null=True, default='Cobán')

    # NUEVOS CAMPOS
    valoracion = models.DecimalField(verbose_name="Puntuacion del cliente", decimal_places=2, max_digits=15, blank=True, null=True, default=0)
    sucursal = models.ForeignKey(Subsidiary, on_delete=models.SET_NULL, blank=True, null=True)
    numero_identificacion_sucursal = models.CharField(verbose_name="Numero de Identificacion Sucursal por Cliente", max_length=150, blank=True, null=True)
    
    def __str__(self):
        return self.get_full_name()

    def get_email_customer():
        pass
        

    def get_nit_customer():
        pass
    

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
    
    def get_estado_civil(self):
        estado = self.marital_status
        genero = self.gender  # 'M' o 'F'

        if not estado:
            return estado

        if '@' in estado:
            if genero == 'MASCULINO':
                return estado.replace('@', 'O')
            elif genero == 'FEMENINO':
                return estado.replace('@', 'A')

        return estado
    
    def get_nacionalidad(self):
        genero = self.gender
        if genero == 'MASCULINO':
            return 'guatemalteco'
        elif genero == 'FEMENINO':
            return 'guatemalteca'

    def get_edad(self):
        from datetime import date
        """
        Calcula la edad de la persona en base a su fecha de nacimiento.
        Devuelve None si la fecha de nacimiento no está definida.
        """
        if not self.date_birth:
            return None  # O 0, según cómo quieras manejarlo

        today = date.today()
        age = today.year - self.date_birth.year

        # Si aún no ha llegado su cumpleaños este año, restamos 1
        if (today.month, today.day) < (self.date_birth.month, self.date_birth.day):
            age -= 1

        return age
    
    
    def get_edad_en_letras(self):
        # CONVERTIR LOS NUMEROS A LETRAS
        
        edad = num2words(self.get_edad(),lang='es')
        return edad
    
    def formato_identificicaion(self):
        num = str(self.identification_number).replace(" ", "").strip()
        if len(num) == 13:
            return f"{num[0:4]} {num[4:9]} {num[9:13]}"
        return num  # Si no tiene 13 dígitos, lo devuelve igual
    
    def get_numero_identificacion_en_letras(self):
        num = str(self.identification_number).replace(" ", "").strip()
        if len(num) == 13:
            
            return f"{num2words(num[0:4],lang='es')}, {num2words(num[4:9],lang='es')}, {num2words(num[9:13],lang='es')}"
        
        return num2words(num,lang='es')  # Si no tiene 13 dígitos, lo devuelve igual
    
    def get_star_rating(self):

        estrellas = []
        if self.valoracion is None:
            valor = 0
        else:
            valor = float(self.valoracion)

        enteras = floor(valor)              # Número de estrellas llenas
        decimal = valor - enteras           # Parte decimal para media estrella

        for i in range(1, 6):
            if i <= enteras:
                estrellas.append('full')
            elif i == enteras + 1 and decimal >= 0.5:
                estrellas.append('half')
            else:
                estrellas.append('empty')

        return estrellas
    
    def get_direccion(self):
        from apps.addresses.models import Address
        from django.db.models import Q
        tipo_direccion = ['Dirección Personal','Dirección de Casa', 'Direccin Personal']

        direccion = Address.objects.filter(Q(customer_id__id=self.id) & Q(type_address__in = tipo_direccion)).first()

        if direccion is None:
            return ''
        
        return direccion

    
    
    def fecha_creacion(self):
        
        return self.creation_date.strftime('%d de %B de %y')

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    

