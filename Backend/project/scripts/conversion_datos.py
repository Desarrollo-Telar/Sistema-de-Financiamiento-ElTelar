from datetime import date, datetime
from decimal import Decimal
from django.db import models



def model_to_dict(instance, exclude_fields=None):
    """
    Convierte una instancia de modelo Django a un diccionario JSON serializable.
    Incluye manejo seguro para campos FileField/ImageField.
    """
    if exclude_fields is None:
        exclude_fields = ['_state', 'password']
    
    data = {}

    for field in instance._meta.fields:
        field_name = field.name
        if field_name in exclude_fields:
            continue

        value = getattr(instance, field_name)

        # 🔹 Relaciones FK o OneToOne
        if isinstance(value, models.Model):
            value = value.pk

        # 🔹 Decimales
        elif isinstance(value, Decimal):
            value = float(value)

        # 🔹 Fechas y datetimes
        elif isinstance(value, (date, datetime)):
            value = value.isoformat()

        # 🔹 Archivos o imágenes
        elif isinstance(value, models.fields.files.FieldFile):
            if value and value.name:  # Solo si tiene archivo asociado
                try:
                    value = value.url  # URL relativa o absoluta según configuración
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