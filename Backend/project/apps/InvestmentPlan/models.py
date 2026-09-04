from django.db import models
import uuid

# Relaciones
from apps.customers.models import Customer, CreditCounselor 
from apps.subsidiaries.models import Subsidiary
from apps.users.models import User

# Create your models here.
# Signals
from django.db.models.signals import pre_save, post_save
# DECIMAL
from decimal import Decimal
from datetime import datetime
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
        ('AMORTIZACIONES A CAPITAL', 'AMORTIZACIONES A CAPITAL'),
        ('INTERES MENSUAL Y CAPITAL AL VENCIMIENTO', 'INTERES MENSUAL Y CAPITAL AL VENCIMIENTO'),
        ('INTERES Y CAPITAL AL VENCIMIENTO', 'INTERES Y CAPITAL AL VENCIMIENTO')
    ]

    type_of_product_or_service = models.CharField("Tipo de Producto o Servicio", max_length=75,choices=tipo_producto_servicio)
    total_value_of_the_product_or_service = models.DecimalField("Valor Total del Producto o Servicio", max_digits=15, decimal_places=2, blank=False, null=False)
    investment_plan_description = models.TextField("Descripción del Plan de Inversión", blank=True, null=True)
    initial_amount = models.DecimalField("Monto Inicial", max_digits=15, decimal_places=2, blank=True, null=True)
    monthly_amount = models.DecimalField("Monto Mensual", max_digits=15, decimal_places=2, blank=True, null=True)
    transfers_or_transfer_of_funds = models.BooleanField("Transferencias o Traslado de Fondos", blank=True, null=True)
    type_of_transfers_or_transfer_of_funds = models.CharField("Tipo de Transferencia", max_length=75, choices=tipo_transferencia,blank=True, null=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    investment_plan_code = models.CharField("Código de Plan de Inversion", max_length=25, blank=False, null=False, unique=True)
    
    plazo = models.IntegerField("Plazo", blank=True, null=True)
    tasa_interes = models.DecimalField("Tasa de Interes", max_digits=8, decimal_places=3, null=True, blank=True)
    forma_de_pago = models.CharField("Forma de Pago", choices=formaPago, max_length=75, blank=False, null=False, default='NIVELADA')
    fecha_inicio = models.DateField("Fecha de Inicio", blank=True, null=True)
    fecha_vencimiento = models.DateField("Fecha de Vencimiento", blank=True, null=True)
    sucursal = models.ForeignKey(Subsidiary, on_delete=models.SET_NULL, blank=True, null=True)

    fiador = models.JSONField(null=True, blank=True, verbose_name="Fiador")
    credito_anterior_vigente = models.JSONField(null=True, blank=True, verbose_name="Credito Anterior Vigente")
    tipo_pagare = models.CharField(verbose_name="Tipo de pagare", max_length=150, blank=True, null=True)
    creation_date = models.DateTimeField("Fecha de Creación", auto_now_add=True)

    plazo_gracia =  models.IntegerField("Plazo de Gracia", blank=True, null=True)
    fecha_finalizacion_gracia = models.DateField("Fecha de Finalizacion de Gracia",blank=True, null=True)

    tipo_documento = models.CharField("Tipo de documento", max_length=75, blank=True, null=True, default='PAGARE')
    asesor_responsable = models.ForeignKey(CreditCounselor, on_delete=models.SET_NULL, null=True, blank=True)
    estado_aprobacion  = models.CharField("Estado de Aprobacion", max_length=75, blank=True, null=True)
    garantias = models.JSONField(null=True, blank=True, verbose_name="Garantias de la Solicitud de Credito")
    notarios = models.JSONField(null=True, blank=True, verbose_name="Notarios")
    riesgo_comercial = models.TextField("Riesgo Comercial", blank=True, null=True)
    diganostico_oportunidad = models.TextField("Diagnóstico de Oportunidades", blank=True, null=True)
    mitigadores = models.TextField("Mitigadores", blank=True, null=True)
    evaluacion_mercado = models.TextField("Evaluación del Mercado", blank=True, null=True)

    
    def fecha_primer_pago(self):
        
        return self.fecha_inicio + relativedelta(months=1)

    

    def get_tasa(self):
        tasa_interes = self.tasa_interes if self.tasa_interes else 0

        if tasa_interes == 0:
            return 0
        
        calculo = Decimal(tasa_interes) / Decimal(12)

        return formatear_numero(round(calculo,  2))

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

    def listado_de_notarios(self):
        notarios_lista = self.notarios or []

        if not notarios_lista:
            return None
        
        ids_notarios = [notario.get('id') for notario in notarios_lista if notario.get('id')]
        
        ids_unicos = set(ids_notarios)
        return ids_unicos

    def tengo_expediente(self):
        exped = ExpedientePlanNotario.objects.filter(investment_plan=self)
        notarios = self.listado_de_notarios()

        if exped and notarios and self.estado_aprobacion == 'ACEPTADO':
            return True
        return False
        
    
    


    class Meta:
        verbose_name = "Plan de Inversión"
        verbose_name_plural = "Planes de Inversión"




class ExpedientePlanNotario(models.Model):
    investment_plan = models.ForeignKey(InvestmentPlan, on_delete=models.CASCADE)
    notario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    asunto_expediente = models.TextField("Asunto del Expediente", blank=True, null=True)

    def __str__(self):
        return f"Expediente de Plan de Inversión: {self.investment_plan} - Notario: {self.notario} - {self.uuid}"

    class Meta:
        verbose_name = "Expediente Plan Notario"
        verbose_name_plural = "Expedientes Plan Notarios"


import re

def validar_codigo(codigo: str) -> bool:
    patron = r"^0\d{1,2}-IIT0[1-9]\d*-\d{4}$"
    return bool(re.match(patron, codigo))


# Función para generar el código de plan de inversion basado en el Tipo de Producto o Servicio junto a la referencia del codigo de cliente
def generate_investment_plan_code(sucursal, counter):
    current_date = datetime.now()
    current_year = current_date.year 

    codigo_establecimiento = sucursal.codigo_establecimiento
    
    return f'0{codigo_establecimiento}-IIT0{counter}-{current_year}'

def generar_codigo(instance):
    counter = 1
    investment_plan_code = generate_investment_plan_code(instance.sucursal, counter)

        # Verificar si no existe un código igual, si no, generar uno nuevo
    while InvestmentPlan.objects.filter(investment_plan_code=investment_plan_code).exists():
        counter += 1
        investment_plan_code = generate_investment_plan_code(instance.sucursal, counter)

    instance.investment_plan_code = investment_plan_code


@receiver(pre_save, sender=InvestmentPlan)
def set_investment_plan_code(sender, instance, **kwargs):
    
    if not instance.investment_plan_code or instance.investment_plan_code == '':
        generar_codigo(instance)
        

    elif instance.pk and InvestmentPlan.objects.filter(pk=instance.pk).exists():
        current_investment_plan = InvestmentPlan.objects.get(pk=instance.pk)

        if current_investment_plan.type_of_product_or_service != instance.type_of_product_or_service:
            generar_codigo(instance)
        
        if not validar_codigo(instance.investment_plan_code):
            generar_codigo(instance)


@receiver(post_save, sender=InvestmentPlan)
def handle_investment_plan_approval(sender, instance, created, **kwargs):
    from apps.users.models import User
    from project.send_mail.correos_para_notarios import send_email_notario

    if instance.estado_aprobacion != "ACEPTADO":
        return

    if not instance.notarios:
        return

    ids_unicos = {
        notario["id"]
        for notario in instance.notarios
        if notario.get("id")
    }

    for id_notario in ids_unicos:
        try:
            user_notario = User.objects.get(id=id_notario)

            expediente, creado = ExpedientePlanNotario.objects.get_or_create(
                investment_plan=instance,
                notario=user_notario
            )

            if not creado:
                continue

            send_email_notario(
                user=user_notario,
                plan_inversion_id=instance.id,
                formato="formato_01",
                uuid=expediente.uuid
            )

        except User.DoesNotExist:
            continue


