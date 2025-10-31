# Reporte Excel
from openpyxl import Workbook
from django.http import HttpResponse
import json
import io
import zipfile

# Tiempo
from datetime import datetime, timedelta

# Modelo
from apps.customers.models import Customer, CreditCounselor
from apps.financings.formato import formatear_numero

# Filtros
from .filtros.creditos import *

def get_cliente(id):
    cliente =  Customer.objects.filter(id=id).first()

    return cliente if cliente else None

def get_asesor_credito(id):
    asesor = CreditCounselor.objects.filter(id=id).first()
    return asesor if asesor else None

def crear_excel_creditos(datos, dia = None):
    if dia is None:
        dia = datetime.now().date()

    workbook = Workbook()
    workbook.remove(workbook.active)

    
    

    filtros = {
        'Creditos Nuevos': creditos_creado_ese_dia(datos,dia),
        'Todos Los Creditos': datos,
        'Creditos Cancelados': creditos_cancelados(datos),
        'Creditos Estado Juridico':creditos_estado_juridico(datos),
        'Creditos con Excedente':creditos_con_excedentes(datos),
        'Creditos en Atraso':creditos_en_atraso(datos),
        'Creditos con falta de Aportacion':creditos_falta_aportacion(datos),
    }

    # Agregar encabezado    
    encabezados = [
        "#", "FECHA DE REGISTRO", "CODIGO DEL CREDITO", 
        "CLIENTE", "MONTO OTORGADO", "PROPOSITO", "PLAZO EN MESES", "TASA DE INTERES",
        "FORMA DE PAGO", "TIPO DE CREDITO", "DESEMBOLSO","FECHA DE INICIO DEL CREDITO", 
        "FECHA DE VENCIMIENTO DEL CREDITO", "FECHA LIMITE DE PAGO", 
        "SALDO ACTUAL", "SALDO CAPITAL PENDIENTE","SALDO EXCEDENTE" ,"STATUS DEL CREDITO", "NUMERO DE REFERENCIA", "ASESOR DE CREDITO"
    ]

    for filtro,data in filtros.items():
        sheet = workbook.create_sheet(title=filtro[:31])

        for col_idx, header in enumerate(encabezados, start=1):
            sheet.cell(row=1, column=col_idx, value=header)

        # Agregar los datos
        contador = 0
        for idx, credito in enumerate(data, start=2):
            contador+=1

            # Mensajes de estado
            if credito['credito']['estado_aportacion']:
                mensaje = 'VIGENTE'
            elif credito['credito']['estado_aportacion'] is None:
                mensaje = 'SIN APORTACIONES'
            else:
                mensaje = 'EN ATRASO'

            aportacion = mensaje
            s_fecha = 'VIGENTE' if credito['credito']['estados_fechas'] else 'EN ATRASO'
            stat = f'''Status de Aportación: {aportacion}, Status por Fecha: {s_fecha}'''

            fila = [
                str(contador),
                f'{credito['credito']['creation_date']}',
                f'{credito['credito']['codigo_credito']}',
                f'{get_cliente(credito['credito']['customer_id'])}',
                f'{formatear_numero(credito['credito']['monto'])}',
                f'{credito['credito']['plazo']}',
                f'{credito['credito']['tasa_interes']*100}%',
                f'{credito['credito']['forma_de_pago']}',
                f'{credito['credito']['tipo_credito']}',
                                
                f'{credito['desembolsos'][0]['forma_desembolso']}',
                f'{credito['credito']['fecha_inicio']}',
                f'{credito['credito']['fecha_vencimiento']}',

                f'{formater_fecha(credito['cuota_vigente']['fecha_limite'])}',

                f'{formatear_numero(credito['credito']['saldo_actual'])}',
                f'{formatear_numero(credito['credito']['saldo_pendiente'])}',
                f'{formatear_numero(credito['credito']['excedente'])}',
                f'{credito['credito']['fecha_vencimiento']}',

                f'{stat}',

                f'{credito['cuota_vigente']['numero_referencia']}',
                f'{get_asesor_credito(credito['credito']['asesor_de_credito'])}',

            ]

            for col_idx, value in enumerate(fila, start=1):
                sheet.cell(row=idx, column=col_idx, value=value)


    return workbook