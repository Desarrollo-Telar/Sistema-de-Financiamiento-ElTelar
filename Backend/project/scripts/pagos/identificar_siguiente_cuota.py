
# DJANGO
from django.db.models import Q

# FUNCIONES
from .sobre_que_pago_analizar import sobre_que_es_pago

def encontrando_siguiente_cuota(self):
    """
    Devuelve la siguiente cuota después de la cuota a pagar actual.
    """
    # Obtener la cuota actual a pagar
    cuota_actual = self._cuota_pagar()

    if cuota_actual is not None:
        # Obtener todas las cuotas ordenadas por fecha límite
        informacion = sobre_que_es_pago(self)

        # Iterar sobre las cuotas después de la cuota actual
        encontrada = False
        for cuota in informacion['cuotas']:
            if encontrada:
                # Si ya encontramos la cuota actual, la siguiente será la segunda cuota
                if cuota == cuota_actual:
                    return None
                return cuota
                
            if cuota == cuota_actual:
                # Marcamos que encontramos la cuota actual
                encontrada = True

    return None  # Si no existe una siguiente cuota
