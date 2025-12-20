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
from .funcion import safe_list_get

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
            cuota = credito.get('cuota_vigente')
            fecha_limite = formater_fecha(cuota.get('fecha_limite')) if cuota else ''
            numero_referencia = cuota.get('numero_referencia') if cuota else ''

            fila = [
                str(contador),
                f"{credito.get('credito', {}).get('creation_date', '')}",
                f"{credito.get('credito', {}).get('codigo_credito', '')}",
                f"{get_cliente(credito.get('credito', {}).get('customer_id_id', ''))}",
                f"{formatear_numero(credito.get('credito', {}).get('monto', 0))}",
                f"{credito.get('credito', {}).get('plazo', '')}",
                f"{credito.get('credito', {}).get('tasa_interes', 0) * 100}%",
                f"{credito.get('credito', {}).get('forma_de_pago', '')}",
                f"{credito.get('credito', {}).get('tipo_credito', '')}",

                # Desembolsos - manejo seguro de lista
                f"{credito.get('desembolsos', [{}])[0].get('forma_desembolso', '')}",
                f"{credito.get('credito', {}).get('fecha_inicio', '')}",
                f"{credito.get('credito', {}).get('fecha_vencimiento', '')}",

                f"{fecha_limite}",

                f"{formatear_numero(credito.get('credito', {}).get('saldo_actual', 0))}",
                f"{formatear_numero(credito.get('credito', {}).get('saldo_pendiente', 0))}",
                f"{formatear_numero(credito.get('credito', {}).get('excedente', 0))}",
                f"{credito.get('credito', {}).get('fecha_vencimiento', '')}",

                f"{stat}",

                f"{numero_referencia}",
                f"{get_asesor_credito(credito.get('credito', {}).get('asesor_de_credito_id', ''))}",

            ]

            for col_idx, value in enumerate(fila, start=1):
                sheet.cell(row=idx, column=col_idx, value=value)


    return workbook