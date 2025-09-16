from datetime import date, datetime
from decimal import Decimal
from django.db import models

def model_to_dict(instance, exclude_fields=None):
    """
    Convierte una instancia de modelo Django a diccionario limpio.
    
    :param instance: Objeto de modelo Django
    :param exclude_fields: Lista de campos a excluir (por defecto: _state y password)
    :return: dict con los campos y valores convertidos
    """
    if exclude_fields is None:
        exclude_fields = ['_state', 'password']
    
    data = {}
    
    # Itera sobre todos los campos del modelo
    for field in instance._meta.fields:
        field_name = field.name
        if field_name in exclude_fields:
            continue
        
        value = getattr(instance, field_name)
        
        # Conversión de tipos no serializables
        if isinstance(value, models.Model):
            # Para relaciones OneToOne o ForeignKey, guardamos el PK
            value = value.pk
        elif isinstance(value, Decimal):
            value = float(value)  # O str(value) si necesitas precisión exacta
        elif isinstance(value, (date, datetime)):
            value = value.isoformat()  # Formato 'YYYY-MM-DD' o 'YYYY-MM-DDTHH:MM:SS'
        
        data[field_name] = value
    
    return data

def cambios_realizados(datos_viejos,datos_nuevos ):
    cambios = {}
    for campo, valor_viejo in datos_viejos.items():
        valor_nuevo = datos_nuevos.get(campo)
        if valor_viejo != valor_nuevo:
            cambios[campo] = {
                'antes': valor_viejo,
                'despues': valor_nuevo
            }
    return cambios