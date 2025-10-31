# Reporte Excel
from openpyxl import Workbook
from django.http import HttpResponse
import json
import io
import zipfile

# Tiempo
from datetime import datetime, timedelta
from .filtros.creditos import formater_fecha

def get_puesto(source_of_income, cliente):
        puesto_cliente = ''

        if source_of_income != 'Otra':
            puesto_cliente = cliente['informacion_laboral']['position']
        else:
            puesto_cliente = 'Otra Fuente de Ingreso'

        return puesto_cliente

def get_empresa_laburo(source_of_income, cliente):
        empresa_laburo_cliente = ''
        if source_of_income != 'Otra':
            empresa_laburo_cliente = cliente['informacion_laboral']['company_name']
        else:
            
            empresa_laburo_cliente = source_of_income

        return empresa_laburo_cliente

def get_estado_laboral(source_of_income, cliente):
        estado_laboral_cliente = ''

        if source_of_income != 'Otra':
            estado_laboral_cliente = cliente['informacion_laboral']['employment_status']
        else:
            estado_laboral_cliente = 'COMPLETO'

        return estado_laboral_cliente

def get_edad(date_birth):
        from datetime import date
        """
        Calcula la edad de la persona en base a su fecha de nacimiento.
        Devuelve None si la fecha de nacimiento no está definida.
        """
        if not date_birth:
            return None  # O 0, según cómo quieras manejarlo

        today = date.today()
        date_birth = formater_fecha(date_birth)
        age = today.year - date_birth.year

        # Si aún no ha llegado su cumpleaños este año, restamos 1
        if (today.month, today.day) < (date_birth.month, date_birth.day):
            age -= 1

        return age

def crear_excel_clientes(data, dia = None):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Informacion Personal"

    encabezados = [
        "#",
        "NOMBRE",
        "TIPO DE IDENTIFICACION",
        "NUMERO DE IDENTIFICACION",
        "NUMERO DE TELEFONO",
        "EDAD",
        "GENERO",
        "CODIGO DE CLIENTE",
        "PROFESION U OFICIO",
        "ASESOR DEL CREDITO",
        "TIENE CREDITO",
        "CANTIDAD DE CREDITOS",
        "DIRECCION DEL CLIENTE",
        "MUNICIPIO DEL CLIENTE",
        "DEPARTAMENTO DEL CLIENTE",
        "DIRECCION DE TRABAJO",
        "MUNICIPIO DE LABORAL",
        "DEPARTAMENTO DE LABORAL",
        "FUENTE DE INGRESO",
        "ESTADO LABORAL",
        "EMPRESA DE LABORAL",
        "PUESTO",
        "REFERENCIA 1",
        "REFERENCIA 2",
        "REFERENCIA 3",
        "REFERENCIA 4",
    ]


    for col_idx, header in enumerate(encabezados, start=1):
        sheet.cell(row=1, column=col_idx, value=header)

 

    contador = 0  # Para la numeración real del archivo

    for idx, cliente in enumerate(data, start=2):
        tiene_creditos = f'SI' if cliente['informacion_credito']['cantidad'] > 0 else f'NO'
        contador+=1


        fila = [
            contador, 
            f'{cliente['informacion_personal']['first_name']} {cliente['informacion_personal']['last_name']}',
            f'{cliente['informacion_personal']['type_identification']}',
            f'{cliente['informacion_personal']['identification_number']}',
            f'{cliente['informacion_personal']['telephone']}',
            f'{str(get_edad(cliente['informacion_personal']['date_birth']))}',
            f'{cliente['informacion_personal']['gender']}',
            f'{cliente['informacion_personal']['customer_code']}',
            f'{cliente['informacion_personal']['profession_trade']}',
            f'{cliente['informacion_personal']['asesor']}',
            f'{ tiene_creditos }',
            f'{cliente['informacion_credito']['cantidad']}',
            f'{cliente['direcciones'][0]['street']}',
            f'{cliente['direcciones'][0]['state']}',
            f'{cliente['direcciones'][0]['city']}',
            f'{cliente['direcciones'][1]['street']}',
            f'{cliente['direcciones'][1]['state']}',
            f'{cliente['direcciones'][1]['city']}',


            f'{cliente['informacion_laboral']['source_of_income']}',           
            f'{ get_estado_laboral(cliente['informacion_laboral']['source_of_income'], cliente)}',
            f'{ get_empresa_laburo(cliente['informacion_laboral']['source_of_income'], cliente)}',
            f'{ get_puesto(cliente['informacion_laboral']['source_of_income'], cliente)}',
            
            f'{cliente['informacion_referencias'][0]['full_name']}', 
            f'{cliente['informacion_referencias'][1]['full_name']}',
            f'{cliente['informacion_referencias'][2]['full_name']}',
            f'{cliente['informacion_referencias'][3]['full_name']}',
            ]

        for col_idx, value in enumerate(fila, start=1):
            sheet.cell(row=idx, column=col_idx, value=value)


    return workbook