# TIEMPO
from datetime import datetime, timedelta

def sobre_que_es_pago(self):
    """ 
    El objetivo de esta funcion es poder identificar que tipo de credito de va a cobrar:
    1. Credito para Clientes
    2. Credito para Acreedores
    3. Credito para Seguros

    Y con este analisis, buscar obtener el ultimo registro de su estado de estado de cuenta, todas sus cuotas, y la cuota actual con forme el tiempo
    __lte: Menor o igual que
    __gte: Mayor o igual que
    """
    
    contexto = {}

    dia = datetime.now().date()
    dia_mas_uno = dia + timedelta(days=1)
    

    if self.credit is not None:
        cuotas = self.get_plan_pagos().objects.filter(credit_id=self.credit).order_by('fecha_limite')
        # Historial de pagos anteriores (último pago realizado)
        historial_a = self.get_estado_cuenta().objects.filter(credit=self.credit, description='PAGO DE CREDITO').order_by('-id').first()

        cuota_a_pagar = self.get_plan_pagos().objects.filter(credit_id=self.credit.id,start_date__lte=dia,fecha_limite__gte=dia_mas_uno).first()
        
        if cuota_a_pagar is None:
            cuota_a_pagar = self.get_plan_pagos().objects(credit_id=self.credit.id).order_by('-id').first()
        
        contexto['credito'] = self.credit
        contexto['tasa_interes'] = self.credit.tasa_interes
        contexto['cliente'] = self.credit.customer_id

        contexto['credit'] = self.credit
        contexto['acreedor'] = None
        contexto['seguro'] = None

        contexto['ultimo_registro_estado_cuenta'] = historial_a
        contexto['ultima_cuota_pagar'] = cuota_a_pagar
        contexto['cuotas'] = cuotas

    if self.acreedor is not None:
        cuotas = self.get_plan_pagos().objects.filter(acreedor=self.acreedor).order_by('fecha_limite')
        # Historial de pagos anteriores (último pago realizado)
        historial_a = self.get_estado_cuenta().objects.filter(acreedor=self.acreedor, description='PAGO DE ACREEDOR').order_by('-id').first()

        cuota_a_pagar = self.get_plan_pagos().objects.filter(acreedor=self.acreedor.id, start_date__lte=dia, fecha_limite__gte=dia_mas_uno).first()

        if cuota_a_pagar is None:
            cuota_a_pagar = self.get_plan_pagos().objects.filter(acreedor=self.acreedor.id).order_by('-id').first()

        contexto['credito'] = self.acreedor
        contexto['tasa_interes'] = self.acreedor.tasa
        contexto['cliente'] = None

        contexto['credit'] = None
        contexto['acreedor'] = self.acreedor
        contexto['seguro'] = None

        contexto['ultimo_registro_estado_cuenta'] = historial_a
        contexto['ultima_cuota_pagar'] = cuota_a_pagar
        contexto['cuotas'] = cuotas
        
    if self.seguro is not None:
        cuotas = self.get_plan_pagos().objects.filter(acreedor=self.acreedor).order_by('fecha_limite')
        # Historial de pagos anteriores (último pago realizado)
        historial_a = self.get_estado_cuenta().objects.filter(seguro=self.seguro, description='PAGO DE SEGURO').order_by('-id').first()
        

        cuota_a_pagar = self.get_plan_pagos().objects.filter(seguro=self.seguro.id, start_date__lte=dia, fecha_limite__gte=dia_mas_uno).first()
        
        if cuota_a_pagar is None:
            cuota_a_pagar = self.get_plan_pagos().objects.filter(seguro=self.seguro.id).order_by('-id').first()

        contexto['credito'] = self.seguro
        contexto['tasa_interes'] = self.seguro.tasa
        contexto['cliente'] = None

        contexto['credit'] = None
        contexto['acreedor'] = None
        contexto['seguro'] = self.seguro

        contexto['ultimo_registro_estado_cuenta'] = historial_a
        contexto['ultima_cuota_pagar'] = cuota_a_pagar
        contexto['cuotas'] = cuotas

    
    

    return contexto