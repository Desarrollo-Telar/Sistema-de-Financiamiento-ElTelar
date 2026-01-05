from datetime import datetime
from dateutil.relativedelta import relativedelta

def formater_fecha(fecha_completa):
    fecha_dt = datetime.fromisoformat(fecha_completa.replace("Z", "+00:00"))

    return fecha_dt.date()
    
def creditos_creado_ese_dia(data, dia=None):
    lista_nuevos = []

    if dia is None:
        dia = datetime.now().date()
    
    # Restar un día
    dia = dia - relativedelta(days=1)

    if data is None:
        return lista_nuevos
   

    for dato in data:
        fecha_completa = dato['informacion_seguro']['creation_date']
        fecha_dt = datetime.fromisoformat(fecha_completa.replace("Z", "+00:00"))

        if fecha_dt.date() == dia:
            lista_nuevos.append(dato)

    return lista_nuevos

def creditos_cancelados(data):
    lista_cancelados = []
    if data is None:
        return lista_cancelados

    for dato in data:

        if dato['informacion_seguro']['is_paid_off']:
            lista_cancelados.append(dato)

    return lista_cancelados

def creditos_en_atraso(data):
    lista = []

    if data is None:
        return lista

    for dato in data:
        if not dato['informacion_seguro']['estados_fechas']:
            lista.append(dato)
    return lista

def creditos_falta_aportacion(data):
    lista = []

    if data is None:
        return lista
    

    for dato in data:
        if not dato['informacion_seguro']['estado_aportacion']:
            lista.append(dato)

    return lista

def creditos_con_excedentes(data):
    lista = []

    if data is None:
        return lista

    for dato in data:
        if dato['informacion_seguro']['excedente'] > 0:
            lista.append(dato)
            
    return lista

