# Modelos
from apps.accountings.models import Egress, Income, Insurance, Creditor


# HISTORIAL Y BITACORA
from apps.actividades.utils import log_user_action, log_system_event
from scripts.conversion_datos import model_to_dict, cambios_realizados

# Funciones
from .funciones import verificacion_de_status, obtener_cuota_vigente, obtener_estados_cuentas


    
def generar_informacion_acreedores(sucursal):
    acreedores = Creditor.objects.filter(sucursal=sucursal).order_by('id')

    list_acreedores = []

    for acreedor in acreedores.iterator(chunk_size=100):
        context = {
            'informacion_acreedor': model_to_dict(acreedor),
            'cuota_vigente':obtener_cuota_vigente(acreedor, 'ACREEDOR'),
            'estados_cuenta':obtener_estados_cuentas(acreedor, 'ACREEDOR')
        }
        list_acreedores.append(context)
    
    return list_acreedores

def generar_informacion_seguros(sucursal):
    seguros = Insurance.objects.filter(sucursal=sucursal).order_by('id')

    list_seguros = []

    for seguro in seguros.iterator(chunk_size=100):
        context = {
            'informacion_seguro': model_to_dict(seguro),
            'cuota_vigente':obtener_cuota_vigente(seguro, 'SEGURO'),
            'estados_cuenta':obtener_estados_cuentas(seguro, 'SEGURO')
        }
        list_seguros.append(context)
    
    return list_seguros

def generar_informacion_ingresos(sucursal):
    ingresos = Income.objects.filter(sucursal=sucursal).order_by('id')

    list_ingresos = []

    for ingreso in ingresos.iterator(chunk_size=100):
        verificacion_de_status(ingreso)
        context = {
            'informacion_ingreso': model_to_dict(ingreso)            
        }
        list_ingresos.append(context)
    
    return list_ingresos

def generar_informacion_egresos(sucursal):
    egresos = Egress.objects.filter(sucursal=sucursal).order_by('id')

    list_egresos = []

    for egreso in egresos.iterator(chunk_size=100):
        verificacion_de_status(egreso)
        context = {
            'informacion_egreso': model_to_dict(egreso)            
        }
        list_egresos.append(context)
    
    return list_egresos

