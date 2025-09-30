from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.dispatch import receiver

# MODELOS
from apps.financings.models import Credit, PaymentPlan,Payment, Cuota
from apps.accountings.models import Creditor, Insurance

# CLASES
from apps.financings.calculos import calculo_mora, calculo_interes

# TIEMPO
from datetime import datetime
from django.utils import timezone

# LOOGER
from apps.financings.clases.personality_logs import logger

# DECIMAL
from decimal import Decimal

from django.db.models import Q

# PARA CREAR CUOTAS NUEVAS POR SI LA FECHA DE LA PRIMERA CUOTA ES MUY ANTIGUA
# EJEMPLO:
# FECHA DE HOY; 27 DE SEPTIEMBRE 
# PERO LA FECHA DEL LA PRIMERA CUOTA ESTA PARA EL 2 DE FEBRERO
# ESTO CREAR NUEVAS CUOTAS



from django.db.models import Max

@receiver(pre_save, sender=PaymentPlan)
def numeracion_cuota(sender, instance, *args, **kwargs):
    if not instance.mes :  # Si `mes` no está definido aún
        # Obtén el valor máximo de `mes` para el mismo crédito
        max_mes = None
        if  instance.credit_id is not None:
            max_mes = PaymentPlan.objects.filter(
            credit_id=instance.credit_id
        ).aggregate(Max('mes'))['mes__max']
        

        if  instance.acreedor is not None: 
            max_mes = PaymentPlan.objects.filter(
                acreedor=instance.acreedor
            ).aggregate(Max('mes'))['mes__max']

        if  instance.seguro is not None:
            max_mes = PaymentPlan.objects.filter(
                seguro=instance.seguro
            ).aggregate(Max('mes'))['mes__max']
    
        
        
        # Si no hay registros, empieza con 1; de lo contrario, incrementa el máximo
        instance.mes = (max_mes or 0) + 1

    


@receiver(post_save, sender=PaymentPlan)
def generar_planes(sender, instance,created, **kwargs):
    # Cálculo de interés y mora acumulada
    tasa_interes = 0
    if  instance.credit_id is not None:
        tasa_interes = instance.credit_id.tasa_interes

    if  instance.acreedor is not None:
        tasa_interes = instance.acreedor.tasa

    if  instance.seguro is not None:
        tasa_interes = instance.seguro.tasa


    interes = calculo_interes(instance.saldo_pendiente, tasa_interes)
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
            more = 0
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
                mora_acumulado_generado=more,
                outstanding_balance=instance.saldo_pendiente,
                interest=interes_acumulado,
                interes_generado=interes,
                interes_acumulado_generado=instance.interest,
                acreedor=instance.acreedor,
                seguro=instance.seguro
                
            )
            cuota_nueva.save()
    
    actualizar(instance)
            
        
    
        
def actualizar(instance):
    if  instance.credit_id is not None:
        credito = Credit.objects.get(id=instance.credit_id.id)
        credito.saldo_pendiente = instance.saldo_pendiente
        credito.saldo_actual = instance.saldo_pendiente + instance.mora + instance.interest
        credito.save()

    if  instance.acreedor is not None:
        acreedor = Creditor.objects.get(id=instance.acreedor.id)
        acreedor.saldo_pendiente = instance.saldo_pendiente
        acreedor.saldo_actual = instance.saldo_pendiente + instance.mora + instance.interest
        acreedor.save()

    if  instance.seguro is not None:
        seguro = Insurance.objects.get(id=instance.seguro.id)
        seguro.saldo_pendiente = instance.saldo_pendiente
        seguro.saldo_actual = instance.saldo_pendiente + instance.mora + instance.interest
        seguro.save()
    
    








@receiver(post_delete, sender=PaymentPlan)
def eliminar_siguientes_cuotas(sender, instance, **kwargs):
    try:
        condiciones = Q(fecha_limite__gt=instance.fecha_limite)

        if instance.credit_id_id:
            condiciones &= Q(credit_id=instance.credit_id.id)
        if instance.acreedor_id:
            condiciones &= Q(acreedor_id=instance.acreedor.id)
        if instance.seguro_id:
            condiciones &= Q(seguro_id=instance.seguro.id)

        siguiente_cuota = PaymentPlan.objects.filter(condiciones).order_by('fecha_limite').first()

        if siguiente_cuota:
            siguiente_cuota.delete()
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error al eliminar siguientes cuotas: {e}")




