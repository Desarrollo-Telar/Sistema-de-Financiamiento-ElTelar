
# FUNCIONES
from .sobre_que_pago_analizar import sobre_que_es_pago
    


def cuota_a_pagar(self):
    """
    Encuentra la próxima cuota a pagar en función de la fecha de emisión y el historial de pagos.
    """
    # Obtener todas las cuotas del crédito ordenadas por la fecha límite
    informacion = sobre_que_es_pago(self)

    # Fecha de emisión (como objeto datetime)
    fecha_emision = self.fecha_emision.date()

    if informacion['ultimo_registro_estado_cuenta'] is not None:
        ultima_fecha = informacion['ultimo_registro_estado_cuenta'].payment.fecha_emision.date()
            

        # Calcular la diferencia en días
        diferencia = (ultima_fecha - fecha_emision).days
        print(f"Diferencia en días desde el último pago: {diferencia} días")

        # Si han pasado 15 días desde el último pago
        if diferencia >= 15:
            # Devolver la cuota más reciente impaga
            print('COBRANDO LA ULTIMA CUOTA POR DIFERENCIA DE DÍAS >= 15')
                
            return informacion['ultima_cuota_pagar']
    
    # Recorre las cuotas para realizar las comparaciones por fechas
    print(informacion['cuotas'])
    for cuota in informacion['cuotas']:
        # Usar objetos datetime directamente
        fecha_inicio = cuota.start_date.date()
        fecha_limite = cuota.fecha_limite.date()
        fecha_emision_date = fecha_emision
        
                        
        # Comparar directamente objetos datetime
        if fecha_inicio <= fecha_emision_date <= fecha_limite:
            # Si la fecha de emisión cae dentro del rango de esta cuota
            print(f"Cuota encontrada en rango de fechas: {cuota}")
            if fecha_emision_date == fecha_limite:
                print("Fecha de emisión es igual a la fecha límite, continuando a la siguiente cuota")
                continue 
            return cuota
        
    # Si no se encuentra ninguna cuota aplicable
    print("No se encontró ninguna cuota aplicable")
    return None

    
