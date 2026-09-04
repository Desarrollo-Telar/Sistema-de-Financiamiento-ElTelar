import pandas as pd
from apps.financings.models import Banco
from datetime import datetime, timedelta
import csv
import os
import pandas as pd

def process(nuevo, sucursal):
    # Leer el archivo CSV
    #nuevo = f'/code/{nuevo}'
    df = pd.read_csv(nuevo, encoding='utf-8', on_bad_lines='skip')  # Usa 'latin1' si es necesario

    #print("Columnas del archivo CSV:", df)

    # Filtrar las columnas 'Fecha', 'Referencia' y 'Crédito (+)'
    df_filtered = df[['Fecha', 'Descripción','Referencia','Secuencial','Cheque Propio / Local / Efectivo' ,'Débito (-)', 'Crédito (+)','Saldo Contable','Saldo Disponible']].copy()  # Asegúrate de hacer una copia explícita


    # Convertir la columna 'Crédito (+)' a numérica, en caso de que no lo sea
    # Convertir las columnas 'Crédito (+)' y 'Débito (-)' a numéricas usando .loc[]
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
        saldo_disponible = row ['Saldo Disponible']

        # Verificar si la referencia ya existe en la base de datos
        if Banco.objects.filter(referencia=referencia).exists():
            print(f"La referencia {referencia} ya existe. Ignorando...")
            continue  # Si ya existe, saltar este registro
        
        banco = Banco(fecha=fecha,referencia=referencia,credito=credito, debito=debito, descripcion=descripcion, 
                      secuencial=secuencial, cheque=cheque, saldo_contable=saldo_contable, saldo_disponible=saldo_disponible, sucursal=sucursal, nombre_del_banco='BANRURAL')
        banco.save()
        
        # Realizar alguna acción con los datos
        print(f"Fecha: {fecha}, Referencia: {referencia}, Crédito: {credito}, Débito: {debito}, Descripción: {descripcion}")



import pandas as np

def process_banco_industrial(nuevo, sucursal):
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
        # Parsear fecha según formato de BI ('DD-MM-YYYY')
        fecha = datetime.strptime(row['Fecha'], '%d-%m-%Y')
        
        # 'No. Doc' actúa como el número de referencia
        referencia = str(row['No. Doc']).strip()
        if '.' in referencia:
            referencia = referencia.split('.')[0]

        debito = row['Debe (GTQ)']
        credito = row['Haber (GTQ)']
        descripcion = row['Descripción']
        saldo = row['Saldo (GTQ)']
        
        # Opcional: Tipo de transacción (NC, ND, DE, CQ, etc.)
        tipo_transaccion = str(row['TT']).strip() if pd.notna(row['TT']) else ''

        # Verificar si la referencia ya existe en la base de datos
        if Banco.objects.filter(referencia=referencia).exists():
            print(f"La referencia {referencia} ya existe. Ignorando...")
            continue  # Si ya existe, saltar este registro

        # Crear el objeto Banco
        banco = Banco(
            fecha=fecha,
            referencia=referencia,
            credito=credito,
            debito=debito,
            descripcion=descripcion,
            secuencial='',                 # No existe en BI
            cheque=tipo_transaccion,       # Se asigna TT (NC, ND, etc.) o deja en blanco
            saldo_contable=saldo,
            saldo_disponible=saldo,
            sucursal=sucursal,
            nombre_del_banco='BANCO INDUSTRIAL'
        )
        banco.save()

        print(f"Guardado - Fecha: {fecha.strftime('%Y-%m-%d')}, Referencia: {referencia}, Crédito: {credito}, Débito: {debito}, Descripción: {descripcion}")