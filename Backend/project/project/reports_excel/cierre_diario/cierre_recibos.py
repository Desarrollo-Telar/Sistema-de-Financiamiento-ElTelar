# Reporte Excel
from openpyxl import Workbook
from django.http import HttpResponse
import json
import io
import zipfile

# Tiempo
from datetime import datetime, timedelta

# Funciones
from apps.financings.formato import formatear_numero

# Modelo
from apps.financings.models import Payment


def recibo_para(instance):
        mensaje = ''
        if instance is None:
            return mensaje
        
        pago = Payment.objects.get(id=instance)

        if pago is None:
            return mensaje
       
        if pago.acreedor:
            mensaje = f'{pago.acreedor.nombre_acreedor}'
        
        if pago.seguro:
            mensaje = f'{pago.seguro.nombre_acreedor}'
        
        if pago.credit:
            mensaje = f'{pago.credit.customer_id}'
        
      

        return mensaje

def crear_excel_recibos(data, dia = None):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Informacion Recibos"

    encabezados = [
        "#","FECHA","NUMERO DE RECIBO", "PARA", "INTERES", "INTERES PAGAGO",
        "MORA","MORA PAGADA","CAPITAL APORTADO","TOTAL","ESTA FACTURADO"
    ]


    for col_idx, header in enumerate(encabezados, start=1):
        sheet.cell(row=1, column=col_idx, value=header)

 

    contador = 0  # Para la numeración real del archivo

    for idx, recibo in enumerate(data, start=2):
        
        contador+=1
        informacion_recibo = recibo.get('informacion_recibo',{})
        
        
      
        fila = [
            contador, 
            str(informacion_recibo.get('fecha','')),
            informacion_recibo.get('recibo',''),
            str(recibo_para(informacion_recibo.get('pago_id',''))),
            formatear_numero(informacion_recibo.get('interes','')),
            formatear_numero(informacion_recibo.get('interes_pagado','')),
            formatear_numero(informacion_recibo.get('mora','')),
            formatear_numero(informacion_recibo.get('mora_pagada','')),
            formatear_numero(informacion_recibo.get('aporte_capital','')),
            formatear_numero(informacion_recibo.get('total','')),
            informacion_recibo.get('factura','')
            
            ]

        for col_idx, value in enumerate(fila, start=1):
            sheet.cell(row=idx, column=col_idx, value=value)


    return workbook
