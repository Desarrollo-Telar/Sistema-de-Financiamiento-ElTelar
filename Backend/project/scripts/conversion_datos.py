from datetime import date, datetime
from decimal import Decimal
from django.db import models


def model_to_dict(instance, exclude_fields=None):
    """
    Convierte una instancia de modelo Django a un diccionario JSON serializable.
    Incluye manejo seguro para campos FileField/ImageField y optimización de Foreign Keys.
    """
    if exclude_fields is None:
        exclude_fields = ['_state', 'password', 'uuid']
    
    data = {}

    for field in instance._meta.fields:
        field_name = field.name
        if field_name in exclude_fields:
            continue

        #  REEMPLAZO ÓPTIMO PARA FK / OneToOne:
        # Obtiene el ID directamente de memoria (ej. credit_id_id) sin hacer SQL extra
        if field.is_relation and field.many_to_one:
            value = getattr(instance, field.attname)

        #  Si no es relación, obtenemos el valor normal del campo
        else:
            value = getattr(instance, field_name)

            #  Decimales
            if isinstance(value, Decimal):
                value = float(value)

            #  Fechas y datetimes
            elif isinstance(value, (date, datetime)):
                value = value.isoformat()

            #  Archivos o imágenes
            elif isinstance(value, models.fields.files.FieldFile):
                if value and value.name:
                    try:
                        value = value.url
                    except ValueError:
                        value = None
                else:
                    value = None

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