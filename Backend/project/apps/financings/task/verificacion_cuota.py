# CELERY
from celery import shared_task

# MODELOS
from apps.financings.models import PaymentPlan, Credit, AccountStatement, Payment
from apps.accountings.models import Creditor, Insurance
from django.db.models import Q

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
    logger.info("OBTENIENDO EL CREDITO")
    credito = None
    if pago.credit_id is not None:
        credito =  Credit.objects.get(id=pago.credit_id.id)
    
    if pago.acreedor is not None:
        credito =  Creditor.objects.get(id=pago.acreedor.id)
    
    if pago.seguro is not None:
        credito =  Insurance.objects.get(id=pago.seguro.id)

    return credito

def calcular_interes_y_mora(pago):
    logger.info("CALCULANDO EL INTERES")
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

def procesar_siguiente_cuota(pago, siguiente_cuota, interes,interes_acumulado, mora):
    if siguiente_cuota is not None:
        siguiente_cuota.outstanding_balance = pago.saldo_pendiente

        siguiente_cuota.saldo_pendiente = pago.saldo_pendiente
        siguiente_cuota.mora = mora
        siguiente_cuota.interest = interes_acumulado
        siguiente_cuota.interes_generado =interes
        siguiente_cuota.start_date = pago.due_date
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

        cuota.start_date = pago.due_date
        cuota.interes_generado =interes
        cuota.interest = interes_acumulado
        cuota.mora = mora
        cuota.save()

def actualizar_estado_credito_seguro_acreedor(credito, pago):
    if not pago.status:
        credito.estados_fechas = False
    else:
        
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


def get_boleta(credito):
    boleta = None

    return boleta

@shared_task
def cambiar_estado():
    dia = datetime.now().date()
    planes = PaymentPlan.objects.filter(due_date__date=dia)
    

    if not planes.exists():
        logger.info("No hay registro")
        return
    
    
    for pago in planes:
        credito = get_credito(pago)
        actualizar_estado_credito_seguro_acreedor(credito, pago)

@shared_task
def cambiar_plan():
    dia = datetime.now().date()

    planes = PaymentPlan.objects.filter(fecha_limite__date=dia, cuota_vencida=False)
    print(planes)

    if not planes.exists():
        logger.info("No hay registro")
        return
    
    
    for pago in planes:
        
        boleta = None
        credito = get_credito(pago)
        
        if credito.is_paid_off:
            logger.error(f"El credito {credito} ya ha sido cancelado por completo")
            continue

        boleta = Payment.objects.filter(Q(credit=pago.credit_id) | Q(acreedor=pago.acreedor)| Q(seguro=pago.seguro)).first()

        
        if boleta.tipo_pago == "CREDITO":
            pago.paso_por_task = True
            pago.save()
            continue
        else:
            logger.info(f"No se encontro boleta")
            interes, mora = calcular_interes_y_mora(pago)
            print(f'{interes}, {mora}')
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
                actualizar_estado_credito_seguro_acreedor(credito, pago)
            else:
                actualizar_estado_credito_seguro_acreedor(credito, pago)

            pago.save()
            interes_acumulado = pago.interest + interes
            procesar_siguiente_cuota(pago, siguiente_cuota,interes ,interes_acumulado, mora)



        logger.info("Procesamiento finalizado")
        


