from django.db import models

# Relaciones
from apps.addresses.models import Address
from apps.customers.models import Customer

# Create your models here.
class WorkingInformation(models.Model):
    source_of_income = [
        ('Relación de Dependencia','Relación de Dependencia'),
        ('Negocio Propio', 'Negocio Propio'),
        ('Otra', 'Otra'),
    ]

    employment_status = [
        ('Empleado a Tiempo Completo', 'Empleado a Tiempo Completo'),
        ('Empleado a Tiempo Parcial', 'Empleado a Tiempo Parcial'),
        ('Autónomo', 'Autónomo'), # Trabaja por cuenta propia, no tiene un empleador y puede ofrecer servicios o productos directamente a los clientes.
        ('Desempleado', 'Desempleado'),
        ('Trabajador Temporal', 'Trabajador Temporal'),
        ('Contratista', 'Contratista'),
        ('Freelancer', 'Freelancer'),
        ('Estudiante', 'Estudiante'),
        ('Jubilado', 'Jubilado'), 
        ('Hogar', 'Hogar'), #Persona que se dedica a las tareas del hogar y el cuidado de la familia, y no participa en la fuerza laboral remunerada.
        ('Practicante o Pasante', 'Practicante o Pasante'),
        ('Trabajador a Domicilio', 'Trabajador a Domicilio'), #Empleado que trabaja desde su casa u otro lugar fuera de las instalaciones de la empresa.
        ('Voluntario', 'Voluntario'), #  Realiza trabajo no remunerado, generalmente para una organización sin fines de lucro o para la comunidad.
    ]

    position  = models.CharField(max_length=150, blank=False, null=False) # Puesto
    company_name  = models.CharField(max_length=150, blank=False, null=False)# Nombre de la empresa
    start_date  = models.DateField(blank=True, null=True) # Fecha de inicio
    description  = models.TextField(blank=True, null=True) # Descripcion
    salary  = models.CharField(max_length=70, blank=False, null=False) # Salario
    working_hours  = models.CharField(max_length=70, blank=False, null=False) # Horario de trabajo
    phone_number = models.CharField(max_length=20, blank=False, null=False) # Numero de trabajo
    source_of_income  = models.CharField(max_length=90, choices=source_of_income) # Fuente de ingreso
    income_detail  = models.TextField(blank=True, null=True) # Detalle de ingreso
    employment_status  = models.CharField(max_length=150, choices=employment_status) # Estado Laboral
    address_id = models.ForeignKey(Address, null=False, blank=False, on_delete=models.CASCADE)

class OtherSourcesOfIncome(models.Model):
    source_of_income = models.CharField(max_length=100, blank=False, null=False) # Fuente de ingreso
    nit = models.CharField(max_length=20, blank=False, null=False)
    phone_number = models.CharField(max_length=20, blank=False, null=False) # Numero de trabajo
    address_id = models.ForeignKey(Address, null=False, blank=False, on_delete=models.CASCADE)

class Reference(models.Model):
    reference_type = [
        ('Personales','Personales'),
        ('Laborales','Laborales'),
        ('Comerciales','Comerciales'),
        ('Bancarias','Bancarias'),
    ]

    full_name  = models.CharField(max_length=150, blank=False, null=False) # Nombre Completo
    phone_number = models.CharField(max_length=20, blank=False, null=False) # Numero de telefono de referencia
    reference_type = models.CharField(max_length=100, choices=reference_type) # Tipo de referencia
    customer_id = models.ForeignKey(Customer, null=False, blank=False, on_delete=models.CASCADE)

    