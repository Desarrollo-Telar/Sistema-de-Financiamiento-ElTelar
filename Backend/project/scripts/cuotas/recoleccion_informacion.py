# MODELS
from apps.financings.models import PaymentPlan

# TIEMPO
from datetime import datetime, time

# URL
from django.urls import reverse


def credito_fecha_vencimiento_hoy(creditos_fecha_vencimiento):
    lista = []
    

    for cuota in creditos_fecha_vencimiento:
        contexto = {}
        

        if cuota.credit_id is not None:
            contexto['de'] = cuota.credit_id.customer_id
            contexto['codigo_credito'] = cuota.credit_id.codigo_credito
            contexto['url_cuota'] = reverse('financings:detail_credit', args=[cuota.credit_id.id])

        

        if cuota.acreedor is not None:
            contexto['de'] = cuota.acreedor.nombre_acreedor
            contexto['codigo_credito'] = cuota.acreedor.codigo_acreedor
            contexto['url_cuota'] = reverse('contable:acreedores_detail', args=[cuota.acreedor.id])
            

        if cuota.seguro is not None:
            contexto['de'] = cuota.seguro.nombre_acreedor
            contexto['codigo_credito'] = cuota.seguro.codigo_seguro
            contexto['url_cuota'] = reverse('contable:seguros_detail', args=[cuota.seguro.id])
            
        
        contexto['mes'] = cuota.mes
        contexto['fecha_inicio'] = cuota.start_date.date()
        contexto['fecha_vencimiento'] = cuota.due_date.date()
        contexto['fecha_limite'] = cuota.fecha_limite.date()

        lista.append(contexto)
    
    return lista