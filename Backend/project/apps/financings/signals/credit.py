
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


# PARA CODIGO DEL CREDITO


@receiver(pre_save, sender=Credit)
def pre_save_credito(sender, instance, **kwargs):
    
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
    if created:
        instance.saldo_pendiente = instance.monto
        # CALCULO DE INTERES
        interes = calculo_interes(instance.monto, instance.tasa_interes)
        # GENERACION DE FECHA LIMITE DE PAGO 15 DIAS
        fecha_limite = calcular_fecha_maxima(instance.fecha_inicio)
       
        # FECHA DE VENCIMIENTO
        fecha_vencimiento = calcular_fecha_vencimiento(instance.fecha_inicio)
        
        # GENERAR LA PRIMERA CUOTA
        plan_pago = PaymentPlan(
            credit_id=instance,
            start_date=instance.fecha_inicio, 
            outstanding_balance=instance.monto, 
            saldo_pendiente=instance.monto,
            interest=interes,
            interes_generado=interes,
            fecha_limite = fecha_limite,
            due_date=fecha_vencimiento
            )
        plan_pago.save()