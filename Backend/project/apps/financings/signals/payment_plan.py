from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.dispatch import receiver

# MODELOS
from apps.financings.models import Credit, PaymentPlan


# CLASES
from apps.financings.calculos import calculo_mora, calculo_interes

# TIEMPO
from datetime import datetime
from django.utils import timezone

# LOOGER
from apps.financings.clases.personality_logs import logger

# DECIMAL
from decimal import Decimal

# PARA CREAR CUOTAS NUEVAS POR SI LA FECHA DE LA PRIMERA CUOTA ES MUY ANTIGUA
# EJEMPLO:
# FECHA DE HOY; 27 DE SEPTIEMBRE 
# PERO LA FECHA DEL LA PRIMERA CUOTA ESTA PARA EL 2 DE FEBRERO
# ESTO CREAR NUEVAS CUOTAS


@receiver(post_save, sender=PaymentPlan)
def generar_planes(sender, instance,created, **kwargs):
    # Cálculo de interés y mora acumulada
    interes = calculo_interes(instance.saldo_pendiente, instance.credit_id.tasa_interes)
    #mora_acumulada = calculo_mora(instance.saldo_pendiente, instance.credit_id.tasa_interes)
    mora_acumulada = Decimal(instance.interest) * Decimal(0.1)
    interes_acumulado = instance.interest + interes
    

    if created:
        fecha_actual = str(datetime.now().date())  # Obtén la fecha actual aware
        limite_fecha = instance.fecha_limite.strftime('%Y-%m-%d')       
        
        if fecha_actual >= limite_fecha:
            # Acumular mora y marcar estado
            logger.info(f'DESDE SIGNALS DE PAYMENT_PLAN: CUOTA VENCIDA: {instance.cuota_vencida}')
            logger.info(f'DESDE SIGNALS DE PAYMENT_PLAN: PAGADO: {instance.status}')

            if not instance.cuota_vencida and not instance.status:
                #more = instance.mora +mora_acumulada
                more = mora_acumulada
                logger.info(f'DESDE SIGNALS DE PAYMENT_PLAN: MORA: {round(more,2)}')
                instance.mora = more
            instance.cuota_vencida = True
            instance.save()

            # Crear nueva cuota
            cuota_nueva = PaymentPlan(
                saldo_pendiente=instance.saldo_pendiente,
                credit_id=instance.credit_id,
                start_date=instance.due_date,
                mora=more,
                outstanding_balance=instance.saldo_pendiente,
                interest=interes_acumulado
            )
            cuota_nueva.save()
            actualizar(instance.id)
        
    
        
def actualizar(id):
    pagos = PaymentPlan.objects.filter(id=id).order_by('-id').first()
    credito = Credit.objects.get(id=pagos.credit_id.id)
    credito.saldo_pendiente = pagos.saldo_pendiente
    credito.saldo_actual = pagos.saldo_pendiente + pagos.mora + pagos.interest
    credito.save()





# VER SI HUBO CAMBIOS
@receiver(post_delete,  sender=PaymentPlan)
def eliminar_siguientes_cuotas(sender, instance, **kwargs):
    # Obtener la siguiente cuota
    siguiente_cuota = PaymentPlan.objects.filter(
        credit_id_id=instance.credit_id.id,  
        fecha_limite__gt=instance.fecha_limite  # Filtramos por fecha límite
    ).order_by('fecha_limite').first()

    if siguiente_cuota:
        siguiente_cuota.delete()


@receiver(post_save, sender=PaymentPlan)
def cambios(sender, instance, **kwargs):
    
    if instance.cambios:
        logger.info(f'\n\n')
        logger.info('\nDESDE SIGNALS DE PAYMENT_PLAN: POR REALIZAR CAMBIOS EN LA SIGUIENTE CUOTA\n')
        referencia = instance.numero_referencia
        #fecha_limite_aware = timezone.make_aware(instance.fecha_limite)
        logger.info(f'DESDE SIGNALS DE PAYMENT_PLAN: CUOTA ACTUAL: {instance}')
        logger.info(f'\n\n')
        # Obtener la siguiente cuota
        siguiente_cuota = PaymentPlan.objects.filter(
            credit_id_id=instance.credit_id.id,  
            fecha_limite__gt=instance.fecha_limite  # Filtramos por fecha límite
        ).order_by('fecha_limite').first()

        logger.info(f'DESDE SIGNALS DE PAYMENT_PLAN: CAMBIO DE LA CUOTA: {siguiente_cuota}')
        cuota_interes = instance.interest
        logger.info(f'DESDE SIGNALS DE PAYMENT_PLAN: INTERES ANTERIOS: {round(cuota_interes,2)}')
        mora_a = instance.mora

        if siguiente_cuota:
            interes = calculo_interes(instance.saldo_pendiente, instance.credit_id.tasa_interes)
            #mora = calculo_mora(instance.saldo_pendiente, instance.credit_id.tasa_interes)
            mora = Decimal(cuota_interes) * Decimal(0.1)
            logger.info(f'DESDE SIGNALS DE PAYMENT_PLAN: OPERACION POR REALIZAR: \nx = {cuota_interes} + {interes}\n')

            cuota_interes = cuota_interes + interes
            cuota_mora = mora_a + mora


            
            logger.info(f'DESDE SIGNALS DE PAYMENT_PLAN: INTERES: {round(cuota_interes,2)}')
            logger.info(f'DESDE SIGNALS DE PAYMENT_PLAN: Mora: {round(mora,2)}')
            logger.info(f'\n\n')
            # Actualizar la siguiente cuota
            siguiente_cuota.cambios = True
            siguiente_cuota.interest = round(cuota_interes,2)  # Asegúrate de que no sea negativa
            #siguiente_cuota.mora = max(0, siguiente_cuota.mora - mora)  # Asegúrate de que no sea negativa
            siguiente_cuota.mora = round(cuota_mora,2) # Asegúrate de que no sea negativa
            siguiente_cuota.start_date = instance.due_date
            siguiente_cuota.saldo_pendiente = instance.saldo_pendiente
            siguiente_cuota.credit_id = instance.credit_id
            siguiente_cuota.save()

            logger.info(f"DESDE SIGNALS DE PAYMENT_PLAN: Siguiente cuota actualizada: {siguiente_cuota}")
        else:
            logger.warning("DESDE SIGNALS DE PAYMENT_PLAN: No hay más cuotas disponibles.")

        # Manejo de pagos
        try:
            pago = Payment.objects.get(numero_referencia=referencia)
            if pago.estado_transaccion == 'COMPLETADO':
                pago.realizar_pago()
        except Payment.DoesNotExist:
            logger.error(f"DESDE SIGNALS DE PAYMENT_PLAN: No se encontró el pago con número de referencia: {referencia}")
        
   

   