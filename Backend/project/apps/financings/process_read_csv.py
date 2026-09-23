import pandas as pd
from apps.financings.models import Banco
from datetime import datetime, timedelta
import csv
import os
import pandas as pd
from apps.actividades.utils import log_user_action, log_system_event
import traceback


def process(nuevo, sucursal):
    print(f'Leyendo el archivo {nuevo} de sucursal: {sucursal}')
    
    registros_creados = 0
    registros_omitidos = 0

    try:
        # Leer el archivo CSV
        df = pd.read_csv(nuevo, encoding='utf-8', on_bad_lines='skip')  # Usa 'latin1' si es necesario

        # Filtrar las columnas necesarias
        df_filtered = df[['Fecha', 'Descripción', 'Referencia', 'Secuencial', 'Cheque Propio / Local / Efectivo', 'Débito (-)', 'Crédito (+)', 'Saldo Contable', 'Saldo Disponible']].copy()

        # Convertir las columnas numéricas usando .loc[]
        df_filtered.loc[:, 'Crédito (+)'] = pd.to_numeric(df_filtered['Crédito (+)'], errors='coerce')
        df_filtered.loc[:, 'Débito (-)'] = pd.to_numeric(df_filtered['Débito (-)'], errors='coerce')
        df_filtered.loc[:, 'Saldo Contable'] = pd.to_numeric(df_filtered['Saldo Contable'], errors='coerce')
        df_filtered.loc[:, 'Saldo Disponible'] = pd.to_numeric(df_filtered['Saldo Disponible'], errors='coerce')

        # Recorrer las filas del DataFrame
        for index, row in df_filtered.iterrows():
            # Acceder a los valores de cada fila
            fecha = datetime.strptime(row['Fecha'], '%d/%m/%Y')
            referencia = str(row['Referencia'])
            secuencial = str(row['Secuencial'])
            cheque = str(row['Cheque Propio / Local / Efectivo'])

            if '.' in referencia:
                referencia = referencia.split('.')[0]

            if '.' in secuencial:
                secuencial = secuencial.split('.')[0]

            credito = row['Crédito (+)']
            debito = row['Débito (-)']
            descripcion = row['Descripción']
            saldo_contable = row['Saldo Contable']
            saldo_disponible = row['Saldo Disponible']

            # Verificar si la referencia ya existe en la base de datos
            if Banco.objects.filter(referencia=referencia).exists():
                print(f"La referencia {referencia} ya existe. Ignorando...")
                registros_omitidos += 1
                continue  # Si ya existe, saltar este registro
            
            banco = Banco(
                fecha=fecha, 
                referencia=referencia, 
                credito=credito, 
                debito=debito, 
                descripcion=descripcion, 
                secuencial=secuencial, 
                cheque=cheque, 
                saldo_contable=saldo_contable, 
                saldo_disponible=saldo_disponible, 
                sucursal=sucursal, 
                nombre_del_banco='BANRURAL'
            )
            banco.save()
            
            registros_creados += 1
            print(f"Fecha: {fecha}, Referencia: {referencia}, Crédito: {credito}, Débito: {debito}, Descripción: {descripcion}")

        # Registro exitoso al finalizar el procesamiento
        log_system_event(
            message=f"Proceso de Banrural completado exitosamente para la sucursal {sucursal}.",
            level_name="INFO",
            source="Banrural",
            category_name="Finanzas",
            metadata={
                "archivo": nuevo,
                "sucursal": str(sucursal),
                "registros_creados": registros_creados,
                "registros_omitidos": registros_omitidos
            }
        )

    except Exception as e:
        # Captura de error inesperado con traceback
        error_msg = f"Error al procesar el archivo de Banrural para la sucursal {sucursal}: {str(e)}"
        print(error_msg)
        
        log_system_event(
            message=error_msg,
            level_name="ERROR",
            source="Banrural",
            category_name="Finanzas",
            traceback=traceback.format_exc(),
            metadata={
                "archivo": nuevo,
                "sucursal": str(sucursal)
            }
        )

import pandas as np


import os
from datetime import datetime
import pandas as pd
import traceback
from apps.financings.models import Banco
from apps.actividades.utils import log_system_event

def process_banco_industrial(nuevo, sucursal):
    print(f'Leyendo el archivo {nuevo} de sucursal: {sucursal}')
    
    # 1. Validar si el archivo procesado realmente fue creado
    if not os.path.exists(nuevo):
        error_msg = f"El archivo procesado no fue creado. Es muy probable que el archivo subido no sea el formato correcto de Banco Industrial."
        print(error_msg)
        
        log_system_event(
            message=error_msg,
            level_name="WARNING",
            source="Banco Industrial",
            category_name="Finanzas",
            metadata={
                "archivo": nuevo,
                "sucursal": str(sucursal)
            }
        )
        return  # Interrumpe la ejecución de forma segura sin lanzar FileNotFoundError

    registros_creados = 0
    registros_omitidos = 0

    try:
        # Leer el archivo CSV generado anteriormente
        df = pd.read_csv(nuevo, encoding='utf-8', on_bad_lines='skip')

        # Filtrar las columnas correspondientes a Banco Industrial
        df_filtered = df[['Fecha', 'TT', 'Descripción', 'No. Doc', 'Debe (GTQ)', 'Haber (GTQ)', 'Saldo (GTQ)']].copy()

        # Convertir las columnas numéricas
        df_filtered.loc[:, 'Debe (GTQ)'] = pd.to_numeric(df_filtered['Debe (GTQ)'], errors='coerce').fillna(0)
        df_filtered.loc[:, 'Haber (GTQ)'] = pd.to_numeric(df_filtered['Haber (GTQ)'], errors='coerce').fillna(0)
        df_filtered.loc[:, 'Saldo (GTQ)'] = pd.to_numeric(df_filtered['Saldo (GTQ)'], errors='coerce').fillna(0)

        # Recorrer las filas del DataFrame
        for index, row in df_filtered.iterrows():
            fecha = datetime.strptime(row['Fecha'], '%d-%m-%Y')
            
            referencia = str(row['No. Doc']).strip()
            if '.' in referencia:
                referencia = referencia.split('.')[0]

            debito = row['Debe (GTQ)']
            credito = row['Haber (GTQ)']
            descripcion = row['Descripción']
            saldo = row['Saldo (GTQ)']
            
            tipo_transaccion = str(row['TT']).strip() if pd.notna(row['TT']) else ''

            if Banco.objects.filter(referencia=referencia).exists():
                print(f"La referencia {referencia} ya existe. Ignorando...")
                registros_omitidos += 1
                continue

            Banco.objects.create(
                fecha=fecha,
                referencia=referencia,
                credito=credito,
                debito=debito,
                descripcion=descripcion,
                secuencial='',
                cheque=tipo_transaccion,
                saldo_contable=saldo,
                saldo_disponible=saldo,
                sucursal=sucursal,
                nombre_del_banco='BANCO INDUSTRIAL'
            )
            
            registros_creados += 1

        log_system_event(
            message=f"Proceso de Banco Industrial completado exitosamente para la sucursal {sucursal}.",
            level_name="INFO",
            source="Banco Industrial",
            category_name="Finanzas",
            metadata={
                "archivo": nuevo,
                "sucursal": str(sucursal),
                "registros_creados": registros_creados,
                "registros_omitidos": registros_omitidos
            }
        )

    except Exception as e:
        error_msg = f"Error al procesar el archivo de Banco Industrial para la sucursal {sucursal}: {str(e)}"
        print(error_msg)
        
        log_system_event(
            message=error_msg,
            level_name="ERROR",
            source="Banco Industrial",
            category_name="Finanzas",
            traceback=traceback.format_exc(),
            metadata={
                "archivo": nuevo,
                "sucursal": str(sucursal)
            }
        )

