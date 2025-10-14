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
        
        banco = Banco(fecha=fecha,referencia=referencia,credito=credito, debito=debito, descripcion=descripcion, secuencial=secuencial, cheque=cheque, saldo_contable=saldo_contable, saldo_disponible=saldo_disponible, sucursal=sucursal)
        banco.save()
        
        # Realizar alguna acción con los datos
        print(f"Fecha: {fecha}, Referencia: {referencia}, Crédito: {credito}, Débito: {debito}, Descripción: {descripcion}")
