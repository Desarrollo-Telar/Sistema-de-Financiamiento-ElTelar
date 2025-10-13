
from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.dispatch import receiver

# MODELOS
from apps.financings.models import  Credit, PaymentPlan

# CLASES
from apps.financings.calculos import calcular_fecha_maxima, calcular_fecha_vencimiento, calculo_mora, calculo_interes

# MENSAJES
from project.send_mail import send_email_new_credit

# LOOGER
from apps.financings.clases.personality_logs import logger

from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.db.models import Q, Sum


def codigo(instance):
    if not instance.codigo_credito or instance.codigo_credito == '':
        counter = 1
        customer_code = instance.customer_id.customer_code
        credit_code = f'{customer_code} / {counter}'

        while Credit.objects.filter(codigo_credito=credit_code).exists():
            counter += 1
            credit_code = f'{customer_code} / {counter}'

        instance.codigo_credito = credit_code

    
@receiver(pre_save, sender=Credit)
def generar_codigo(sender, instance, **kwargs):
    codigo(instance)
    instance.fecha_actualizacion = datetime.now().date()

# LA CREACION DE LA PRIMERA CUOTA DE UN CREDITO
@receiver(post_save, sender=Credit)
def generar_plan_pagos_nuevo(sender, instance, created, **kwargs):
    if not created:
        return  # solo se ejecuta al crear un crédito nuevo

    # Calcular valores base
    interes = calculo_interes(instance.monto, instance.tasa_interes)
    fecha_limite = calcular_fecha_maxima(instance.fecha_inicio)
    fecha_vencimiento = calcular_fecha_vencimiento(instance.fecha_inicio)

    # Asignar asesor si no tiene
    if instance.asesor_de_credito is None and hasattr(instance.customer_id, "new_asesor_credito"):
        instance.asesor_de_credito = instance.customer_id.new_asesor_credito
        instance.save(update_fields=["asesor_de_credito"])  # actualiza solo ese campo

    # Crear el plan de pago inicial
    PaymentPlan.objects.create(
        credit_id=instance,
        start_date=instance.fecha_inicio,
        outstanding_balance=instance.monto,
        saldo_pendiente=instance.monto,
        interest=interes,
        interes_generado=interes,
        fecha_limite=fecha_limite,
        due_date=fecha_vencimiento,
        sucursal=instance.sucursal
    )

    # Enviar notificación por correo
    send_email_new_credit(instance)
    
