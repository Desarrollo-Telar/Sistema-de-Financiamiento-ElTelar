import pandas as pd
from apps.financings.models import Banco
from datetime import datetime, timedelta
import csv
import os
import pandas as pd
def process(nuevo):
    # Leer el archivo CSV
    #nuevo = f'/code/{nuevo}'
    df = pd.read_csv(nuevo, encoding='utf-8', on_bad_lines='skip')  # Usa 'latin1' si es necesario

    #print("Columnas del archivo CSV:", df)

    # Filtrar las columnas 'Fecha', 'Referencia' y 'Crédito (+)'
    df_filtered = df[['Fecha', 'Descripción','Referencia', 'Débito (-)', 'Crédito (+)']].copy()  # Asegúrate de hacer una copia explícita


    # Convertir la columna 'Crédito (+)' a numérica, en caso de que no lo sea
    # Convertir las columnas 'Crédito (+)' y 'Débito (-)' a numéricas usando .loc[]
    df_filtered.loc[:, 'Crédito (+)'] = pd.to_numeric(df_filtered['Crédito (+)'], errors='coerce')
    df_filtered.loc[:, 'Débito (-)'] = pd.to_numeric(df_filtered['Débito (-)'], errors='coerce')

    # Recorrer las filas del DataFrame
    for index, row in df_filtered.iterrows():
        # Acceder a los valores de cada fila
        fecha = datetime.strptime(row['Fecha'], '%d/%m/%Y')
        referencia = str(row['Referencia'])

        if '.' in referencia:
            referencia = referencia.split('.')[0]
        credito = row['Crédito (+)']
        debito = row['Débito (-)']
        descripcion = row['Descripción']
        # Verificar si la referencia ya existe en la base de datos
        if Banco.objects.filter(referencia=referencia).exists():
            print(f"La referencia {referencia} ya existe. Ignorando...")
            continue  # Si ya existe, saltar este registro
        
        banco = Banco(fecha=fecha,referencia=referencia,credito=credito, debito=debito, descripcion=descripcion)
        banco.save()
        
        # Realizar alguna acción con los datos
        print(f"Fecha: {fecha}, Referencia: {referencia}, Crédito: {credito}, Débito: {debito}, Descripción: {descripcion}")
