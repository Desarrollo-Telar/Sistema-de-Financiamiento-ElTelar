
from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.dispatch import receiver

# MODELOS
from apps.accountings.models import Insurance
from apps.financings.models import PaymentPlan

# CLASES
from apps.financings.calculos import calcular_fecha_maxima, calcular_fecha_vencimiento, calculo_mora, calculo_interes


# LOOGER
from apps.financings.clases.personality_logs import logger

from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.db.models import Q, Sum

from datetime import datetime

def codigo_seg(instance):
    if not instance.codigo_seguro or instance.codigo_seguro == '':
        counter = 1
        current_date = datetime.now()
        current_year = current_date.year
        
        codigo_acreedor = f'SEG-{current_year}-{counter}'

        while Insurance.objects.filter(codigo_seguro=codigo_acreedor).exists():
            counter += 1
            codigo_acreedor = f'SEG-{current_year}-{counter}'

        instance.codigo_seguro = codigo_acreedor

    
@receiver(pre_save, sender=Insurance)
def generar_codigo_s(sender, instance, **kwargs):
    codigo_seg(instance)

# LA CREACION DE LA PRIMERA CUOTA DE UN CREDITO
@receiver(post_save, sender=Insurance)
def generar_plan_pagos_nuevo_s(sender, instance, created, **kwargs):
    print('desde signals post save de credit, de la funcion generar plan de pagos nuevos')
    if created:
        # CALCULO DE INTERES
        interes = calculo_interes(instance.monto, instance.tasa)
        # GENERACION DE FECHA LIMITE DE PAGO 15 DIAS
        fecha_limite = calcular_fecha_maxima(instance.fecha_inicio)
       
        # FECHA DE VENCIMIENTO
        fecha_vencimiento = calcular_fecha_vencimiento(instance.fecha_inicio)
        
    
        # GENERAR LA PRIMERA CUOTA
        plan_pago = PaymentPlan(
            seguro=instance,
            start_date=instance.fecha_inicio, 
            outstanding_balance=instance.monto, 
            saldo_pendiente=instance.monto,
            interest=interes,
            interes_generado=interes,
            fecha_limite = fecha_limite,
            due_date=fecha_vencimiento
            )
        plan_pago.save()
    

@receiver(post_save, sender=Insurance)
def ver_scredito(sender, instance, created, **kwargs):
    print('desde signals post save de credit de la funcion ver el credito')
    print(instance.estados_fechas)
    # Actualizar solo un campo sin disparar nuevamente la señal
    #Credit.objects.filter(pk=instance.pk).update(estados_fechas=instance.estados_fechas)