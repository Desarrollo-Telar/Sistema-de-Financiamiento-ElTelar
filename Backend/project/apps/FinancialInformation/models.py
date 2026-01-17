from django.db import models

# Relaciones
from apps.addresses.models import Address
from apps.customers.models import Customer

# Signals
from django.db.models.signals import pre_save, post_save

# Django
from django.dispatch import receiver

# FORMATO
from apps.financings.formato import formatear_numero

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
    creation_date = models.DateTimeField("Fecha de Creación", auto_now_add=True)
    def __str__(self):
        return f"{self.position} - {self.company_name}"
    
    def f_salary(self):
        return formatear_numero(self.salary)
    
    def get_fuente_ingreso(self):
        fuente_ingreso_cliente = ''

        if self.source_of_income != 'Otra':
            fuente_ingreso_cliente = self.source_of_income
        else:
            otra_fuente_ingreso = OtherSourcesOfIncome.objects.filter(customer_id=self.customer_id.id).first()
            fuente_ingreso_cliente = otra_fuente_ingreso.source_of_income

        return fuente_ingreso_cliente
    
    def get_estado_laboral(self):
        estado_laboral_cliente = ''

        if self.source_of_income != 'Otra':
            estado_laboral_cliente = self.employment_status
        else:
            estado_laboral_cliente = 'COMPLETO'

        return estado_laboral_cliente
    
    def get_empresa_laburo(self):
        empresa_laburo_cliente = ''
        if self.source_of_income != 'Otra':
            empresa_laburo_cliente = self.company_name
        else:
            otra_fuente_ingreso = OtherSourcesOfIncome.objects.filter(customer_id=self.customer_id.id).first()
            empresa_laburo_cliente = otra_fuente_ingreso.source_of_income

        return empresa_laburo_cliente
    
    def get_puesto(self):
        puesto_cliente = ''

        if self.source_of_income != 'Otra':
            puesto_cliente = self.position
        else:
            puesto_cliente = 'Otra Fuente de Ingreso'

        return puesto_cliente
        

    class Meta:
        verbose_name = "Información Laboral"
        verbose_name_plural = "Informaciones Laborales"


class OtherSourcesOfIncome(models.Model):
    source_of_income = models.CharField("Fuente de Ingreso", max_length=100, blank=False, null=False)
    nit = models.CharField(max_length=20, blank=False, null=False)
    phone_number = models.CharField("Número de Teléfono", max_length=20, blank=False, null=False)
    salary = models.DecimalField("Salario", max_digits=10, decimal_places=2, blank=False, null=False)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    creation_date = models.DateTimeField("Fecha de Creación", auto_now_add=True)
    def __str__(self):
        return self.source_of_income
    
    def f_salary(self):
        return formatear_numero(self.salary)

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
    creation_date = models.DateTimeField("Fecha de Creación", auto_now_add=True)
    def __str__(self):
        return self.full_name
    
    def get_listado_referencia(self):
        listado_referencias = []
        referencias = Reference.objects.filter(customer_id = self.customer_id.id)
        referencia_s = {}
        for referencia in referencias:
            referencia_s += {
                'nombre_completo': referencia.full_name,
                'telefono': referencia.phone_number,
                'tipo_referencia': referencia.reference_type
            }
            listado_referencias.append(referencia_s)

        return referencia_s

    class Meta:
        verbose_name = "Referencia"
        verbose_name_plural = "Referencias"


@receiver(pre_save, sender=WorkingInformation)
def consultar_working_information(sender, instance, **kwargs):
    customer_id = instance.customer_id
    OtherSourcesOfIncome.objects.filter(customer_id=customer_id).delete()

@receiver(pre_save, sender=OtherSourcesOfIncome)
def consultar_other_sources_of_income(sender, instance, **kwargs):
    customer_id = instance.customer_id
    WorkingInformation.objects.filter(customer_id=customer_id).delete()