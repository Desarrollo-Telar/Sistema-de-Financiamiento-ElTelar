from celery import shared_task
import time
import os

from apps.financings.read_csv import read, read_txt_movements
from .models import DocumentBank
# Ejemplo de tarea asíncrona
@shared_task
def tarea_larga_duracion():
    time.sleep(10)  # Simula una tarea larga, que toma 10 segundos
    return 'La tarea ha terminado'

@shared_task
def leer_documento(file, id):
    try:
        # Obtener la extensión del archivo
        extension = os.path.splitext(file)[1].lower()
        print(extension)

        # Dependiendo del tipo de archivo, llamar a la función correspondiente
        if extension == '.csv':
            read(file)  # Llama a tu función original para archivos CSV
        elif extension == '.txt':
            print('FORMATO .TXT')
            read_txt_movements(file)  # Llama a la nueva función para archivos TXT
        else:
            return f"Error: Tipo de archivo '{extension}' no soportado."

        # Eliminar el documento de la base de datos después de procesarlo
        delete_b = DocumentBank.objects.get(id=id)
        delete_b.delete()

        return 'Documento leído correctamente'

    except Exception as e:
        return f'Error al leer el documento: {str(e)}'
