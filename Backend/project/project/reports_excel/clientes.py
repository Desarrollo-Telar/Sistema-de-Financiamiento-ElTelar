
from openpyxl import Workbook
from django.http import HttpResponse
import json

from django.db.models import Q, Sum

from datetime import datetime

# MODELOS
from apps.customers.models import Customer
from apps.financings.models import Credit

def informacion_credito(creditos):
    return creditos.first() if creditos.exists() else None


def report_clientes(request):
    # Crear el archivo Excel
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Reporte de cartera de Creditos"

    # Agregar encabezados
    sheet['A1'] = "#"
    sheet['B1'] = "NOMBRE"
    sheet['C1'] = "TIPO DE IDENTIFICACION"
    sheet['D1'] = "NUMERO DE IDENTIFICACION"
    sheet['E1'] = "NUMERO DE TELEFONO"
    sheet['F1'] = "EDAD"
    sheet['G1'] = "GENERO"
    sheet['H1'] = "CODIGO DE CLIENTE"
    sheet['I1'] = "PROFESION U OFICIO"
    sheet['J1'] = "ASESOR DEL CREDITO"
    sheet['K1'] = "TIENE CREDITO"
    sheet['L1'] = "CANTIDAD DE CREDITOS"
    sheet['M1'] = "CODIGO DE CREDITO"
    sheet['N1'] = "EL CREDITO ESTA VIGENTE"
    sheet['O1'] = "PROPOSITO"
    sheet['P1'] = "MONTO"
    sheet['Q1'] = "PLAZO"
    sheet['R1'] = "TASA DE INTERES"

    # Obtener datos de la base de datos, ordenando por status (True primero)
    clientes = Customer.objects.all()
    contador = 0

    # Agregar datos al archivo
    for idx, cliente in enumerate(clientes, start=2):  # Comenzar en la fila 2
        contador += 1
        creditos = Credit.objects.filter(customer_id__id=cliente.id).order_by('-id')
        primer_credito = creditos.first()
        mensaje = ''

        if primer_credito:
            mensaje = 'CREDITO CANCELADO' if primer_credito.is_paid_off else 'CREDITO VIGENTE'

        sheet[f'A{idx}'] = contador
        sheet[f'B{idx}'] = str(cliente)
        sheet[f'C{idx}'] = str(cliente.type_identification)
        sheet[f'D{idx}'] = str(cliente.identification_number)
        sheet[f'E{idx}'] = cliente.telephone
        sheet[f'F{idx}'] = str(cliente.get_age())
        sheet[f'G{idx}'] = cliente.gender
        sheet[f'H{idx}'] = cliente.customer_code
        sheet[f'I{idx}'] = cliente.profession_trade
        sheet[f'J{idx}'] = cliente.asesor
        sheet[f'K{idx}'] = 'SI' if creditos else 'NO CUENTA CON CREDITOS REGISTRADOS'
        sheet[f'L{idx}'] =  str(creditos.count()) if creditos else '0'
        sheet[f'M{idx}'] = str(primer_credito.codigo_credito) if primer_credito else ''
        sheet[f'N{idx}'] = mensaje if primer_credito else ''
        sheet[f'O{idx}'] = primer_credito.proposito if primer_credito else ''
        sheet[f'P{idx}'] = primer_credito.monto if primer_credito else ''
        sheet[f'Q{idx}'] = primer_credito.plazo if primer_credito else ''
        sheet[f'R{idx}'] = primer_credito.tasa_mensual() if primer_credito else ''
        

    

       




    # Crear respuesta HTTP para descargar el archivo
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = f'attachment; filename="reporte_cartera_creditos_{datetime.now()}.xlsx"'

    # Guardar el archivo en la respuesta
    workbook.save(response)
    return response


