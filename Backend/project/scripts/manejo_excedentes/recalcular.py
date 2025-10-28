# Modelos
from apps.financings.models import Recibo, Credit, AccountStatement, PaymentPlan

# HISTORIAL
from apps.actividades.utils import log_user_action, log_system_event
from scripts.conversion_datos import model_to_dict, cambios_realizados


def cuotas_con_excedente():
    creditos = Credit.objects.filter(saldo_actual__lt=0).order_by('-id')

    #creditos = Credit.objects.filter(id=351)

    for credito in creditos:
        # cambiar en el estado de cuenta y en el recibo del ultimo pago
        estado_cuenta = AccountStatement.objects.filter(credit=credito).order_by('-id').first()
        recibo = Recibo.objects.filter(pago=estado_cuenta.payment).first()
        cuota = None

        

        datos_viejos = {
            'credito':model_to_dict(credito),
            'recibo':model_to_dict(recibo) if recibo is not None else None,
            'estado_cuenta':model_to_dict(estado_cuenta)  if estado_cuenta is not None else None,
            'cuota':model_to_dict(cuota) if cuota is not None else None,
        }

        saldo_excedente = abs(credito.saldo_actual) # Poner en positivo el excedente del credito
        
        credito.excedente = saldo_excedente # Poner ese excedente en el saldo excedente del credito

        # Poner en 0 todos los saldos como: saldo actual y saldo pendiente
        credito.saldo_actual = 0 
        credito.saldo_pendiente = 0

        # Cambiando en el estado de cuenta
        estado_cuenta.excedente = saldo_excedente
        estado_cuenta.saldo_pendiente = 0
        aporte_capital = estado_cuenta.capital_paid - saldo_excedente
        estado_cuenta.capital_paid =  aporte_capital

        # Cambiando en el recibo del pago
        recibo.aporte_capital = aporte_capital

        # Cambios realizados a la cuota
        #cuota.saldo_pendiente = 0

        
        

        # Realizando los cambios
        credito.save()
        estado_cuenta.save()
        recibo.save()

        datos_nuevos = {
            'credito':model_to_dict(credito),
            'recibo':model_to_dict(recibo) if recibo is not None else None,
            'estado_cuenta':model_to_dict(estado_cuenta)  if estado_cuenta is not None else None,
            'cuota':model_to_dict(cuota) if cuota is not None else None,
        }

        


        # Guardar los cambios realizados
        log_system_event(
            f'Manejo de excedente para el credito: {credito}',
            'DEBUG',
            'Sistema',
            'Créditos',
            None,
            cambios_realizados(datos_viejos,datos_nuevos)

        )
        print(f'Credito: {credito}')