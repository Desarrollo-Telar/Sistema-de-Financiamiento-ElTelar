from django.urls import reverse, NoReverseMatch
from django.utils.functional import Promise

def build_notificacion_especificaciones(view_name=None, kwargs=None, extra_data=None):
    """
    Construye un diccionario con información para guardar en el campo JSONField 'especificaciones'.

    :param view_name: Nombre de la vista para generar la URL.
    :param kwargs: Argumentos de URL (como {'pk': 1}).
    :param extra_data: Diccionario adicional con otros datos personalizados.
    :return: Diccionario válido para especificaciones.
    """
    especificaciones = {}

    # Intentar generar la URL
    if view_name:
        try:
            url = reverse(view_name, kwargs=kwargs or {})
            if isinstance(url, Promise):
                url = str(url)
            especificaciones['url'] = url
        except NoReverseMatch:
            especificaciones['url'] = None

    # Agregar datos extra si vienen
    if extra_data:
        for key, value in extra_data.items():
            especificaciones[key] = value

    return especificaciones
