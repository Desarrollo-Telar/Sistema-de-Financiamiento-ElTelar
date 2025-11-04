# Modelos
from apps.financings.models import Banco, Recibo, Payment, Invoice

# HISTORIAL Y BITACORA
from apps.actividades.utils import log_user_action, log_system_event
from scripts.conversion_datos import model_to_dict, cambios_realizados

def generar_informacion_bancos(sucursal):
    list_informacion_bancos = []
    bancos = Banco.objects.filter(sucursal=sucursal).order_by('id')
    
    #bancos = Banco.objects.all().order_by('id')

    for banco in bancos.iterator(chunk_size=100):
        context = {}
        context['informacion_banco'] = model_to_dict(banco)
        list_informacion_bancos.append(context)

    return list_informacion_bancos

def generar_informacion_recibos(sucursal):
    list_informacion_recibos = []
    recibos = Recibo.objects.filter(sucursal=sucursal).order_by('id')

    #recibos = Recibo.objects.all().order_by('id')

    for recibo in recibos.iterator(chunk_size=100):
        context = {}
        context['informacion_recibo'] = model_to_dict(recibo)
        list_informacion_recibos.append(context)

    return list_informacion_recibos

def generar_informacion_pagos(sucursal):
    list_informacion_pagos = []
    pagos = Payment.objects.filter(sucursal=sucursal).order_by('id')

    #pagos = Payment.objects.all().order_by('id')

    for pago in pagos.iterator(chunk_size=100):
        context = {}
        context['informacion_pagos'] = model_to_dict(pago)
        list_informacion_pagos.append(context)
    
    return list_informacion_pagos

def generar_informacion_facturas(sucursal):
    list_informacion_facturas = []
    facturas = Invoice.objects.filter(sucursal=sucursal).order_by('id')

    #facturas = Invoice.objects.all().order_by('id')
    print(f'Recolentando el total de: {facturas.count()}')

    for factura in facturas.iterator(chunk_size=100):
        context = {}
        context['informacion_factura'] = model_to_dict(factura)
        list_informacion_facturas.append(context)
    
    return list_informacion_facturas