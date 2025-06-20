
def sobre_que_es_pago(self):
    lista = []

    if self.credit is not None:
        cuotas = self.get_plan_pagos().objects.filter(credit_id=self.credit).order_by('fecha_limite')
        # Historial de pagos anteriores (último pago realizado)
        historial_a = self.get_estado_cuenta().objects.filter(credit=self.credit, description='PAGO DE CREDITO').order_by('-id').first()
        cuota_a_pagar = self.get_plan_pagos().objects.filter(credit_id=self.credit.id).order_by('-id').first()
        lista.append('Credito')
        
    if self.acreedor is not None:
        cuotas = self.get_plan_pagos().objects.filter(acreedor=self.acreedor).order_by('fecha_limite')
        # Historial de pagos anteriores (último pago realizado)
        historial_a = self.get_estado_cuenta().objects.filter(acreedor=self.acreedor, description='PAGO DE ACREEDOR').order_by('-id').first()
        cuota_a_pagar = self.get_plan_pagos().objects.filter(acreedor=self.acreedor.id).order_by('-id').first()
        
    if self.seguro is not None:
        cuotas = self.get_plan_pagos().objects.filter(acreedor=self.acreedor).order_by('fecha_limite')
        # Historial de pagos anteriores (último pago realizado)
        historial_a = self.get_estado_cuenta().objects.filter(seguro=self.seguro, description='PAGO DE SEGURO').order_by('-id').first()
        cuota_a_pagar = self.get_plan_pagos().objects.filter(seguro=self.seguro.id).order_by('-id').first()

    lista.append(cuotas)
    lista.append(historial_a)
    lista.append(cuota_a_pagar)

    return lista
    
    


def cuota_a_pagar(self):
    """
    Encuentra la próxima cuota a pagar en función de la fecha de emisión y el historial de pagos.
    """
    # Obtener todas las cuotas del crédito ordenadas por la fecha límite
    cuotas = None
    historial_a = None
    cuota_a_pagar = None

    


    # Fecha de emisión (como objeto datetime)
    fecha_emision = self.fecha_emision
    print(f"Fecha de emisión: {fecha_emision.date()}")

       

    # Verifica si hay historial de pagos
    if historial_a:
        ultima_fecha = historial_a.payment.fecha_emision
        print(f"Última fecha de pago: {ultima_fecha.date()}")

        # Calcular la diferencia en días
        diferencia = (ultima_fecha - fecha_emision).days
        print(f"Diferencia en días desde el último pago: {diferencia} días")

        # Si han pasado 15 días desde el último pago
        if diferencia >= 15:
            # Devolver la cuota más reciente impaga
            print('COBRANDO LA ULTIMA CUOTA POR DIFERENCIA DE DÍAS >= 15')
                
            return cuota_a_pagar

    else:
        print("No hay historial de pagos")

    # Si no han pasado 31 días, se recorre las cuotas por fechas
    print("Pasando a comparar cuotas por rangos de fechas")

    # Recorre las cuotas para realizar las comparaciones por fechas
    for cuota in cuotas:
        # Usar objetos datetime directamente
        fecha_inicio = cuota.start_date
        fecha_limite = cuota.fecha_limite
        print(f"Comparando cuota con rango: {fecha_inicio.date()} a {fecha_limite.date()}")
                        
        # Comparar directamente objetos datetime
        if fecha_inicio <= fecha_emision <= fecha_limite:
            # Si la fecha de emisión cae dentro del rango de esta cuota
            print("Cuota encontrada en rango de fechas")
            if fecha_emision == fecha_limite:
                print("Fecha de emisión es igual a la fecha límite, continuando a la siguiente cuota")
                continue 
            return cuota

    # Si no se encuentra ninguna cuota aplicable
    print("No se encontró ninguna cuota aplicable")
    return None