from apps.financings.models import Payment, Recibo

from apps.accountings.models import Egress, Income
from openpyxl import Workbook
from django.http import HttpResponse
import json

from openpyxl import Workbook
from django.db.models import Q, Sum

from datetime import datetime



def report_base_boletas(request):
    # Crear el archivo Excel
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Reporte de base de Boletas"

    # Agregar encabezados
    sheet['A1'] = "#"
    sheet['B1'] = "REFERENCIA"
    sheet['C1'] = "FECHA"
    sheet['D1'] = "MONTO"
    sheet['E1'] = "CODIGO"
    sheet['F1'] = "NOMBRE"
    sheet['G1'] = "MORA"
    sheet['H1'] = "INTERES"
    sheet['I1'] = "CAPITAL"
    sheet['J1'] = "NIT/CUI"
    sheet['L1'] = "SUMA"
    sheet['M1'] = "DIFERENCIA"
    sheet['N1'] = "FACTURA"
    sheet['O1'] = "RECIBO"
    

    # Obtener datos de la base de datos, ordenando por status (True primero)
    boletas = Payment.objects.filter(registro_ficticio = False, estado_transaccion='COMPLETADO').order_by('-id')  # True primero, luego False
    contador = 0

    # Agregar datos al archivo
    for idx, boleta in enumerate(boletas, start=2):  # Comenzar en la fila 2
        contador += 1
        
        codigo = '---'

        mora = 0
        interes = 0
        capital = 0

        cui = '---'

        suma = 0
        diferencia = 0
        nombre = 'ELTELAR'
        cui = '---'

        factura = 'NO'
        recibo_p = 'NO'

        recibo = Recibo.objects.filter(pago__id=boleta.id).first()

        if boleta.credit is not None:
            codigo = boleta.credit.codigo_credito
            nombre = boleta.credit.customer_id

            cui = boleta.credit.customer_id.identification_number

        elif boleta.acreedor is not None:
            codigo = boleta.acreedor.codigo_acreedor
            nombre = boleta.acreedor.nombre_acreedor
            

        elif boleta.seguro is not None:
            codigo = boleta.seguro.codigo_seguro
            nombre = boleta.seguro.nombre_acreedor

        else:
            codigo = boleta.tipo_pago

            if boleta.cliente is not None:
                nombre = boleta.cliente
                cui = boleta.cliente.identification_number
                codigo = boleta.cliente.customer_code
            
            if boleta.tipo_pago == 'EGRESO':
                egreso = Egress.objects.filter(numero_referencia=boleta.numero_referencia).first()
                codigo = egreso.codigo_egreso
                cui = egreso.nit if egreso.nit else '---'
                nombre = egreso.nombre if egreso.nombre else egreso.observaciones

            elif boleta.tipo_pago == 'INGRESO':
                ingreso = Income.objects.filter(numero_referencia=boleta.numero_referencia).first()
                codigo = ingreso.codigo_ingreso


        
        if recibo is not None:
            mora = recibo.mora_pagada
            interes = recibo.interes_pagado
            capital = recibo.aporte_capital

            suma = mora + interes + capital
            diferencia = boleta.monto - suma

            recibo_p = 'SI'

            factura = 'SI' if recibo.factura else 'NO'

        

        sheet[f'A{idx}'] = contador
        sheet[f'B{idx}'] = boleta.numero_referencia
        sheet[f'C{idx}'] = str(boleta.fecha_emision.date())
        sheet[f'D{idx}'] = f'Q {boleta.Fmonto()}'

        sheet[f'E{idx}'] = codigo


        sheet[f'F{idx}'] = str(nombre)
        sheet[f'G{idx}'] = mora
        sheet[f'H{idx}'] = interes
        sheet[f'I{idx}'] = capital
        sheet[f'J{idx}'] = cui
        sheet[f'L{idx}'] = suma
        sheet[f'M{idx}'] = diferencia

        sheet[f'N{idx}'] = factura
        sheet[f'O{idx}'] = recibo_p

       




    # Crear respuesta HTTP para descargar el archivo
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = f'attachment; filename="reporte_bolestas_{datetime.now()}.xlsx"'

    # Guardar el archivo en la respuesta
    workbook.save(response)
    return response


