from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

# MODELOS
from .models import Payment, AccountStatement, Credit, PaymentPlan, Banco, Recibo, Disbursement

# FUNCIONALIDADES
from .functions import realizar_pago

# CLASES
from apps.financings.clases import credit as Credito
from apps.financings.clases import paymentplan as PlanPago
from .calculos import calcular_fecha_maxima, calcular_fecha_vencimiento, calculo_mora, calculo_interes

# TIEMPO
from datetime import datetime
from dateutil.relativedelta import relativedelta

import uuid
import logging
logger = logging.getLogger(__name__)



# ENVIO DE EMAIL
from .task import envio_mensaje_alerta, envio_mensaje_alerta_recibo
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
# GENERACION DE NUMEROS DE RECIBO
@receiver(pre_save, sender=Recibo)
def generar_noRecibo(sender, instance, **kwargs):
    if not instance.recibo or instance.recibo == 0:
        counter = 1
        while Recibo.objects.filter(recibo=counter).exists():
            counter += 1

        instance.recibo = counter
    # ENVIAR MENSAJES AL CLIENTE, ADMINISTRADORES Y SECRETARIA
    #envio_mensaje_alerta_recibo(instance.id)
    logger.info('ENVIO DE MENSAJE DE RECIBO CARGADO')


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
def generar_plan_pagos(sender, instance, created, **kwargs):
    if created:
        instance.saldo_pendiente = instance.monto
        # CALCULO DE INTERES
        interes = calculo_interes(instance.saldo_pendiente, instance.tasa_interes)
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
            fecha_limite = fecha_limite,
            due_date=fecha_vencimiento
            )
        plan_pago.save()
    

# PARA CREAR CUOTAS NUEVAS POR SI LA FECHA DE LA PRIMERA CUOTA ES MUY ANTIGUA
# EJEMPLO:
# FECHA DE HOY; 27 DE SEPTIEMBRE 
# PERO LA FECHA DEL LA PRIMERA CUOTA ESTA PARA EL 2 DE FEBRERO
# ESTO CREAR NUEVAS CUOTAS

@receiver(post_save, sender=PaymentPlan)
def generar_planes(sender, instance,created, **kwargs):
    
    if created:
        fecha_actual = datetime.now().date()
        limite_fecha = instance.fecha_limite
        print(limite_fecha)
        print(fecha_actual)
        
        
        if fecha_actual >= limite_fecha:
            mora_acumulada = calculo_mora(instance.saldo_pendiente, instance.credit_id.tasa_interes)
            instance.mora += mora_acumulada   
            instance.status = True   

            interes = calculo_interes(instance.saldo_pendiente,instance.credit_id.tasa_interes)
            interes_acumulado = instance.interest + interes
            cuota_nueva = PaymentPlan(
                saldo_pendiente=instance.saldo_pendiente, 
                credit_id= instance.credit_id, 
                start_date=instance.due_date,
                mora=instance.mora, 
                outstanding_balance=instance.saldo_pendiente,
                interest=interes_acumulado
                )
            cuota_nueva.save()
        

# EL DESEMBOLSO REALIZADO SE REFLEJA EN EL ESTADO DE CUENTAS DEL CLIENTE
@receiver(post_save, sender=Disbursement)
def reflejar_estado_cuenta(sender, instance, created, **kwargs):
    if created:
        referencia = str(uuid.uuid4())[:8]
        
        # Si `numero_referencia` es único, manejamos colisión con try/except
        estado_cuenta = AccountStatement(
            credit=instance.credit_id,
            disbursement=instance,
            disbursement_paid=instance.monto_total_desembolso,
            numero_referencia=referencia
        )
        
        try:
            estado_cuenta.save()
        except IntegrityError:
            # En caso de colisión, generar una nueva referencia y volver a intentar
            referencia = str(uuid.uuid4())[:8]
            estado_cuenta.numero_referencia = referencia
            estado_cuenta.save()

# VER SI HUBO CAMBIOS
@receiver(post_save, sender=PaymentPlan)
def cambios(sender, instance, **kwargs):
    if instance.cambios:
        referencia = instance.numero_referencia
        
        # Obtener la siguiente cuota
        siguiente_cuota = PaymentPlan.objects.filter(
            credit_id=instance.credit_id,  
            fecha_limite__gt=instance.fecha_limite  # Filtramos por fecha límite
        ).order_by('fecha_limite').first()

        if siguiente_cuota:
            interes = calculo_interes(instance.saldo_pendiente, instance.credit_id.tasa_interes)
            mora = calculo_mora(instance.saldo_pendiente, instance.credit_id.tasa_interes)
            
            # Actualizar la siguiente cuota
            siguiente_cuota.cambios = True
            siguiente_cuota.interest = max(siguiente_cuota.interest, siguiente_cuota.interest - interes)  # Asegúrate de que no sea negativa
            siguiente_cuota.mora = max(siguiente_cuota.mora, siguiente_cuota.mora - mora)  # Asegúrate de que no sea negativa
            siguiente_cuota.start_date = instance.due_date
            siguiente_cuota.saldo_pendiente = instance.saldo_pendiente
            siguiente_cuota.credit_id = instance.credit_id
            siguiente_cuota.save()

            logger.info(f"Siguiente cuota actualizada: {siguiente_cuota}")
        else:
            logger.warning("No hay más cuotas disponibles.")

        # Manejo de pagos
        try:
            pago = Payment.objects.get(numero_referencia=referencia)
            if pago.estado_transaccion == 'COMPLETADO':
                pago.realizar_pago()
        except Payment.DoesNotExist:
            logger.error(f"No se encontró el pago con número de referencia: {referencia}")
   

# ENVIO DE ALERTA PARA EL ESTATUS DE LA BOLETA
@receiver(post_save, sender=Payment)
def alerta(sender, instance, **kwargs):
    if instance.estado_transaccion == 'FALLIDO':
        logger.info('ENVIANDO MENSAJE')
        #envio_mensaje_alerta(instance.descripcion_estado, 'FALLIDO',instance.id)
    elif instance.estado_transaccion == 'COMPLETADO':
        logger.info('ENVIANDO MENSAJE')
        #envio_mensaje_alerta(instance.descripcion_estado, 'COMPLETADO',instance.id)


   