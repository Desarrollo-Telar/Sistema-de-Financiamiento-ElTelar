
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
import asyncio
import time

# Funciones
from .informacion_relacionada_credito import obtener_cuota_vigente, obtener_desembolsos_credito, obtener_garantias, obtener_estados_cuentas

import asyncio
from datetime import datetime
from asgiref.sync import sync_to_async
from django.forms.models import model_to_dict

@sync_to_async
def obtener_informacion_laboral_sync(cliente):
    informacion_laboral = WorkingInformation.objects.filter(customer_id=cliente)
    if not informacion_laboral.exists():
        informacion_laboral = OtherSourcesOfIncome.objects.filter(customer_id=cliente)
    if not informacion_laboral.exists():
        cliente.completado = False
        cliente.save()
        return None
    return model_to_dict(informacion_laboral.order_by('-id').first())


@sync_to_async
def obtener_referencias_sync(cliente):
    referencias = Reference.objects.filter(customer_id=cliente)
    if not referencias.exists():
        cliente.completado = False
        cliente.save()
        return None
    return [model_to_dict(ref) for ref in referencias]


@sync_to_async
def obtener_plan_de_inversion_sync(cliente):
    planes = InvestmentPlan.objects.filter(customer_id=cliente)
    if not planes.exists():
        return None
    return [model_to_dict(plan) for plan in planes]


@sync_to_async
def obtener_direcciones_sync(cliente):
    direcciones = Address.objects.filter(customer_id=cliente)
    if not direcciones.exists():
        cliente.completado = False
        cliente.save()
        return None
    return [model_to_dict(d) for d in direcciones]


@sync_to_async
def obtener_informacion_creditos_sync(cliente, sucursal, dia=None):
    if dia is None:
        dia = datetime.now().date()

    creditos = Credit.objects.filter(customer_id=cliente, sucursal=sucursal).order_by('id')
    context = {'cantidad': creditos.count()}

    if creditos.exists():
        list_creditos = []
        for credito in creditos.iterator(chunk_size=100):
            context_credito = {
                'credito': model_to_dict(credito),
                'cuota_vigente': obtener_cuota_vigente(credito, dia),
                'desembolsos': obtener_desembolsos_credito(credito),
                'garantia': obtener_garantias(credito),
                'estados_cuentas': obtener_estados_cuentas(credito)
            }
            list_creditos.append(context_credito)
        context['creditos'] = list_creditos

    return context


async def obtener_informacion_creditos_sucursal(sucursal,dia= None):  
    creditos = Credit.objects.filter(sucursal=sucursal).order_by('id')

    list_creditos = []

    if creditos.exists():

        for credito in creditos.iterator(chunk_size=100):            
            context_credito = {}
            context_credito['credito'] = model_to_dict(credito)
            context_credito['cuota_vigente'] = obtener_cuota_vigente(credito,dia)
            context_credito['desembolsos']=obtener_desembolsos_credito(credito)
            context_credito['garantia'] = obtener_garantias(credito)
            context_credito['estados_cuentas'] = obtener_estados_cuentas(credito)

            list_creditos.append(context_credito)
            
    return list_creditos

@sync_to_async
def obtener_clientes_por_sucursal(sucursal):
    return list(Customer.objects.filter(sucursal=sucursal).order_by('id'))


async def generando_informacion_cliente(sucursal, dia=None):
    if dia is None:
        dia = datetime.now().date()

    clientes = await obtener_clientes_por_sucursal(sucursal)
    list_informacion = []

    for cliente in clientes:
        # Ejecutar las funciones en paralelo para cada cliente
        (
            info_laboral,
            plan_inversion,
            referencias,
            direcciones,
            info_creditos,
        ) = await asyncio.gather(
            obtener_informacion_laboral_sync(cliente),
            obtener_plan_de_inversion_sync(cliente),
            obtener_referencias_sync(cliente),
            obtener_direcciones_sync(cliente),
            obtener_informacion_creditos_sync(cliente, sucursal, dia),
        )

        context = {
            'informacion_personal': model_to_dict(cliente),
            'informacion_laboral': info_laboral,
            'informacion_plan_inversion': plan_inversion,
            'informacion_referencias': referencias,
            'direcciones': direcciones,
            'informacion_credito': info_creditos,
        }

        list_informacion.append(context)

    return list_informacion


