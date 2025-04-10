from apps.financings.models import Banco, Payment, Recibo
from openpyxl import Workbook
from django.http import HttpResponse
import json

from openpyxl import Workbook
from django.db.models import Q, Sum


def report_filtro_banco(filters):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Reporte de Bancos"

    # Agregar encabezados
    sheet['A1'] = "STATUS"
    sheet['B1'] = "FECHA"
    sheet['C1'] = "DESCRIPCION"
    sheet['D1'] = "REFERENCIA"
    sheet['E1'] = "SECUENCIAL"
    sheet['F1'] = "CHEQUE PROPIO/LOCAL/EFECTIVO"
    sheet['G1'] = "DEBITO(-)"
    sheet['H1'] = "CREDITO(+)"
    sheet['I1'] = "SALDO CONTABLE"
    sheet['J1'] = "SALDO DISPONIBLE"
    sheet['L1'] = "MONTO REF COMPARATIVA"
    sheet['M1'] = "TIPO DE PAGO"
    sheet['N1'] = "DESCRIPCION"
    sheet['O1'] = "FECHA"
    sheet['P1'] = "PARA"

    # Obtener datos de la base de datos, ordenando por status (True primero)
    bancos = Banco.objects.filter(filters).order_by('-status')  # True primero, luego False

    # Agregar datos al archivo
    for idx, banco in enumerate(bancos, start=2):  # Comenzar en la fila 2
        numero_referencia = banco.referencia

        # Buscar el objeto Payment asociado
        boleta = Payment.objects.filter(numero_referencia=numero_referencia).first()

        sheet[f'A{idx}'] = banco.status
        sheet[f'B{idx}'] = banco.fecha
        sheet[f'C{idx}'] = banco.descripcion
        sheet[f'D{idx}'] = banco.referencia
        sheet[f'E{idx}'] = banco.secuencial
        sheet[f'F{idx}'] = banco.cheque
        sheet[f'G{idx}'] = banco.debito
        sheet[f'H{idx}'] = banco.credito
        sheet[f'I{idx}'] = banco.saldo_contable
        sheet[f'J{idx}'] = banco.saldo_disponible

        # Agregar datos de boleta si existe
        if boleta:
            sheet[f'L{idx}'] = boleta.monto
            sheet[f'M{idx}'] = boleta.tipo_pago
            sheet[f'N{idx}'] = boleta.descripcion
            sheet[f'O{idx}'] = boleta.fecha_emision.date()
            if boleta.acreedor:
                sheet[f'P{idx}'] = str(boleta.acreedor)
            elif boleta.seguro:
                sheet[f'P{idx}'] = str(boleta.seguro)
            elif boleta.cliente:
                sheet[f'P{idx}'] = str(boleta.cliente)
            elif boleta.credit:
                sheet[f'P{idx}'] = str(boleta.credit)
                
            elif boleta.disbursement:
                sheet[f'P{idx}'] = str(boleta.disbursement)
            
            else:
                sheet[f'P{idx}'] = str(boleta.descripcion)




    # Crear respuesta HTTP para descargar el archivo
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = 'attachment; filename="reporte_bancos.xlsx"'

    # Guardar el archivo en la respuesta
    workbook.save(response)
    return response

def report_banco(request):
    # Crear el archivo Excel
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Reporte de Bancos"

    # Agregar encabezados
    sheet['A1'] = "STATUS"
    sheet['B1'] = "FECHA"
    sheet['C1'] = "DESCRIPCION"
    sheet['D1'] = "REFERENCIA"
    sheet['E1'] = "SECUENCIAL"
    sheet['F1'] = "CHEQUE PROPIO/LOCAL/EFECTIVO"
    sheet['G1'] = "DEBITO(-)"
    sheet['H1'] = "CREDITO(+)"
    sheet['I1'] = "SALDO CONTABLE"
    sheet['J1'] = "SALDO DISPONIBLE"
    sheet['L1'] = "MONTO REF COMPARATIVA"
    sheet['M1'] = "TIPO DE PAGO"
    sheet['N1'] = "DESCRIPCION"
    sheet['O1'] = "FECHA"
    sheet['P1'] = "PARA"

    # Obtener datos de la base de datos, ordenando por status (True primero)
    bancos = Banco.objects.filter(registro_ficticio = False).order_by('-status')  # True primero, luego False

    # Agregar datos al archivo
    for idx, banco in enumerate(bancos, start=2):  # Comenzar en la fila 2
        numero_referencia = banco.referencia

        # Buscar el objeto Payment asociado
        boleta = Payment.objects.filter(numero_referencia=numero_referencia).first()

        sheet[f'A{idx}'] = banco.status
        sheet[f'B{idx}'] = banco.fecha
        sheet[f'C{idx}'] = banco.descripcion
        sheet[f'D{idx}'] = banco.referencia
        sheet[f'E{idx}'] = banco.secuencial
        sheet[f'F{idx}'] = banco.cheque
        sheet[f'G{idx}'] = banco.debito
        sheet[f'H{idx}'] = banco.credito
        sheet[f'I{idx}'] = banco.saldo_contable
        sheet[f'J{idx}'] = banco.saldo_disponible

        # Agregar datos de boleta si existe
        if boleta:
            sheet[f'L{idx}'] = boleta.monto
            sheet[f'M{idx}'] = boleta.tipo_pago
            sheet[f'N{idx}'] = boleta.descripcion
            sheet[f'O{idx}'] = boleta.fecha_emision.date()
            if boleta.acreedor:
                sheet[f'P{idx}'] = str(boleta.acreedor)
            elif boleta.seguro:
                sheet[f'P{idx}'] = str(boleta.seguro)
            elif boleta.cliente:
                sheet[f'P{idx}'] = str(boleta.cliente)
            elif boleta.credit:
                sheet[f'P{idx}'] = str(boleta.credit)
                
            elif boleta.disbursement:
                sheet[f'P{idx}'] = str(boleta.disbursement)
            
            else:
                sheet[f'P{idx}'] = str(boleta.descripcion)




    # Crear respuesta HTTP para descargar el archivo
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = 'attachment; filename="reporte_bancos.xlsx"'

    # Guardar el archivo en la respuesta
    workbook.save(response)
    return response


