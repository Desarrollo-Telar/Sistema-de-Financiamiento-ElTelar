import csv
import os
import pandas as pd

from .process_read_csv import process
def read(file_path):
    
    nuevo = 'apps/financings/clases/buenoo.csv'
    # Elimina el archivo si ya existe antes de empezar a escribir
    if os.path.exists(nuevo):
        
        os.remove(nuevo)

    

    # Función para crear un archivo nuevo y escribir en él
    def crear_archivo_nuevo(info):
        print('creando archivo nuevo')
        with open(nuevo, 'a', newline='') as archivo:
            writer = csv.writer(archivo)
            writer.writerow(info)
            
    if os.path.exists(file_path):
        # Lee el archivo CSV original y escribe el nuevo archivo filtrado
        with open(file_path, newline='',encoding='latin1') as csvfile:
            file = csv.reader(csvfile, delimiter=',')

            # Variable para activar la captura de los movimientos cuando se encuentra el encabezado
            capture_data = False

            for row in file:         
                
                
                # Detecta el encabezado para comenzar a capturar los datos relevantes
                if row == ['Fecha', 'Oficina', 'Descripción', 'Referencia', 'Secuencial', 'Cheque Propio / Local / Efectivo', 'Débito (-)', 'Crédito (+)', 'Saldo Contable', 'Saldo Disponible']:
                    capture_data = True
                    #print(row)
                    crear_archivo_nuevo(row)  # Escribe el encabezado
                    continue

                # Si ya estamos capturando datos, guarda las filas no vacías que siguen al encabezado
                if capture_data and row:
                    if row != ['Confidencial']:  # Evita filas con "Confidencial"
                        crear_archivo_nuevo(row)
                        #print(row)
                    
        process(nuevo)