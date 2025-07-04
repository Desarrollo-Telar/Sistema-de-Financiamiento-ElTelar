import csv
import os
import pandas as pd


    

file_path = 'apps/financings/clases/Movs_XXXXXXXXXX8868_Últimos5Movimientos.csv'
nuevo = 'apps/financings/clases/buenoo.csv'

# Elimina el archivo si ya existe antes de empezar a escribir
if os.path.exists(nuevo):
    os.remove(nuevo)


# Función para crear un archivo nuevo y escribir en él
def crear_archivo_nuevo(info):
    with open(nuevo, 'a', newline='') as archivo:
        writer = csv.writer(archivo)
        writer.writerow(info)



# Lee el archivo CSV original y escribe el nuevo archivo filtrado
with open(file_path, newline='') as csvfile:
    file = csv.reader(csvfile, delimiter=',')

    # Variable para activar la captura de los movimientos cuando se encuentra el encabezado
    capture_data = False

    for row in file:
        # Detecta el encabezado para comenzar a capturar los datos relevantes
        if row == ['Fecha', 'Oficina', 'Descripciï¿½n', 'Referencia', 'Secuencial', 'Cheque Propio / Local / Efectivo', 'Dï¿½bito (-)', 'Crï¿½dito (+)', 'Saldo Contable', 'Saldo Disponible']:
            capture_data = True
            #print(row)
            crear_archivo_nuevo(row)  # Escribe el encabezado
            continue

        # Si ya estamos capturando datos, guarda las filas no vacías que siguen al encabezado
        if capture_data and row:
            if row != ['Confidencial']:  # Evita filas con "Confidencial"
                crear_archivo_nuevo(row)
                #print(row)



import pandas as pd
# Leer el archivo CSV
df = pd.read_csv(nuevo, encoding='latin1')  # Usa 'latin1' si es necesario

# Corregir el nombre de la columna con caracteres extraños (si es necesario)
df.columns = df.columns.str.replace('ï¿½', 'é')

# Filtrar las columnas 'Fecha', 'Referencia' y 'Crédito (+)'
df_filtered = df[['Fecha', 'Referencia', 'Crédito (+)']]

# Convertir la columna 'Crédito (+)' a numérica, en caso de que no lo sea
df_filtered['Crédito (+)'] = pd.to_numeric(df_filtered['Crédito (+)'], errors='coerce')

# Recorrer las filas del DataFrame
for index, row in df_filtered.iterrows():
    # Acceder a los valores de cada fila
    fecha = row['Fecha']
    referencia = row['Referencia']
    credito = row['Crédito (+)']
    
    # Realizar alguna acción con los datos
    print(f"Fecha: {fecha}, Referencia: {referencia}, Crédito: {credito}")




print('Fin de programa')