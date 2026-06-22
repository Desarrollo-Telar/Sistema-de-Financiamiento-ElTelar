# HISTORIAL Y BITACORA
from apps.actividades.utils import log_user_action, log_system_event

# UUID
import uuid

# MODELOS
from apps.financings.models import   Payment
from apps.accountings.models import Creditor, Insurance
from django.db.models import Q
from dateutil.relativedelta import relativedelta
from apps.codes.models import TokenCliente



# MENSAJES DE ALERTA
from project.send_mail import send_email_update_of_quotas
from datetime import datetime

# lOGS
import logging
logger = logging.getLogger(__name__)


# FUNCIONES
from .funciones import get_credito, calcular_interes_y_mora, calculo_interes, calculo_mora, procesar_siguiente_cuota, generar_estado_cuenta
from .funciones import obtener_la_siguiente_cuota

def recorrido_de_cuotas(cuotas, accion, dia=None):

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
        
        cambiar_estados = True

        if cuota.credit_id:
            fecha_inicio = cuota.credit_id.fecha_inicio
            fecha_emision = dia
            fecha_limite = cuota.credit_id.fecha_finalizacion_gracia 
           
            forma_pago = cuota.credit_id.forma_de_pago


            if (
                    fecha_limite is not None and
                    fecha_inicio <= fecha_emision <= fecha_limite and
                    forma_pago == 'INTERES Y CAPITAL AL VENCIMIENTO'
                ):
                cambiar_estados = False
                cuota.status = True

        
        if accion == 'FECHA_LIMITE':
            
            interes, mora = calcular_interes_y_mora(cuota)
            interes_acumulado = 0
            
            

            if ( cuota.status == False or cuota.status is None) :
                cuota.cuota_vencida = True
                credito.estado_aportacion = False

                generar_estado_cuenta(cuota, accion, dia)
                if cuota.interest != 0:
                    cuota.mora = mora
                    cuota.mora_generado = mora
                cuota.save()               
                
    
            else:
                credito.estados_fechas = True
                

            credito.save()
            siguiente_cuota = obtener_la_siguiente_cuota(cuota)

            interes_acumulado = cuota.interest + interes

            if cuota.credit_id:
                forma_pago = cuota.credit_id.forma_de_pago
                fecha_inicio = cuota.credit_id.fecha_inicio
                fecha_emision = dia
                fecha_limite = cuota.credit_id.fecha_finalizacion_gracia + relativedelta(months=1)
                forma_pago = cuota.credit_id.forma_de_pago
                if (
                    fecha_limite is not None and
                    fecha_inicio <= fecha_emision <= fecha_limite and
                    forma_pago == 'INTERES Y CAPITAL AL VENCIMIENTO'
                ):
                    interes_acumulado = cuota.interest





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

                


                

            

            procesar_siguiente_cuota(cuota, siguiente_cuota,interes ,interes_acumulado, mora, dia)

      
        if accion == 'FECHA_VENCIMIENTO':
            
            cuota.paso_por_task = True   
            cuota.save() 
            
               

            if ( cuota.status == False or cuota.status is None) and cambiar_estados:
               

                if cuota.interest > 0:
                    credito.estados_fechas = False
                    if credito.fecha_entrar_en_mora is None:
                        credito.fecha_entrar_en_mora = datetime.now().date()
                
                verificacion_estado_aportacion = cuota.capital_generado - cuota.principal 

                if verificacion_estado_aportacion > 0:
                    credito.estado_aportacion = False

                generar_estado_cuenta(cuota, accion, dia)

            else:
                credito.estados_fechas = True

<<<<<<< HEAD
            print(credito.estados_fechas)
            credito.save()
            
=======
            
            credito.save()
>>>>>>> master
            
            

            
   

    print('PROCESO FINALIZADO')