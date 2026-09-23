import csv
import os
import re
import traceback
from datetime import datetime
import pandas as pd

from .process_read_csv import process, process_banco_industrial
from apps.actividades.utils import log_system_event


def read(file_path, sucursal):
    nuevo = 'apps/financings/clases/buenoo.csv'

    try:
        # Asegura la existencia del directorio donde se guardará el archivo procesado
        os.makedirs(os.path.dirname(nuevo), exist_ok=True)

        # Elimina el archivo si ya existe antes de empezar a escribir
        if os.path.exists(nuevo):
            os.remove(nuevo)

        # Función para crear un archivo nuevo y escribir en él
        def crear_archivo_nuevo(info):
            print('creando archivo nuevo')
            with open(nuevo, 'a', newline='', encoding='utf-8') as archivo:
                writer = csv.writer(archivo)
                writer.writerow(info)

        if not os.path.exists(file_path):
            error_msg = f"El archivo de origen no existe: {file_path}"
            print(error_msg)
            log_system_event(
                message=error_msg,
                level_name="WARNING",
                source="Lectura Banrural",
                category_name="Finanzas",
                metadata={"file_path": file_path, "sucursal": str(sucursal)}
            )
            return

        capture_data = False

        # Lee el archivo CSV original y escribe el nuevo archivo filtrado
        with open(file_path, newline='', encoding='latin1') as csvfile:
            file = csv.reader(csvfile, delimiter=',')

            for row in file:
                # Detecta el encabezado para comenzar a capturar los datos relevantes
                if row == ['Fecha', 'Oficina', 'Descripción', 'Referencia', 'Secuencial', 'Cheque Propio / Local / Efectivo', 'Débito (-)', 'Crédito (+)', 'Saldo Contable', 'Saldo Disponible']:
                    capture_data = True
                    crear_archivo_nuevo(row)  # Escribe el encabezado
                    continue

                # Si ya estamos capturando datos, guarda las filas no vacías
                if capture_data and row:
                    if row != ['Confidencial']:  # Evita filas con "Confidencial"
                        crear_archivo_nuevo(row)

        if capture_data:
            process(nuevo, sucursal)
        else:
            msg = f"El archivo subido no contiene el encabezado válido de Banrural."
            print(msg)
            log_system_event(
                message=msg,
                level_name="WARNING",
                source="Lectura Banrural",
                category_name="Finanzas",
                metadata={"file_path": file_path, "sucursal": str(sucursal)}
            )

    except Exception as e:
        error_msg = f"Error al leer/procesar archivo Banrural: {str(e)}"
        print(error_msg)
        log_system_event(
            message=error_msg,
            level_name="ERROR",
            source="Lectura Banrural",
            category_name="Finanzas",
            traceback=traceback.format_exc(),
            metadata={"file_path": file_path, "sucursal": str(sucursal)}
        )


def read_banco_industrial(file_path, sucursal):
    nuevo = 'apps/financings/clases/buenoo_industrial.csv'

    try:
        # Asegura la existencia del directorio donde se guardará el archivo procesado
        os.makedirs(os.path.dirname(nuevo), exist_ok=True)

        if os.path.exists(nuevo):
            os.remove(nuevo)

        def crear_archivo_nuevo(info):
            print('creando archivo nuevo')
            with open(nuevo, 'a', newline='', encoding='utf-8') as archivo:
                writer = csv.writer(archivo)
                writer.writerow(info)

        if not os.path.exists(file_path):
            error_msg = f"El archivo de origen no existe: {file_path}"
            print(error_msg)
            log_system_event(
                message=error_msg,
                level_name="WARNING",
                source="Lectura BI",
                category_name="Finanzas",
                metadata={"file_path": file_path, "sucursal": str(sucursal)}
            )
            return

        capture_data = False
        tiene_saldo = False

        with open(file_path, newline='', encoding='latin1') as csvfile:
            file = csv.reader(csvfile, delimiter=',')

            for row in file:
                # Soporta archivos de Banco Industrial con o sin columna 'Saldo (GTQ)'
                if row and row[:6] == ['Fecha', 'TT', 'Descripción', 'No. Doc', 'Debe (GTQ)', 'Haber (GTQ)']:
                    capture_data = True
                    tiene_saldo = (len(row) >= 7 and row[6] == 'Saldo (GTQ)')
                    crear_archivo_nuevo(['Fecha', 'TT', 'Descripción', 'No. Doc', 'Debe (GTQ)', 'Haber (GTQ)', 'Saldo (GTQ)'])
                    continue

                if capture_data and row and any(field.strip() for field in row):
                    if tiene_saldo:
                        fecha = row[0]
                        tt = row[1]
                        no_doc = row[-4]
                        debe = row[-3]
                        haber = row[-2]
                        saldo = row[-1]
                        descripcion = ",".join(row[2:-4])
                    else:
                        fecha = row[0]
                        tt = row[1]
                        no_doc = row[-3]
                        debe = row[-2]
                        haber = row[-1]
                        saldo = '0.0'
                        descripcion = ",".join(row[2:-3])

                    row_normalizado = [fecha, tt, descripcion, no_doc, debe, haber, saldo]
                    crear_archivo_nuevo(row_normalizado)

        if capture_data:
            process_banco_industrial(nuevo, sucursal)
        else:
            msg = "El archivo proporcionado no contiene el formato/encabezado válido de Banco Industrial."
            print(msg)
            log_system_event(
                message=msg,
                level_name="WARNING",
                source="Lectura BI",
                category_name="Finanzas",
                metadata={"file_path": file_path, "sucursal": str(sucursal)}
            )

    except Exception as e:
        error_msg = f"Error al leer/procesar archivo de Banco Industrial: {str(e)}"
        print(error_msg)
        log_system_event(
            message=error_msg,
            level_name="ERROR",
            source="Lectura BI",
            category_name="Finanzas",
            traceback=traceback.format_exc(),
            metadata={"file_path": file_path, "sucursal": str(sucursal)}
        )


def read_txt_movements(file_path, sucursal):
    nuevo = 'apps/financings/clases/buenoo.csv'

    try:
        os.makedirs(os.path.dirname(nuevo), exist_ok=True)

        if os.path.exists(nuevo):
            os.remove(nuevo)

        def crear_archivo_nuevo(info):
            with open(nuevo, 'a', newline='', encoding='utf-8') as archivo:
                print('creando archivo')
                writer = csv.writer(archivo)
                writer.writerow(info)

        if not os.path.exists(file_path):
            error_msg = f"El archivo TXT de origen no existe: {file_path}"
            print(error_msg)
            log_system_event(
                message=error_msg,
                level_name="WARNING",
                source="Lectura TXT Movimientos",
                category_name="Finanzas",
                metadata={"file_path": file_path, "sucursal": str(sucursal)}
            )
            return

        capture_data = False

        with open(file_path, 'r', encoding='latin1') as txtfile:
            for line in txtfile:
                line = line.strip()

                if not line:
                    continue

                if line.startswith("Fecha\tOficina\tDescripción"):
                    capture_data = True
                    encabezado = [
                        'Fecha', 'Oficina', 'Descripción', 'Referencia', 'Secuencial',
                        'Cheque Propio / Local / Efectivo', 'Débito (-)', 'Crédito (+)',
                        'Saldo Contable', 'Saldo Disponible'
                    ]
                    crear_archivo_nuevo(encabezado)
                    continue

                if capture_data:
                    if line == "Confidencial":
                        continue

                    row = line.split('\t')

                    if len(row) == 10:
                        crear_archivo_nuevo(row)

        if capture_data:
            process(nuevo, sucursal)
        else:
            msg = "El archivo TXT no contiene el encabezado esperado."
            print(msg)
            log_system_event(
                message=msg,
                level_name="WARNING",
                source="Lectura TXT Movimientos",
                category_name="Finanzas",
                metadata={"file_path": file_path, "sucursal": str(sucursal)}
            )

    except Exception as e:
        error_msg = f"Error al procesar el archivo TXT de movimientos: {str(e)}"
        print(error_msg)
        log_system_event(
            message=error_msg,
            level_name="ERROR",
            source="Lectura TXT Movimientos",
            category_name="Finanzas",
            traceback=traceback.format_exc(),
            metadata={"file_path": file_path, "sucursal": str(sucursal)}
        )


def process_csv(csv_file_path):
    try:
        movements = []

        if not os.path.exists(csv_file_path):
            error_msg = f"El archivo CSV a analizar no existe: {csv_file_path}"
            print(error_msg)
            log_system_event(
                message=error_msg,
                level_name="WARNING",
                source="Procesamiento CSV",
                category_name="Finanzas",
                metadata={"csv_file_path": csv_file_path}
            )
            return []

        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader, None)

            for row in reader:
                if len(row) >= 10:
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

        print(f"Se procesaron {len(movements)} movimientos")
        return movements

    except Exception as e:
        error_msg = f"Error en process_csv: {str(e)}"
        print(error_msg)
        log_system_event(
            message=error_msg,
            level_name="ERROR",
            source="Procesamiento CSV",
            category_name="Finanzas",
            traceback=traceback.format_exc(),
            metadata={"csv_file_path": csv_file_path}
        )
        return []