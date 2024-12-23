
import uuid
from django.db import transaction
from celery import shared_task

# MODELOS
from apps.financings.models import PaymentPlan, Payment, Recibo,AccountStatement, Credit
from decimal import Decimal
from django.shortcuts import render, get_object_or_404

# CALCULOS
from apps.financings.calculos import calculo_mora, calculo_interes

# TIEMPO
from datetime import datetime

import logging
logger = logging.getLogger(__name__)

def get_credito(id):
    return Credit.objects.get(id=id)

@shared_task
def cambiar_plan():
    # Obtener todas las cuotas con respecto al dia de hoy
    planes = PaymentPlan.objects.filter(fecha_limite__date=datetime.now().date(), cuota_vencida=False,paso_por_task=False)
    if planes:
        # Recorrer por cada cuota encontrada
        for pago in planes:

            # Verificar si el credito ya esta cancelado
            if pago.credit_id.is_paid_off:
                logger.error('El Credito ya ha sido cancelado')
            else:
                # Validar si hay algún pago registrado para este crédito
                boleta = Payment.objects.filter(credit=pago.credit_id, id=pago.id )
                # Credito de la cuota
                credito = get_credito(pago.credit_id.id)

                # Si en dado caso no se encontrar una boleta para este credito 

                # Calcular el interes para la proxima cuota
                interes = calculo_interes(pago.saldo_pendiente,pago.credit_id.tasa_interes)

                # Buscar la siguiente cuota del credito
                siguiente_cuota = PaymentPlan.objects.filter(
                        credit_id_id=pago.credit_id.id,  
                        fecha_limite__gt=pago.fecha_limite  # Filtramos por fecha límite
                    ).order_by('fecha_limite').first()

                if not boleta:
                    # GENERAR MORA
                    mora = Decimal(pago.interest) * Decimal(0.1)
                    pago.mora = mora
                    pago.mora_generado = mora

                    

                    # Asegurar que ya haya pasado por aqui la cuota
                    pago.paso_por_task = True


                    # Verificar si no llego alcanzar aportar a capital
                    if not pago.status:
                        # Colocar como la cuota vencida
                        pago.cuota_vencida = True

                        # Poner en estado de en atraso del credito
                        
                        credito.estados_fechas = False
                        credito.save()

                        # Indicar en el estado de cuenta que hay un atraso en el estado de cuenta
                        estado_cuenta = AccountStatement(credit=pago.credit_id,numero_referencia=str(uuid.uuid4())[:8],description="CUOTA VENCIDA",cuota=pago, saldo_pendiente=pago.saldo_pendiente)
                        estado_cuenta.save()
                    else:
                        # Si llego aportar a capital, se resta un plazo
                        credito.plazo_restante -= 1

                        # Se actualiza el estado de aportacion para la otra cuota
                        credito.estado_aportacion = False
                        credito.save()

                    pago.save()

                    interes_acumulado = pago.interest + interes

                    if not siguiente_cuota:
                        #  Si no hay una siguiente cuota, se genera una nueva cuota
                        nuevo_plan = PaymentPlan(
                            saldo_pendiente=pago.saldo_pendiente, 
                            credit_id= pago.credit_id, 
                            start_date=pago.due_date,
                            mora=pago.mora, 
                            outstanding_balance=pago.saldo_pendiente,
                            interest=interes_acumulado,
                            interes_generado=interes,
                            interes_acumulado_generado=pago.interest,
                            mora_acumulado_generado=pago.mora,
                            
                            )
                        nuevo_plan.save()
                        credito.saldo_pendiente = nuevo_plan.saldo_pendiente
                        credito.saldo_actual = nuevo_plan.saldo_pendiente +  nuevo_plan.mora + nuevo_plan.interest
                        credito.save()

                    else:
                        # Si hay una siguiente cuota, se actualiza la siguiente cuota
                        siguiente_cuota.saldo_pendiente =pago.saldo_pendiente
                        siguiente_cuota.credit_id =pago.credit_id
                        siguiente_cuota.start_date =pago.due_date
                        siguiente_cuota.mora =pago.mora
                        siguiente_cuota.outstanding_balance =pago.saldo_pendiente
                        siguiente_cuota.interest =interes_acumulado
                        siguiente_cuota.interes_generado = interes
                        siguiente_cuota.interes_acumulado_generado=pago.interest,
                        siguiente_cuota.mora_acumulado_generado = pago.mora
                        siguiente_cuota.save()

                        credito.saldo_pendiente = siguiente_cuota.saldo_pendiente
                        credito.saldo_actual = siguiente_cuota.saldo_pendiente +  siguiente_cuota.mora + siguiente_cuota.interest
                        credito.save()

                else:
                    # Asegurar que ya haya pasado por aqui la cuota
                    pago.paso_por_task = True
                    pago.save()
                    if siguiente_cuota:
                        # Si hay una siguiente cuota, se actualiza la siguiente cuota
                        siguiente_cuota.saldo_pendiente =pago.saldo_pendiente
                        siguiente_cuota.credit_id =pago.credit_id
                        siguiente_cuota.start_date =pago.due_date
                        #siguiente_cuota.mora =pago.mora
                        siguiente_cuota.outstanding_balance =pago.saldo_pendiente
                        siguiente_cuota.interest =interes

                        siguiente_cuota.interes_generado = interes
                        
                        siguiente_cuota.save()

                        credito.saldo_pendiente = siguiente_cuota.saldo_pendiente
                        credito.saldo_actual = siguiente_cuota.saldo_pendiente +  siguiente_cuota.mora + siguiente_cuota.interest
                        credito.save()

                    else:
                        #  Si no hay una siguiente cuota, se genera una nueva cuota
                        nuevo_plan = PaymentPlan(
                            saldo_pendiente=pago.saldo_pendiente, 
                            credit_id= pago.credit_id, 
                            start_date=pago.due_date,                            
                            outstanding_balance=pago.saldo_pendiente,
                            interest=interes,
                            interes_generado=interes
                            
                            
                            )
                        nuevo_plan.save() 

                        credito.saldo_pendiente = nuevo_plan.saldo_pendiente
                        credito.saldo_actual = nuevo_plan.saldo_pendiente +  nuevo_plan.mora + nuevo_plan.interest
                        credito.save()
                        
            
            