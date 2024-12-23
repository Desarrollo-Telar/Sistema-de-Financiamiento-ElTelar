from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.dispatch import receiver
from django.core.exceptions import ValidationError
# LOGGER
from apps.financings.clases.personality_logs import logger
# MODELOS
from apps.financings.models import AccountStatement, Disbursement, Credit, PaymentPlan

# CALCULOS
from apps.financings.calculos import calculo_interes

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
    estado_cuenta = AccountStatement(
        credit=instance.credit_id,
        disbursement=instance,
        disbursement_paid=disbursement_paid,
        numero_referencia=referencia,
        description=description,
        saldo_pendiente=instance.total_t
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
    total_desembolso = Disbursement.objects.filter(credit_id=instance.credit_id.id).aggregate(
        total_gastos_sum=Sum('total_gastos')
    )['total_gastos_sum'] or 0  # Sumar todos los gastos previos, manejando None como 0

    # Incluir el monto del desembolso actual
    total_desembolso += instance.total_gastos
    instance.total_t = total_desembolso

    if total_desembolso > total_credito:
        credito_desembolsado(instance)
        #raise ValidationError('El monto total desembolsado excede el monto del crédito.')
    
    if total_desembolso == total_credito:
        # Indicar que ya se desembolsó completamente
        credito_desembolsado(instance)

    # Registrar información adicional
    logger.info(f'Total desembolsado: {total_desembolso}, Total crédito: {total_credito}')

# EL DESEMBOLSO REALIZADO SE REFLEJA EN EL ESTADO DE CUENTAS DEL CLIENTE
@receiver(post_save, sender=Disbursement)
def reflejar_estado_cuenta(sender, instance, created, **kwargs):
    if created:
        desembolso_credito = Disbursement.objects.filter(
            credit_id_id=instance.credit_id.id, 
            forma_desembolso='APLICACIÓN GASTOS'
        )

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
