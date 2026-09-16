from django.db.models import Count
from apps.actividades.models import Notification

def obtener_notificaciones_clasificadas():
    # 1. Obtenemos los títulos con su respectiva cuenta de la base de datos
    titulos_raw = (
        Notification.objects.values('title')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    # 2. Diccionario para acumular los totales por categoría limpia
    clasificacion_resumen = {
        "Gestión de Cobranza": 0,
        "Boleta de Pago": 0,
        "Generación de Recibo": 0,
        "Crédito Nuevo": 0,
        "Cliente Nuevo": 0,
        "Boleta de Pago de Cliente": 0,
        "Cuotas": 0,
        "Otros": 0
    }

    # 3. Clasificamos cada título evaluando palabras clave
    for item in titulos_raw:
        title = item['title'].lower()
        cantidad = item['total']

        if "gestion de una cobranza" in title or "cobranza" in title:
            clasificacion_resumen["Gestión de Cobranza"] += cantidad
        elif "ha subido su boleta de pago" in title:
            clasificacion_resumen["Boleta_Pago_Cliente"] += cantidad  # O Boleta de Pago de Cliente
        elif "alerta de boleta" in title:
            clasificacion_resumen["Boleta de Pago"] += cantidad
        elif "recibo" in title:
            clasificacion_resumen["Generación de Recibo"] += cantidad
        elif "credito nuevo" in title or "crédito nuevo" in title:
            clasificacion_resumen["Crédito Nuevo"] += cantidad
        elif "cliente nuevo" in title:
            clasificacion_resumen["Cliente Nuevo"] += cantidad
        elif "cuotas" in title:
            clasificacion_resumen["Cuotas"] += cantidad
        else:
            clasificacion_resumen["Otros"] += cantidad

    return clasificacion_resumen