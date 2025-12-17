from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.dispatch import receiver
from django.core.exceptions import ValidationError
# LOGGER
from apps.financings.clases.personality_logs import logger
# MODELOS
from apps.financings.models import AccountStatement, Disbursement, Credit, PaymentPlan, Payment, Banco
from apps.accountings.models import Egress

# CALCULOS
from apps.financings.calculos import calculo_interes

# TIEMPO
from datetime import datetime
from django.utils import timezone

import uuid
from django.db import transaction, IntegrityError
from django.db.models import Q, Sum

def buscar_tipo_desembolso(elemento):
    lista = [
        'APLICACIÓN GASTOS', 
        'APLICACIÓN DE AMPLIACIÓN DE CRÉDITO VIGENTE',
        'CANCELACIÓN DE CRÉDITO VIGENTE'
    ]
    try:
        indice = lista.index(elemento)
        return indice
    except ValueError:
        if elemento == 'DESEMBOLSAR':
            return -1
        return 0

def informacion_estado_cuenta(instance, disbursement_paid, referencia, description):
    saldo_pendiente = None
    referencia = referencia

    pago_desembolso = Payment.objects.filter(disbursement=instance).first()
    
    if pago_desembolso is not None:
        referencia = pago_desembolso.numero_referencia


    if instance.forma_desembolso == "CANCELACIÓN DE CRÉDITO VIGENTE":
        saldo_pendiente = 0
    else:
        saldo_pendiente = instance.total_t

    estado_cuenta = AccountStatement(
        credit=instance.credit_id,
        disbursement=instance,
        disbursement_paid=disbursement_paid,
        numero_referencia=referencia,
        description=description,
        saldo_pendiente= saldo_pendiente
    )
    return estado_cuenta

def credito_desembolsado(instance):
    credito = instance.credit_id
    credito.desembolsado_completo = True
    credito.save()


@receiver(pre_save, sender=Disbursement)
def verificar_montos_desembolsados(sender, instance, **kwargs):
    # Verificar que los montos desembolsados no excedan el monto del crédito
    total_credito = instance.credit_id.monto

    filtros = Q()
    filtros &= ~Q(id=instance.id)
    filtros &= Q(credit_id=instance.credit_id.id)

    total_desembolso = Disbursement.objects.filter(filtros).order_by('-id')  # Sumar todos los gastos previos, manejando None como 0

    if instance.forma_desembolso == "CANCELACIÓN DE CRÉDITO VIGENTE":
        return f'No hacer suma'
    
    if not total_desembolso:
        return f'No hacer suma'
    
    print(total_desembolso)
    

    """monto_pendiente_desembolsar = total_desembolso.monto_total_desembolso if total_desembolso.monto_total_desembolso else 0
    gastos =  instance.total_gastos

    # Incluir el monto del desembolso actual
    total_desembolso = monto_pendiente_desembolsar - gastos
    instance.total_t = total_desembolso
    instance.monto_total_desembolso = total_desembolso

    if total_desembolso > total_credito:
        credito_desembolsado(instance)
        #raise ValidationError('El monto total desembolsado excede el monto del crédito.')
    
    if total_desembolso == total_credito:
        # Indicar que ya se desembolsó completamente
        credito_desembolsado(instance)

    # Registrar información adicional
    logger.info(f'Total desembolsado: {total_desembolso}, Total crédito: {total_credito}')"""

# EL DESEMBOLSO REALIZADO SE REFLEJA EN EL ESTADO DE CUENTAS DEL CLIENTE
@receiver(post_save, sender=Disbursement)
def reflejar_estado_cuenta(sender, instance, created, **kwargs):
    if created:
        desembolso_credito = Disbursement.objects.filter(
            credit_id_id=instance.credit_id.id, 
            forma_desembolso='APLICACIÓN GASTOS'
        )

        if instance.forma_desembolso == "CANCELACIÓN DE CRÉDITO VIGENTE":
            instance.monto_total_desembolso = 0
            monto_saldo_actual = instance.credit_id.saldo_actual
            referencia_ficticia = str(uuid.uuid4())[:8]

            boleta_ficticia = Payment(
                credit=instance.credit_id,
                monto=monto_saldo_actual,
                numero_referencia=referencia_ficticia,
                fecha_emision=timezone.now(),
                registro_ficticio=True,
                sucursal=instance.credit_id.sucursal
            )
            boleta_ficticia.save()

            banco_registro_ficticio = Banco(
                fecha=timezone.now().date(),
                referencia=referencia_ficticia,
                credito=monto_saldo_actual,
                registro_ficticio=True,
                sucursal=instance.credit_id.sucursal
            )
            banco_registro_ficticio.save()








        if desembolso_credito.count() > 1:
            instance.delete()
            return
        
        referencia = str(uuid.uuid4())[:8]
        

        # Usar una transacción atómica para asegurar la consistencia
        with transaction.atomic():
            try:
                # Cuando solo se está ejecutando un desembolso
                if buscar_tipo_desembolso(instance.forma_desembolso) == -1:
                    disbursement_paid = instance.monto_desembolsado
                    description = f'{instance.forma_desembolso}'
                    estado_cuenta = informacion_estado_cuenta(instance, disbursement_paid, referencia,description)
                    estado_cuenta.save()
                # Cuando se está creando un tipo de desembolso diferente a desembolsar
                else:
                    disbursement_paid = instance.monto_desembolsado
                    description = f'{instance.forma_desembolso}'
                    estado_cuenta = informacion_estado_cuenta(instance, instance.total_gastos, referencia, description)
                    estado_cuenta.save()
                    
                    if instance.monto_desembolsado > 0:
                        referencia2 = str(uuid.uuid4())[:8]
                        description2 = 'MONTO DESEMBOLSADO'
                        estado_cuenta2 = informacion_estado_cuenta(instance, disbursement_paid, referencia2,description2)
                        #estado_cuenta2.save()
            except IntegrityError:
                # En caso de colisión, generar nuevas referencias y volver a intentar
                referencia = str(uuid.uuid4())[:8]
                estado_cuenta.numero_referencia = referencia

                if 'estado_cuenta2' in locals():
                    referencia2 = str(uuid.uuid4())[:8]
                    estado_cuenta2.numero_referencia = referencia2

                estado_cuenta.save()

                if 'estado_cuenta2' in locals():
                    estado_cuenta2.save()
                    
                logger.info(f'Nueva referencia generada y guardada: {referencia}')
                if 'estado_cuenta2' in locals():
                    logger.info(f'Nueva referencia2 generada y guardada: {referencia2}')
