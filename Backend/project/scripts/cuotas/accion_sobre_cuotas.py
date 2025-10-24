# HISTORIAL Y BITACORA
from apps.actividades.utils import log_user_action, log_system_event


# UUID
import uuid

# MODELOS
from apps.financings.models import PaymentPlan, Credit, AccountStatement, Payment
from apps.accountings.models import Creditor, Insurance
from django.db.models import Q
from apps.codes.models import TokenCliente

# CALCULOS
from apps.financings.calculos import calculo_mora, calculo_interes
from decimal import Decimal

# MENSAJES DE ALERTA
from project.send_mail import send_email_update_of_quotas


# lOGS
import logging
logger = logging.getLogger(__name__)

def get_credito(cuota):
    logger.info("OBTENIENDO EL CREDITO")
    credito = None

    if cuota.credit_id is not None:
        credito =  Credit.objects.get(id=cuota.credit_id.id)

        if credito.estado_judicial:
            return None
    
    if cuota.acreedor is not None:
        credito =  Creditor.objects.get(id=cuota.acreedor.id)
    
    if cuota.seguro is not None:
        credito =  Insurance.objects.get(id=cuota.seguro.id)

    return credito



def calcular_interes_y_mora(cuota):
    logger.info("Realizando los Calculos de Interes o de Mora")

    tasa_interes = 0
    interes = 0
    mora = 0

    if cuota.credit_id is not None:
        tasa_interes =  cuota.credit_id.tasa_interes

        if not cuota.status:
            mora = Decimal(cuota.mora) + (Decimal(cuota.interest) * Decimal("0.10")) # Por lo establecido la mora es del 10%
    
    if cuota.acreedor is not None:
        tasa_interes = cuota.acreedor.tasa
    
    if cuota.seguro is not None:
        tasa_interes = cuota.seguro.tasa
    
    interes = calculo_interes(cuota.saldo_pendiente,tasa_interes)

    return interes, mora

def procesar_siguiente_cuota(pago, siguiente_cuota, interes,interes_acumulado, mora):
    datos_viejos = {}
    datos_nuevos = {}
    

    if siguiente_cuota is not None:
        

        siguiente_cuota.outstanding_balance = pago.saldo_pendiente
        siguiente_cuota.saldo_pendiente = pago.saldo_pendiente

        if pago.credit_id:
            siguiente_cuota.credit_id = pago.credit_id
            siguiente_cuota.mora = mora 
            siguiente_cuota.interest = interes_acumulado

        if pago.seguro:
            siguiente_cuota.seguro = pago.seguro
            siguiente_cuota.interest = interes
        
        if pago.acreedor:
            siguiente_cuota.acreedor = pago.acreedor
            siguiente_cuota.interest = interes

        

        siguiente_cuota.interes_generado =interes
        siguiente_cuota.start_date = pago.due_date
        siguiente_cuota.cambios = True
        siguiente_cuota.save()

        
        

       
        

    else:
        cuota = PaymentPlan()
        cuota.outstanding_balance = pago.saldo_pendiente
        cuota.saldo_pendiente = pago.saldo_pendiente

        if pago.credit_id:
            cuota.credit_id = pago.credit_id
            cuota.interes_generado =interes
            cuota.interest = interes_acumulado
            cuota.mora = mora 

        if pago.seguro:
            cuota.seguro = pago.seguro
            cuota.interest = interes
        
        if pago.acreedor:
            cuota.acreedor = pago.acreedor
            cuota.interest = interes

        cuota.start_date = pago.due_date
        cuota.save()

        
        
        



def generar_estado_cuenta(cuota, accion):
    estado_cuenta = AccountStatement()

    if cuota.credit_id:
        estado_cuenta.credit = cuota.credit_id
    
    if cuota.acreedor:
        estado_cuenta.acreedor = cuota.acreedor
    
    if cuota.seguro:
        estado_cuenta.seguro = cuota.seguro

    estado_cuenta.numero_referencia = str(uuid.uuid4())[:8]

    if accion == 'FECHA_LIMITE':
        if cuota.interes_pagado > 0:
            estado_cuenta.description = f'La cuota No. {cuota.mes} se encuentra vencida.\nCapital Pendiente Por Pagar.'
        else:
            estado_cuenta.description = f'La cuota No. {cuota.mes} se encuentra vencida.\nFalta de Pago.'

    if accion == 'FECHA_VENCIMIENTO':
        if cuota.interes_pagado > 0:
            estado_cuenta.description = f'La cuota No. {cuota.mes} ha pasado al estado de "Fechas en atraso".\nPor Capital Pendiente Por Pagar.'
        else:
            estado_cuenta.description = f'La cuota No. {cuota.mes} ha pasado al estado de "Fechas en atraso".\nPor Falta de Pago.'


    estado_cuenta.cuota = cuota
    estado_cuenta.saldo_pendiente = cuota.saldo_pendiente
    estado_cuenta.save()


def get_boleta(credito):
    boleta = None

    return boleta

def obtener_la_siguiente_cuota(cuota):
    siguiente_cuota = None

    if cuota.credit_id:
        siguiente_cuota = PaymentPlan.objects.filter(
            credit_id=cuota.credit_id,
            fecha_limite__gt=cuota.fecha_limite
            ).order_by('fecha_limite').first()
                

    if cuota.acreedor:
        siguiente_cuota = PaymentPlan.objects.filter(
            acreedor=cuota.acreedor,
            fecha_limite__gt=cuota.fecha_limite
            ).order_by('fecha_limite').first()
                
            
    if cuota.seguro:
        siguiente_cuota = PaymentPlan.objects.filter(
            seguro=cuota.seguro,
            fecha_limite__gt=cuota.fecha_limite
            ).order_by('fecha_limite').first()
                
    return siguiente_cuota

def recorrido_de_cuotas(cuotas, accion):

    print(f'SE ESTA ANALIZANDO: {accion}')

    for cuota in cuotas:
        boleta_cuota = None
        credito = get_credito(cuota)

        print(f'CUOTA: {cuota}')
        
        if credito is None:
            continue

        if credito.is_paid_off:
            print(f"El credito {credito} ya ha sido cancelado por completo")
            continue

        

        
        

        if accion == 'FECHA_LIMITE':

            interes, mora = calcular_interes_y_mora(cuota)
            interes_acumulado = 0
            
            

            if not cuota.status:
                cuota.cuota_vencida = True
                credito.estado_aportacion = False

                generar_estado_cuenta(cuota, accion)
                if cuota.interest != 0:
                    cuota.mora = mora
                    cuota.mora_generado = mora
                cuota.save()               
                
    
            else:
                credito.estados_fechas = True
                credito.estado_aportacion = False

            credito.save()
            siguiente_cuota = obtener_la_siguiente_cuota(cuota)
            interes_acumulado = cuota.interest + interes

            if cuota.credit_id is not None:

                tokken, creado = TokenCliente.objects.get_or_create(
                    cliente=cuota.credit_id.customer_id,
                    cuota=cuota
                )

                tokken.delete()

                tokkens, creado = TokenCliente.objects.get_or_create(
                    cliente=cuota.credit_id.customer_id,
                    cuota=siguiente_cuota
                )

                print(f'Token nuevo {tokkens}')

                


                

            

            procesar_siguiente_cuota(cuota, siguiente_cuota,interes ,interes_acumulado, mora)
            
        if accion == 'FECHA_VENCIMIENTO':
            
            cuota.paso_por_task = True

            if credito.estado_aportacion == True:
                credito.estado_aportacion = False

            if not cuota.status:
                credito.estados_fechas = False
                generar_estado_cuenta(cuota, accion)

            else:
                credito.estados_fechas = True

            credito.save()
            cuota.save()
            
            

            
   

    print('PROCESO FINALIZADO')