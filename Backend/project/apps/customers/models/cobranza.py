# Models
from django.db import models

# Relacion
from apps.customers.models import CreditCounselor, Customer
from apps.financings.models import PaymentPlan, Credit

# TIEMPO
from datetime import datetime

# SIGNALS
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

tipos_cobranzas = [
    'Cobranza Preventiva',
    'Cobranza Administrativa',
    'Cobranza Extrajudicial',
    'Cobranza Judicial',
    'Cobranza domiciliaria',
]

tipos_gestion = [
    'correo electronico',
    'llama telefonica',

]

class Cobranza(models.Model):
    credito = models.ForeignKey(Credit, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Credito Asociado")
    asesor_credito = models.ForeignKey(CreditCounselor, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Responsable de Seguimiento")
    cuota = models.ForeignKey(PaymentPlan, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Cuota de Seguimiento")
    tipo_cobranza = models.CharField(verbose_name="Tipo de Cobranza", max_length=100, default="Preventiva")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")
    fecha_gestion = models.DateField(verbose_name="Fecha de Gestion", default=datetime.date())
    tipo_gestion = models

    class Meta:
        verbose_name = 'Cobranza'
        verbose_name_plural = 'Cobranzas'