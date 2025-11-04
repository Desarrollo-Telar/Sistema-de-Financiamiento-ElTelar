
from apps.customers.models import Customer
from apps.addresses.models import Address
from apps.FinancialInformation.models import Reference, OtherSourcesOfIncome, WorkingInformation
from apps.InvestmentPlan.models import InvestmentPlan
from apps.financings.models import Credit

# HISTORIAL Y BITACORA
from apps.actividades.utils import log_user_action, log_system_event
from scripts.conversion_datos import model_to_dict, cambios_realizados

# Tiempo
from datetime import datetime,timedelta

# Funciones
from .informacion_relacionada_credito import obtener_cuota_vigente, obtener_desembolsos_credito, obtener_garantias, obtener_estados_cuentas

def obtener_informacion_laboral(cliente):
    informacion_laboral = WorkingInformation.objects.filter(customer_id=cliente)
    list_informacion = None

    if not informacion_laboral.exists():
        informacion_laboral = OtherSourcesOfIncome.objects.filter(customer_id=cliente)
    
    if not informacion_laboral.exists():
        cliente.completado = False
        cliente.save()
        return None
    
    
    list_informacion = model_to_dict(informacion_laboral.order_by('-id').first())


    return list_informacion

def obtener_referencias(cliente):
    referencias = Reference.objects.filter(customer_id=cliente)

    list_referencias = []

    if not referencias.exists():
        cliente.completado = False
        cliente.save()
        return None
    
    for referencia in referencias:
        list_referencias.append(model_to_dict(referencia))
    
    return list_referencias

def obtener_plan_de_inversion(cliente):
    plan_inversion = InvestmentPlan.objects.filter(customer_id=cliente)
    list_plan_inversion = []

    if not plan_inversion.exists():
        return None
    
    for plan_de_inversion in plan_inversion:
        list_plan_inversion.append(model_to_dict(plan_de_inversion))

    return list_plan_inversion

def obtener_direcciones(cliente):
    direcciones = Address.objects.filter(customer_id=cliente)
    list_direcciones = []

    if not direcciones.exists():
        cliente.completado = False
        cliente.save()
        return None
    
    for direccion in direcciones:
        list_direcciones.append(model_to_dict(direccion))
    
    return list_direcciones


def obtener_informacion_creditos(cliente, sucursal,dia= None):  
    if dia is None:
        dia = datetime.now().date()
    creditos = Credit.objects.filter(customer_id=cliente, sucursal=sucursal).order_by('id')

    context = {
        'cantidad':creditos.count()
    }

    if creditos.exists():
        list_creditos = []
        

        for credito in creditos:
            print(f'{credito}')
            context_credito = {}
            context_credito['credito'] = model_to_dict(credito)
            context_credito['cuota_vigente'] = obtener_cuota_vigente(credito, dia)
            context_credito['desembolsos']=obtener_desembolsos_credito(credito)
            context_credito['garantia'] = obtener_garantias(credito)
            context_credito['estados_cuentas'] = obtener_estados_cuentas(credito)

            list_creditos.append(context_credito)
        
        context['creditos'] = list_creditos
            

    return context

def obtener_informacion_creditos_sucursal( sucursal,dia= None):  
    creditos = Credit.objects.filter(sucursal=sucursal).order_by('id')

    list_creditos = []

    if creditos.exists():

        for credito in creditos.iterator(chunk_size=100):
            print(f'{credito}')
            context_credito = {}
            context_credito['credito'] = model_to_dict(credito)
            context_credito['cuota_vigente'] = obtener_cuota_vigente(credito,dia)
            context_credito['desembolsos']=obtener_desembolsos_credito(credito)
            context_credito['garantia'] = obtener_garantias(credito)
            context_credito['estados_cuentas'] = obtener_estados_cuentas(credito)

            list_creditos.append(context_credito)
        
    return list_creditos



def generando_informacion_cliente(sucursal, dia=None, chunk_size=100):
    if dia is None:
        dia = datetime.now().date()
    list_informacion_relacionada_cliente = []

    queryset = Customer.objects.filter(sucursal=sucursal).order_by('id')

    for clientes_chunk in queryset.iterator(chunk_size=chunk_size):
        context = {}
        cliente = clientes_chunk

        context['informacion_laboral'] = obtener_informacion_laboral(cliente)
        context['informacion_plan_inversion'] = obtener_plan_de_inversion(cliente)
        context['informacion_referencias'] = obtener_referencias(cliente)
        context['direcciones'] = obtener_direcciones(cliente)
        context['informacion_credito'] = obtener_informacion_creditos(cliente, sucursal, dia)
        context['informacion_personal'] = model_to_dict(cliente, 'uuid')

        list_informacion_relacionada_cliente.append(context)

    return list_informacion_relacionada_cliente


