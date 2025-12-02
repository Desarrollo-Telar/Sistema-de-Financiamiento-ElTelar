
from apps.financings.models import Credit, PaymentPlan, Disbursement, DetailsGuarantees, AccountStatement

# HISTORIAL Y BITACORA
from apps.actividades.utils import log_user_action, log_system_event
from scripts.conversion_datos import model_to_dict, cambios_realizados
# Tiempo
from datetime import datetime,timedelta

import time, gc, os, json

def obtener_cuota_vigente(credito, dia = None):
    gc.collect() 
    if dia is None:
        dia = datetime.now().date()
        
    dia_mas_uno = dia + timedelta(days=1)
    
    siguiente_pago = PaymentPlan.objects.filter(
        credit_id=credito,
        start_date__lte=dia,
        fecha_limite__gte=dia_mas_uno
    ).first()

    if siguiente_pago is None:
        siguiente_pago = PaymentPlan.objects.filter(
        credit_id=credito).order_by('-id').first()
    
    if siguiente_pago is not None:
        return model_to_dict(siguiente_pago)
    
    return None

def obtener_desembolsos_credito(credito):
    gc.collect() 
    desembolsos = Disbursement.objects.filter(credit_id=credito).order_by('id')
    list_desembolsos = []

    if not desembolsos.exists():
        return None
    
    for desembolso in desembolsos.iterator(chunk_size=100):
        list_desembolsos.append(model_to_dict(desembolso))
    
    return list_desembolsos

def obtener_garantias(credito):
    gc.collect() 
    garantias = DetailsGuarantees.objects.filter(garantia_id__credit_id=credito).order_by('id')
    list_garantias = []

    if not garantias.exists():
        return None
    
    for garantia in garantias.iterator(chunk_size=100):
        list_garantias.append(model_to_dict(garantia))
    
    return list_garantias

def obtener_estados_cuentas(credito):
    gc.collect() 
    estados_cuenta = AccountStatement.objects.filter(credit=credito).order_by('id')
    list_estados_cuenta = []

    if not estados_cuenta.exists():
        return None
    
    for estado_cuenta in estados_cuenta.iterator(chunk_size=100):
        list_estados_cuenta.append(model_to_dict(estado_cuenta))
    
    return list_estados_cuenta

def obtener_informacion_creditos(sucursal): 
    gc.collect() 
    creditos = Credit.objects.filter(sucursal=sucursal).order_by('id')

    list_creditos = []

    if creditos.exists():

        for credito in creditos.iterator(chunk_size=100):            
            context_credito = {}
            context_credito['credito'] = model_to_dict(credito)
            context_credito['cuota_vigente'] = obtener_cuota_vigente(credito)
            context_credito['desembolsos']=obtener_desembolsos_credito(credito)
            context_credito['garantia'] = obtener_garantias(credito)
            context_credito['estados_cuentas'] = obtener_estados_cuentas(credito)

            list_creditos.append(context_credito)
        
    return list_creditos
            