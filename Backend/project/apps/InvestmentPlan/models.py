from django.db import models

# Relaciones
from apps.customers.models import Customer

# Create your models here.
# Signals
from django.db.models.signals import pre_save, post_save

# Django
from django.dispatch import receiver

from apps.financings.formato import formatear_numero

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
    type_of_product_or_service = models.CharField("Tipo de Producto o Servicio", max_length=75,choices=tipo_producto_servicio)
    total_value_of_the_product_or_service = models.DecimalField("Valor Total del Producto o Servicio", max_digits=15, decimal_places=2, blank=False, null=False)
    investment_plan_description = models.TextField("Descripción del Plan de Inversión", blank=True, null=True)
    initial_amount = models.DecimalField("Monto Inicial", max_digits=15, decimal_places=2, blank=False, null=False)
    monthly_amount = models.DecimalField("Monto Mensual", max_digits=15, decimal_places=2, blank=False, null=False)
    transfers_or_transfer_of_funds = models.BooleanField("Transferencias o Traslado de Fondos", blank=False, null=False)
    type_of_transfers_or_transfer_of_funds = models.CharField("Tipo de Transferencia", max_length=75, choices=tipo_transferencia)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    investment_plan_code = models.CharField("Código de Plan de Inversion", max_length=25, blank=False, null=False, unique=True)

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

    def tipo_transferencia(self):
        return 'Local' if self.transfers_or_transfer_of_funds else 'Internacional'

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
