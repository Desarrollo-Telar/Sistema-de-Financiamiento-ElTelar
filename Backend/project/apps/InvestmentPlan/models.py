from django.db import models

# Relaciones
from apps.customers.models import Customer
from apps.subsidiaries.models import Subsidiary

# Create your models here.
# Signals
from django.db.models.signals import pre_save, post_save

# Django
from django.dispatch import receiver
from num2words import num2words
from apps.financings.formato import formatear_numero
from dateutil.relativedelta import relativedelta

class InvestmentPlan(models.Model):
    tipo_producto_servicio = [
        ('AGROPECUARIO Y/O PRODUCTIVO', 'AGROPECUARIO Y/O PRODUCTIVO'),
        ('COMERCIO', 'COMERCIO'),
        ('SERVICIOS', 'SERVICIOS'),
        ('CONSUMO', 'CONSUMO'),
        ('VIVIENDA', 'VIVIENDA')

    ]
    tipo_transferencia = [
        ('Local', 'Local'),
        ('Internacional', 'Internacional')
    ]
    formaPago = [
        ('NIVELADA', 'NIVELADA'),
        ('AMORTIZACIONES A CAPITAL', 'AMORTIZACIONES A CAPITAL')
    ]
    type_of_product_or_service = models.CharField("Tipo de Producto o Servicio", max_length=75,choices=tipo_producto_servicio)
    total_value_of_the_product_or_service = models.DecimalField("Valor Total del Producto o Servicio", max_digits=15, decimal_places=2, blank=False, null=False)
    investment_plan_description = models.TextField("Descripción del Plan de Inversión", blank=True, null=True)
    initial_amount = models.DecimalField("Monto Inicial", max_digits=15, decimal_places=2, blank=True, null=True)
    monthly_amount = models.DecimalField("Monto Mensual", max_digits=15, decimal_places=2, blank=True, null=True)
    transfers_or_transfer_of_funds = models.BooleanField("Transferencias o Traslado de Fondos", blank=False, null=False)
    type_of_transfers_or_transfer_of_funds = models.CharField("Tipo de Transferencia", max_length=75, choices=tipo_transferencia)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    investment_plan_code = models.CharField("Código de Plan de Inversion", max_length=25, blank=False, null=False, unique=True)
    
    plazo = models.IntegerField("Plazo", blank=True, null=True)
    tasa_interes = models.DecimalField("Tasa de Interes", max_digits=5, decimal_places=3, null=True, blank=True)
    forma_de_pago = models.CharField("Forma de Pago", choices=formaPago, max_length=75, blank=False, null=False, default='NIVELADA')
    fecha_inicio = models.DateField("Fecha de Inicio", blank=True, null=True)
    fecha_vencimiento = models.DateField("Fecha de Vencimiento", blank=True, null=True)
    sucursal = models.ForeignKey(Subsidiary, on_delete=models.SET_NULL, blank=True, null=True)

    def calcular_fecha_vencimiento(self):
        self.fecha_vencimiento = self.fecha_inicio + relativedelta(months=self.plazo)
        return self.fecha_vencimiento

    def __str__(self):
        return f"{self.type_of_product_or_service} - {self.customer_id}"

    def description(self):
        return self.investment_plan_description or '----'
    
    def transferencias_o_traslado_de_Fondos(self):
        return 'Si' if self.transfers_or_transfer_of_funds else 'No'

    def f_initial_amount(self):
        return formatear_numero(self.initial_amount)

    def f_monthly_amount(self):
        return formatear_numero(self.monthly_amount)
    
    def f_total_value_of_the_product_or_service(self):
        return formatear_numero(self.total_value_of_the_product_or_service)
    
    def en_letras_el_valor(self):
        return num2words(self.total_value_of_the_product_or_service, lang='es')

    def tipo_transferencia(self):
        return 'Local' if self.transfers_or_transfer_of_funds else 'Internacional'
    
    def save(self, *args, **kwargs):
        self.calcular_fecha_vencimiento()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Plan de Inversión"
        verbose_name_plural = "Planes de Inversión"


# Función para generar el código de plan de inversion basado en el Tipo de Producto o Servicio junto a la referencia del codigo de cliente
def generate_investment_plan_code(type_of_product_or_service,customer_code, counter):
    status_suffix = {
        'AGROPECUARIO Y/O PRODUCTIVO': 'A&P',
        'COMERCIO': 'C',
        'SERVICIOS': 'S',
        'CONSUMO': 'C',        
        'VIVIENDA': 'V',
    }
    suffix = status_suffix.get(type_of_product_or_service, '')
    
    return f'{customer_code}/{suffix}{counter}'

@receiver(pre_save, sender=InvestmentPlan)
def set_investment_plan_code(sender, instance, **kwargs):
    customer_code = instance.customer_id.customer_code
    if not instance.investment_plan_code or instance.investment_plan_code == '':
        counter = 1
        investment_plan_code = generate_investment_plan_code(instance.type_of_product_or_service,customer_code, counter)

        # Verificar si no existe un código igual, si no, generar uno nuevo
        while InvestmentPlan.objects.filter(investment_plan_code=investment_plan_code).exists():
            counter += 1
            investment_plan_code = generate_investment_plan_code(instance.type_of_product_or_service,customer_code, counter)

        instance.investment_plan_code = investment_plan_code

    elif instance.pk and InvestmentPlan.objects.filter(pk=instance.pk).exists():
        current_investment_plan = InvestmentPlan.objects.get(pk=instance.pk)

        if current_investment_plan.type_of_product_or_service != instance.type_of_product_or_service:
            counter = 1
            investment_plan_code = generate_investment_plan_code( instance.type_of_product_or_service,customer_code, counter)

            # Verificar si no existe un código igual, si no, generar uno nuevo
            while InvestmentPlan.objects.filter(investment_plan_code=investment_plan_code).exists():
                counter += 1
                investment_plan_code = generate_investment_plan_code(instance.type_of_product_or_service,customer_code, counter)

            instance.investment_plan_code = investment_plan_code
