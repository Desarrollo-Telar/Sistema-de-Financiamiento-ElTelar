import csv
import os
import pandas as pd

from .process_read_csv import process, process_banco_industrial






def read(file_path, sucursal):
    
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
                    
        process(nuevo, sucursal)

def read_banco_industrial(file_path, sucursal):
    nuevo = 'apps/financings/clases/buenoo_industrial.csv'

    # Elimina el archivo si ya existe antes de empezar a escribir
    if os.path.exists(nuevo):
        os.remove(nuevo)

    # Función para crear un archivo nuevo y escribir en él
    def crear_archivo_nuevo(info):
        os.makedirs(os.path.dirname(nuevo), exist_ok=True)
        print('creando archivo nuevo')
        with open(nuevo, 'a', newline='', encoding='utf-8') as archivo:
            writer = csv.writer(archivo)
            writer.writerow(info)
            
    if os.path.exists(file_path):
        with open(file_path, newline='', encoding='latin1') as csvfile:
            file = csv.reader(csvfile, delimiter=',')

            capture_data = False
            tiene_saldo = False

            for row in file:        
                # Detecta las primeras 6 columnas obligatorias de Banco Industrial
                if row and row[:6] == ['Fecha', 'TT', 'Descripción', 'No. Doc', 'Debe (GTQ)', 'Haber (GTQ)']:
                    capture_data = True
                    # Verifica si la descarga incluye la columna 'Saldo (GTQ)'
                    tiene_saldo = (len(row) >= 7 and row[6] == 'Saldo (GTQ)')
                    
                    # Genera el encabezado estandarizado de 7 columnas
                    crear_archivo_nuevo(['Fecha', 'TT', 'Descripción', 'No. Doc', 'Debe (GTQ)', 'Haber (GTQ)', 'Saldo (GTQ)'])
                    continue

                # Captura las filas de datos
                if capture_data and row and any(field.strip() for field in row):
                    if tiene_saldo:
                        # Estructura de 7 columnas (o más por comas en descripción)
                        fecha = row[0]
                        tt = row[1]
                        no_doc = row[-4]
                        debe = row[-3]
                        haber = row[-2]
                        saldo = row[-1]
                        descripcion = ",".join(row[2:-4])
                    else:
                        # Estructura de 6 columnas (sin Saldo)
                        fecha = row[0]
                        tt = row[1]
                        no_doc = row[-3]
                        debe = row[-2]
                        haber = row[-1]
                        saldo = '0.0'  # Valor por defecto
                        descripcion = ",".join(row[2:-3])

                    row_normalizado = [fecha, tt, descripcion, no_doc, debe, haber, saldo]
                    crear_archivo_nuevo(row_normalizado)
                    
        if capture_data:
            process_banco_industrial(nuevo, sucursal)
        else:
            print("El archivo proporcionado no contiene el formato/encabezado válido de Banco Industrial.")
            
import re
from datetime import datetime



def read_txt_movements(file_path, sucursal):
    nuevo = 'apps/financings/clases/buenoo.csv'

    # Elimina el archivo si ya existe
    if os.path.exists(nuevo):
        os.remove(nuevo)

    # Función para crear el archivo nuevo
    def crear_archivo_nuevo(info):
        with open(nuevo, 'a', newline='') as archivo:
            print('creando archivo')
            writer = csv.writer(archivo)
            writer.writerow(info)

    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='latin1') as txtfile:
            capture_data = False

            for line in txtfile:
                line = line.strip()

                # Saltar líneas vacías
                if not line:
                    continue

                # Detectar encabezado
                if line.startswith("Fecha\tOficina\tDescripción"):
                    capture_data = True
                    encabezado = [
                        'Fecha', 'Oficina', 'Descripción', 'Referencia', 'Secuencial',
                        'Cheque Propio / Local / Efectivo', 'Débito (-)', 'Crédito (+)',
                        'Saldo Contable', 'Saldo Disponible'
                    ]
                    crear_archivo_nuevo(encabezado)
                    continue

                # Procesar solo cuando estamos en la sección de datos
                if capture_data:
                    if line == "Confidencial":
                        continue  # Saltar esta fila

                    # Separar por tabulaciones
                    row = line.split('\t')

                    # Validar que tenga exactamente 10 columnas
                    if len(row) == 10:
                        crear_archivo_nuevo(row)

        # Procesar el archivo limpio
        process(nuevo,sucursal)


    
    
# Función adicional para procesar el CSV generado (similar a tu función process)
def process_csv(csv_file_path):
    """
    Procesa el archivo CSV generado para análisis adicional
    
    Args:
        csv_file_path (str): Ruta del archivo CSV a procesar
    """
    try:
        movements = []
        
        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            
            # Leer encabezados
            headers = next(reader)
            
            # Procesar cada movimiento
            for row in reader:
                if len(row) >= 10:  # Asegurar que tenga todas las columnas
                    movement = {
                        'fecha': row[0],
                        'oficina': row[1],
                        'descripcion': row[2],
                        'referencia': row[3],
                        'secuencial': row[4],
                        'tipo_pago': row[5],
                        'debito': float(row[6]) if row[6] else 0.0,
                        'credito': float(row[7]) if row[7] else 0.0,
                        'saldo_contable': float(row[8]) if row[8] else 0.0,
                        'saldo_disponible': float(row[9]) if row[9] else 0.0
                    }
                    movements.append(movement)
        
        # Aquí puedes agregar más lógica de procesamiento
        print(f"Se procesaron {len(movements)} movimientos")
        return movements
        
    except Exception as e:
        print(f"Error en process_csv: {str(e)}")
        return []

