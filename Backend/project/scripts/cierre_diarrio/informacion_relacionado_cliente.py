
from apps.customers.models import Customer
from apps.customers.api.serializers import CustomerSerializer

from apps.addresses.models import Address
from apps.FinancialInformation.models import Reference, OtherSourcesOfIncome, WorkingInformation
from apps.InvestmentPlan.models import InvestmentPlan
from apps.financings.models import Credit

# HISTORIAL Y BITACORA
from apps.actividades.utils import log_user_action, log_system_event
from scripts.conversion_datos import model_to_dict, cambios_realizados

# Tiempo
from datetime import datetime,timedelta

import time, gc, os, json

def obtener_informacion_laboral(cliente):
    gc.collect() 
    informacion_laboral = WorkingInformation.objects.filter(customer_id=cliente)
    list_informacion = None

    if not informacion_laboral.exists():
        informacion_laboral = OtherSourcesOfIncome.objects.filter(customer_id=cliente)
    
    if not informacion_laboral.exists():
        return None
    
    
    list_informacion = model_to_dict(informacion_laboral.order_by('-id').first())


    return list_informacion

def obtener_referencias(cliente):
    gc.collect() 
    referencias = Reference.objects.filter(customer_id=cliente)

    list_referencias = []

    if not referencias.exists():
        return None
    
    for referencia in referencias:
        list_referencias.append(model_to_dict(referencia))
    
    return list_referencias

def obtener_plan_de_inversion(cliente):
    gc.collect() 
    plan_inversion = InvestmentPlan.objects.filter(customer_id=cliente)
    list_plan_inversion = []

    if not plan_inversion.exists():
        return None
    
    for plan_de_inversion in plan_inversion:
        list_plan_inversion.append(model_to_dict(plan_de_inversion))

    return list_plan_inversion

def obtener_direcciones(cliente):
    gc.collect() 
    direcciones = Address.objects.filter(customer_id=cliente)
    list_direcciones = []

    if not direcciones.exists():
        return None
    
    for direccion in direcciones:
        list_direcciones.append(model_to_dict(direccion))
    
    return list_direcciones

def generando_informacion_cliente(sucursal):
    context = {}
    
    for cliente in Customer.objects.filter(sucursal=sucursal).order_by('id').iterator(chunk_size=100):

        context['informacion_personal'] = model_to_dict(cliente)
        context['informacion_laboral'] = obtener_informacion_laboral(cliente) 
        context['informacion_plan_inversion'] =  obtener_plan_de_inversion(cliente) 
        context['informacion_referencias'] = obtener_referencias(cliente) 
        context['direcciones'] = obtener_direcciones(cliente) 
        
    return context


