import pandas as pd
from apps.financings.models import Banco
from datetime import datetime, timedelta

def process(nuevo):
    # Leer el archivo CSV
    df = pd.read_csv(nuevo, encoding='utf-8')  # Usa 'latin1' si es necesario

    #print("Columnas del archivo CSV:", df.columns)

    # Filtrar las columnas 'Fecha', 'Referencia' y 'Crédito (+)'
    df_filtered = df[['Fecha', 'Referencia', 'Crédito (+)']]

    # Convertir la columna 'Crédito (+)' a numérica, en caso de que no lo sea
    df_filtered['Crédito (+)'] = pd.to_numeric(df_filtered['Crédito (+)'], errors='coerce')

    # Recorrer las filas del DataFrame
    for index, row in df_filtered.iterrows():
        # Acceder a los valores de cada fila
        fecha = datetime.strptime(row['Fecha'], '%d/%m/%Y')
        referencia = str(row['Referencia'])
        credito = row['Crédito (+)']
        # Verificar si la referencia ya existe en la base de datos
        if Banco.objects.filter(referencia=referencia).exists():
            print(f"La referencia {referencia} ya existe. Ignorando...")
            continue  # Si ya existe, saltar este registro
        
        banco = Banco(fecha=fecha,referencia=referencia,credito=credito)
        banco.save()
        
        # Realizar alguna acción con los datos
        print(f"Fecha: {fecha}, Referencia: {referencia}, Crédito: {credito}")
