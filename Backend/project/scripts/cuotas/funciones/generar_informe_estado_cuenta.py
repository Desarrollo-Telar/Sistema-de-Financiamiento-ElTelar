
from apps.financings.models import  AccountStatement

# UUID
import uuid

def generar_estado_cuenta(cuota, accion, dia):
    estado_cuenta = AccountStatement()
    mostrar = True

    if cuota.credit_id:
        estado_cuenta.credit = cuota.credit_id
        fecha_inicio = cuota.credit_id.fecha_inicio
        fecha_emision = dia
        fecha_limite = cuota.credit_id.fecha_vencimiento
        forma_pago = cuota.credit_id.forma_de_pago


        if (
                fecha_limite is not None and
                fecha_inicio <= fecha_emision <= fecha_limite and
                forma_pago == 'INTERES Y CAPITAL AL VENCIMIENTO'
            ):
            mostrar = False
    
    if cuota.acreedor:
        estado_cuenta.acreedor = cuota.acreedor
    
    if cuota.seguro:
        estado_cuenta.seguro = cuota.seguro

    estado_cuenta.numero_referencia = str(uuid.uuid4())[:8]

    if not mostrar:
        return f'No mostrar'

    if accion == 'FECHA_LIMITE' :
        if cuota.interes_pagado > 0:
            estado_cuenta.description = f'La cuota No. {cuota.mes} se encuentra vencida.\nCapital Pendiente Por Pagar.'
            if cuota.credit_id:
                cuota.credit_id.estados_fechas = False
                
        else:

            estado_cuenta.description = f'La cuota No. {cuota.mes} se encuentra vencida.\nFalta de Pago.'

    if accion == 'FECHA_VENCIMIENTO' :
        if cuota.interes_pagado > 0:
            if cuota.credit_id:
                cuota.credit_id.estados_fechas = False
            estado_cuenta.description = f'La cuota No. {cuota.mes} ha pasado al estado de "Fechas en atraso".\nPor Capital Pendiente Por Pagar.'
        else:
            estado_cuenta.description = f'La cuota No. {cuota.mes} ha pasado al estado de "Fechas en atraso".\nPor Falta de Pago.'


    estado_cuenta.cuota = cuota
    estado_cuenta.saldo_pendiente = cuota.saldo_pendiente
    estado_cuenta.save()


