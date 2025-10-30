# Modelos
from apps.financings.models import Banco, Payment, PaymentPlan, AccountStatement
from apps.accountings.models import Egress, Income, Insurance, Creditor
from django.db.models import Q

# TIEMPO
from datetime import datetime, time, timedelta
from django.utils.timezone import now

# HISTORIAL Y BITACORA
from apps.actividades.utils import log_user_action, log_system_event
from scripts.conversion_datos import model_to_dict, cambios_realizados

def verificacion_de_status(instance):
    referencia = instance.numero_referencia

    if instance.status:
        return f'{instance} ya se encuentra verificado'

    banco = Banco.objects.filter(referencia=referencia).first()
    boleta = Payment.objects.filter(numero_referencia=referencia).first()

    if banco is None:
        log_system_event(
            f'No hay registro en bancos de este numero de referencia {referencia} para {instance}.',
            'INFO',
            'Sistema','Contable',None,model_to_dict(instance)
        )
        return f'No hay registro en bancos de este numero de referencia {referencia} para {instance}.'
    
    if boleta is None:
        log_system_event(
            f'No hay registro en boletas para este numero de referencia {referencia} para {instance}.',
            'INFO',
            'Sistema','Contable',None,model_to_dict(instance)
        )
        return f'No hay registro en boletas para este numero de referencia {referencia} para {instance}.'
    
    if banco.status and boleta.estado_transaccion == 'COMPLETADO':
        instance.status = True
        instance.save()

        log_system_event(
            f'Validando para {instance}.',
            'INFO',
            'Sistema','Contable',None,model_to_dict(instance)
        )
        return f'Validando para {instance}.'
    
    if boleta.estado_transaccion == 'COMPLETADO':
        banco.status = True
        banco.save()

        instance.status = True
        instance.save()

        log_system_event(
            f'Validando para {instance}.',
            'INFO',
            'Sistema','Contable',None,model_to_dict(instance)
        )
        return f'Validando para {instance}.'
    
    if banco.status:
        boleta.estado_transaccion = 'COMPLETADO'
        boleta.save()

        instance.status = True
        instance.save()

        log_system_event(
            f'Validando para {instance}.',
            'INFO',
            'Sistema','Contable',None,model_to_dict(instance)
        )
        return f'Validando para {instance}.'

def obtener_cuota_vigente(credito,tipo):
    dia = datetime.now().date()
    dia_mas_uno = dia + timedelta(days=1)
    filters = Q()

    if tipo == 'ACREEDOR':
        filters = Q(acreedor= Creditor.objects.get(id=credito.id))
    
    elif tipo == 'SEGURO':
        filters = Q(seguro = Insurance.objects.get(id=credito.id))
    
    else:
        return None
    
    siguiente_pago = PaymentPlan.objects.filter(       
        Q(start_date__lte=dia) & Q(fecha_limite__gte=dia_mas_uno) & ( filters )
    ).first()

    if siguiente_pago is None:
        siguiente_pago = PaymentPlan.objects.filter(filters).order_by('-id').first()
    
    if siguiente_pago is not None:
        return model_to_dict(siguiente_pago)
    return None

def obtener_estados_cuentas(credito, tipo):
    filters = Q()

    if tipo == 'ACREEDOR':
        filters = Q(acreedor= Creditor.objects.get(id=credito.id))
    
    elif tipo == 'SEGURO':
        filters = Q(seguro = Insurance.objects.get(id=credito.id))
    
    else:
        return None
    

    estados_cuenta = AccountStatement.objects.filter(filters).order_by('id')
    list_estados_cuenta = []

    if not estados_cuenta.exists():
        return None
    
    for estado_cuenta in estados_cuenta:
        list_estados_cuenta.append(model_to_dict(estado_cuenta))
    
    return list_estados_cuenta