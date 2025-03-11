# CELERY
from celery import shared_task

# MODELOS
from apps.financings.models import PaymentPlan, Credit, AccountStatement, Payment
from apps.accountings.models import Creditor, Insurance

# CALCULOS
from apps.financings.calculos import calculo_mora, calculo_interes
from decimal import Decimal

# TIEMPO
from datetime import datetime
from django.utils.timezone import now

# UUID
import uuid

# lOGS
import logging
logger = logging.getLogger(__name__)

def get_credito(pago):
    credito = None
    if pago.credit_id is not None:
        credito =  Credit.objects.get(id=pago.credit_id.id)
    
    if pago.acreedor is not None:
        credito =  Creditor.objects.get(id=pago.acreedor.id)
    
    if pago.seguro is not None:
        credito =  Insurance.objects.get(id=pago.seguro.id)

    return credito

def calcular_interes_y_mora(pago):
    tasa_interes = 0

    if pago.credit_id is not None:
        tasa_interes =  pago.credit_id.tasa_interes
    
    if pago.acreedor is not None:
        tasa_interes = pago.acreedor.tasa
    
    if pago.seguro is not None:
        tasa_interes = pago.seguro.tasa
    
    interes = calculo_interes(pago.saldo_pendiente,tasa_interes)
    mora = Decimal(pago.interest) * Decimal(0.1)

    return interes, mora

def procesar_siguiente_cuota(pago, siguiente_cuota, interes_acumulado, mora):
    if siguiente_cuota:
        siguiente_cuota.saldo_pendiente = pago.saldo_pendiente
        siguiente_cuota.mora = mora
        siguiente_cuota.interest = interes_acumulado
        siguiente_cuota.start_date = pago.fecha_limite
        siguiente_cuota.save()

    else:
        cuota = PaymentPlan()
        cuota.saldo_pendiente = pago.saldo_pendiente

        if pago.credit_id:
            cuota.credit_id = pago.credit_id

        if pago.seguro:
            cuota.seguro = pago.seguro
        
        if pago.acreedor:
            cuota.acreedor = pago.acreedor

        cuota.start_date = pago.fecha_limite
        cuota.interest = interes_acumulado
        cuota.mora = mora
        cuota.save()

def actualizar_estado_credito_seguro_acreedor(credito, pago):
    if not pago.status:
        credito.estados_fechas = False
    else:
        credito.plazo_restante -= 1
        credito.estado_aportacion = False
    credito.save()

def generar_estado_cuenta(pago):
    estado_cuenta = AccountStatement()

    if pago.credit_id:
        estado_cuenta.credit = pago.credit_id
    
    if pago.acreedor:
        estado_cuenta.acreedor = pago.acreedor
    
    if pago.seguro:
        estado_cuenta.seguro = pago.seguro

    estado_cuenta.numero_referencia = str(uuid.uuid4())[:8]
    estado_cuenta.description = "CUOTA VENCIDA"
    estado_cuenta.cuota = pago
    estado_cuenta.saldo_pendiente = pago.saldo_pendiente
    estado_cuenta.save()

def verificar_por_ausencia():
    planes = PaymentPlan.objects.filter(cuota_vencida=False)

    if not planes.exists():
        logger.info("No hay registro")
        return
    
    logger.info("Procesando Datos")

    for pago in planes:
        boleta = None
        credito = get_credito(pago)

        if pago.credit_id:

            if pago.credit_id.is_paid_off:
                logger.error(f"El credito {pago.credit_id} ya ha sido cancelado por completo")
                continue
            
            if not pago.credit_id.desembolsado_completo:
                logger.error(f'El credito {pago.credit_id} no esta desembolsado por completo')
                continue

            boleta = Payment.objects.filter(credit=pago.credit_id).exists()

        if pago.acreedor:

            if pago.acreedor.is_paid_off:
                logger.error(f"El acreedor {pago.acreedor} ya ha sido cancelado por completo")
                continue
            
            boleta = Payment.objects.filter(acreedor=pago.acreedor).exists()
        
        if pago.seguro:

            if pago.seguro.is_paid_off:
                logger.error(f"El seguro {pago.seguro} ya ha sido cancelado por completo")
                continue
            
            boleta = Payment.objects.filter(seguro=pago.seguro).exists()
        
        if boleta is not None and pago.fecha_limite.date() < now().date():
            pago.paso_por_task = True
            pago.save()
            continue

            interes, mora = calcular_interes_y_mora(pago)
            siguiente_cuota = None

            if pago.credit_id:
                siguiente_cuota = PaymentPlan.objects.filter(
                    credit_id=pago.credit_id,
                    fecha_limite__gt=pago.fecha_limite
                ).order_by('fecha_limite').first()
                pago.paso_por_task = True

            if pago.acreedor:
                siguiente_cuota = PaymentPlan.objects.filter(
                    acreedor=pago.acreedor,
                    fecha_limite__gt=pago.fecha_limite
                ).order_by('fecha_limite').first()
            
            if pago.seguro:
                siguiente_cuota = PaymentPlan.objects.filter(
                    seguro=pago.seguro,
                    fecha_limite__gt=pago.fecha_limite
                ).order_by('fecha_limite').first()

            pago.mora = mora
            pago.mora_generado = mora

            if not pago.status:
                pago.cuota_vencida = True
                generar_estado_cuenta(pago)
                actualizar_estado_credito(credito, pago)
            else:
                actualizar_estado_credito(credito, pago)

            pago.save()
            interes_acumulado = pago.interest + interes
            procesar_siguiente_cuota(pago, siguiente_cuota, interes_acumulado, mora)
        
        logger.info("Procesamiento finalizado")

@shared_task
def cambiar_plan():
    #verificar_por_ausencia()

    planes = PaymentPlan.objects.filter(fecha_limite__date=datetime.now().date(), cuota_vencida=False)
    print(datetime.now().date())

    if not planes.exists():
        logger.info("No hay registro")
        return
    
    for pago in planes:
        boleta = None
        credito = get_credito(pago)

        if pago.credit_id:
            if pago.credit_id.is_paid_off:
                logger.error(f"El credito {pago.credit_id} ya ha sido cancelado por completo")
                continue
            
            if not pago.credit_id.desembolsado_completo:
                logger.error(f'El credito {pago.credit_id} no esta desembolsado por completo')
                continue

            boleta = Payment.objects.filter(credit=pago.credit_id).exists()

        if pago.acreedor:

            if pago.acreedor.is_paid_off:
                logger.error(f"El acreedor {pago.acreedor} ya ha sido cancelado por completo")
                continue
            
            boleta = Payment.objects.filter(acreedor=pago.acreedor).exists()
        
        if pago.seguro:

            if pago.seguro.is_paid_off:
                logger.error(f"El seguro {pago.seguro} ya ha sido cancelado por completo")
                continue
            
            boleta = Payment.objects.filter(seguro=pago.seguro).exists()

        if boleta:
            pago.paso_por_task = True
            pago.save()
            continue

            interes, mora = calcular_interes_y_mora(pago)
            siguiente_cuota = None

            if pago.credit_id:
                siguiente_cuota = PaymentPlan.objects.filter(
                    credit_id=pago.credit_id,
                    fecha_limite__gt=pago.fecha_limite
                ).order_by('fecha_limite').first()
                pago.paso_por_task = True

            if pago.acreedor:
                siguiente_cuota = PaymentPlan.objects.filter(
                    acreedor=pago.acreedor,
                    fecha_limite__gt=pago.fecha_limite
                ).order_by('fecha_limite').first()
            
            if pago.seguro:
                siguiente_cuota = PaymentPlan.objects.filter(
                    seguro=pago.seguro,
                    fecha_limite__gt=pago.fecha_limite
                ).order_by('fecha_limite').first()

            pago.mora = mora
            pago.mora_generado = mora

            if not pago.status:
                pago.cuota_vencida = True
                generar_estado_cuenta(pago)
                actualizar_estado_credito(credito, pago)
            else:
                actualizar_estado_credito(credito, pago)

            pago.save()
            interes_acumulado = pago.interest + interes
            procesar_siguiente_cuota(pago, siguiente_cuota, interes_acumulado, mora)
        
        logger.info("Procesamiento finalizado")
        


