from django.db import models

# Relaciones
from apps.addresses.models import Address
from apps.customers.models import Customer








class WorkingInformation(models.Model):
    fuente_ingreso = [
        ('Relación de Dependencia', 'Relación de Dependencia'),
        ('Negocio Propio', 'Negocio Propio'),
        ('Otra', 'Otra'),
    ]
    estado_laboral = [
        ('Empleado a Tiempo Completo', 'Empleado a Tiempo Completo'),
        ('Empleado a Tiempo Parcial', 'Empleado a Tiempo Parcial'),
        ('Autónomo', 'Autónomo'), # Self-employed, no employer, can offer services or products directly to customers.
        ('Desempleado', 'Desempleado'),
        ('Trabajador Temporal', 'Trabajador Temporal'),
        ('Contratista', 'Contratista'),
        ('Freelancer', 'Freelancer'),
        ('Estudiante', 'Estudiante'),
        ('Jubilado', 'Jubilado'), 
        ('Hogar', 'Hogar'), # Person dedicated to household tasks and family care, not part of the paid labor force.
        ('Practicante o Pasante', 'Practicante o Pasante'),
        ('Trabajador a Domicilio', 'Trabajador a Domicilio'), # Employee working from home or another location outside company premises.
        ('Voluntario', 'Voluntario'), # Performs unpaid work, usually for a non-profit organization or community.
    ]
    position = models.CharField("Puesto", max_length=150, blank=False, null=False)
    company_name = models.CharField("Nombre de la Empresa", max_length=150, blank=False, null=False)
    start_date = models.DateField("Fecha de Inicio", blank=True, null=True)
    description = models.TextField("Descripción", blank=True, null=True)
    salary = models.DecimalField("Salario", max_digits=10, decimal_places=2, blank=False, null=False)
    working_hours = models.CharField("Horario de Trabajo", max_length=70, blank=False, null=False)
    phone_number = models.CharField("Número de Teléfono", max_length=20, blank=False, null=False)
    source_of_income = models.CharField("Fuente de Ingreso", max_length=90, choices=fuente_ingreso)
    income_detail = models.TextField("Detalle de Ingreso", blank=True, null=True)
    employment_status = models.CharField("Estado Laboral", max_length=150, choices=estado_laboral)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.position} at {self.company_name}"

    class Meta:
        verbose_name = "Información Laboral"
        verbose_name_plural = "Informaciones Laborales"


class OtherSourcesOfIncome(models.Model):
    source_of_income = models.CharField("Fuente de Ingreso", max_length=100, blank=False, null=False)
    nit = models.CharField(max_length=20, blank=False, null=False)
    phone_number = models.CharField("Número de Teléfono", max_length=20, blank=False, null=False)
    salary = models.DecimalField("Salario", max_digits=10, decimal_places=2, blank=False, null=False)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return self.source_of_income

    class Meta:
        verbose_name = "Otra Fuente de Ingreso"
        verbose_name_plural = "Otras Fuentes de Ingreso"

class Reference(models.Model):
    tipo_referencia = [
        ('Personales', 'Personales'),
        ('Laborales', 'Laborales'),
        ('Comerciales', 'Comerciales'),
        ('Bancarias', 'Bancarias'),
    ]
    full_name = models.CharField("Nombre Completo", max_length=150, blank=False, null=False)
    phone_number = models.CharField("Número de Teléfono", max_length=20, blank=False, null=False)
    reference_type = models.CharField("Tipo de Referencia", max_length=100, choices=tipo_referencia)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Referencia"
        verbose_name_plural = "Referencias"


    