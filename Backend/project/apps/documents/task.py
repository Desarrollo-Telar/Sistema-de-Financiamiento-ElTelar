from celery import shared_task
import time

from apps.financings.read_csv import read
from .models import DocumentBank
# Ejemplo de tarea asíncrona
@shared_task
def tarea_larga_duracion():
    time.sleep(10)  # Simula una tarea larga, que toma 10 segundos
    return 'La tarea ha terminado'

@shared_task
def leer_documento(file,id):
    try:
        read(file)
        delete_b = DocumentBank.objects.get(id=id)
        delete_b.delete()
        
        return 'Documento leído correctamente'
    except Exception as e:
        return f'Error al leer el documento: {str(e)}'
