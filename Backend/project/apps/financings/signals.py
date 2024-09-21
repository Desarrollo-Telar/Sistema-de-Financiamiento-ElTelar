from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

# MODELOS
from .models import Payment, AccountStatement, Credit, PaymentPlan, Banco, Recibo

# FUNCIONALIDADES
from .functions import realizar_pago

# CLASES
from apps.financings.clases import credit as Credito
from apps.financings.clases import paymentplan as PlanPago

# TIEMPO
from datetime import datetime
from dateutil.relativedelta import relativedelta

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
@receiver(pre_save, sender=Recibo)
def generar_noRecibo(sender, instance, **kwargs):
    if not instance.recibo or instance.recibo == 0:
        counter = 1
        while Recibo.objects.filter(recibo=counter).exists():
            counter += 1

        instance.recibo = counter

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
        

def calculo_interes(saldo_pendiente, tasa_interes):
    interes = saldo_pendiente * tasa_interes 
    return round(interes,2)

def calcular_fecha_vencimiento(fecha_inicio):
    # Convertir fecha_inicio a un objeto datetime
    #fecha_inicio = datetime.strptime(fecha_inicio)
    plazo = 1
    # Usar relativedelta para sumar meses al objeto datetime
    fecha_vencimiento = fecha_inicio + relativedelta(months=plazo)
    # Devolver la fecha en formato string
    return fecha_vencimiento

def calcular_fecha_maxima(fecha_inicio):
    
    # Convertir fecha_inicio a un objeto datetime
    #fecha_inicio = datetime.strptime(fecha_inicio)
    plazo = 1
    # Usar relativedelta para sumar meses al objeto datetime
    fecha_limite = fecha_inicio + relativedelta(months=plazo, days= 15)
    # Devolver la fecha en formato string
    return fecha_limite

@receiver(post_save, sender=Credit)
def generar_plan_pagos(sender, instance, created, **kwargs):
    if created:
        instance.saldo_pendiente = instance.monto

        #credito = Credito(instance.proposito, instance.monto, instance.plazo, instance.forma_de_pago, instance.frecuecia_pago, instance.fecha_inicio, instance.tipo_credito, instance.customer_id)
        #pago = PlanPago(credito)
        #pcapital = pago.recalcular_capital()
      
        
        # CALCULO DE INTERES
        interes = calculo_interes(instance.saldo_pendiente, instance.tasa_interes)
        # GENERACION DE FECHA LIMITE DE PAGO 15 DIAS
        fecha_limite = calcular_fecha_maxima(instance.fecha_inicio)
        print(fecha_limite)
        # FECHA DE VENCIMIENTO
        fecha_vencimiento = calcular_fecha_vencimiento(instance.fecha_inicio)
        
        # GENERAR LA PRIMERA CUOTA
        plan_pago = PaymentPlan(
            credit_id=instance,
            start_date=instance.fecha_inicio, 
            outstanding_balance=instance.monto, 
            saldo_pendiente=instance.monto,
            interest=interes,
            #fecha_limite = fecha_limite,
            due_date=fecha_vencimiento
            )
        plan_pago.save()
     