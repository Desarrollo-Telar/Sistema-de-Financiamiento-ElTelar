from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

# MODELOS
from .models import Payment, AccountStatement, Credit, PaymentPlan, Banco

# FUNCIONALIDADES
from .functions import realizar_pago

# CLASES
from apps.financings.clases import credit as Credito
from apps.financings.clases import paymentplan as PlanPago

""" 
@receiver(post_save, sender=Payment)
def registrar_pago_en_estado_de_cuenta(sender, instance, created, **kwargs):
    
    if created:
        realizar_pago(instance.credit, instance.fecha_emision, instance.monto, instance)

"""
@receiver(post_save, sender=Banco)
def validar_con_pagos(sender,instance,created,**kwargs):
    if created:
        pagos = Payment.objects.filter(numero_referencia=instance.referencia)

# Señales
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
        instance.saldo_pendiente = instance.monto

@receiver(post_save, sender=Credit)
def generar_plan_pagos(sender, instance, created, **kwargs):
    if created:
        credito = Credito(instance.proposito, instance.monto, instance.plazo, instance.forma_de_pago, instance.frecuecia_pago, instance.fecha_inicio, instance.tipo_credito, instance.customer_id)
        pago = PlanPago(credito)
        pcapital = pago.recalcular_capital()
        cuota = 0
        fecha_vencimiento = 0
        for ca in pcapital:
            cuota = ca['cuota']
            
            break


        plan_pago = PaymentPlan(credit_id=instance,start_date=instance.fecha_inicio, outstanding_balance=instance.monto, saldo_pendiente=instance.monto, installment=cuota)
        plan_pago.save()
     