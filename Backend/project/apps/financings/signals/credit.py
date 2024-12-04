
from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.dispatch import receiver

# MODELOS
from apps.financings.models import  Credit, PaymentPlan

# CLASES
from apps.financings.calculos import calcular_fecha_maxima, calcular_fecha_vencimiento, calculo_mora, calculo_interes


# LOOGER
from apps.financings.clases.personality_logs import logger

from datetime import datetime
from dateutil.relativedelta import relativedelta


def codigo(instance):
    if not instance.codigo_credito or instance.codigo_credito == '':
        counter = 1
        customer_code = instance.customer_id.customer_code
        credit_code = f'{customer_code} / {counter}'

        while Credit.objects.filter(codigo_credito=credit_code).exists():
            counter += 1
            credit_code = f'{customer_code} / {counter}'

        instance.codigo_credito = credit_code

    

# LA CREACION DE LA PRIMERA CUOTA DE UN CREDITO
@receiver(post_save, sender=Credit)
def generar_plan_pagos_nuevo(sender, instance, created, **kwargs):
    print('desde signals post save de credit')
    if created:
        codigo(instance)
    

@receiver(post_save, sender=Credit)
def ver_credito(sender, instance, created, **kwargs):
    print('desde signals post save de credit')
    print(instance.estados_fechas)
    # Actualizar solo un campo sin disparar nuevamente la señal
    Credit.objects.filter(pk=instance.pk).update(estados_fechas=instance.estados_fechas)