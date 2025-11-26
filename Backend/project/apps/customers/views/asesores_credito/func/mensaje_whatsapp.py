
from apps.financings.models import PaymentPlan
from apps.customers.models import Customer
from apps.codes.models import TokenCliente

def get_mensaje_whatsaap(customer_code, cuota_id):
    cliente = Customer.objects.filter(customer_code=customer_code).first()
    cuota = PaymentPlan.objects.filter(id=cuota_id).first()
    tokken = TokenCliente.objects.filter(cliente=cliente, cuota=cuota).first()
    mensaje = f'''
    Estimado *{cliente.first_name} {cliente.last_name}*.
    Le recordamos la importancia de realizar su pago correspondiente, el total del monto a cancelar es de *Q{cuota.formato_cuota_total()}* para su cuota No. _{cuota.mes}_.
    Tiene como fecha de pago el *{cuota.due_date.date()}*. Agradecemos su boleta de manera urgente para evitar recargos adicionales.

    Si tiene alguna duda o necesita asistencia, no dude en comunicarse con nosotros.

    Nota. En el siguiente link puede cargar su boleta de pago:
    https://www.ii-eltelarsa.com/cliente/{tokken.uuid}/
        '''
    
    return mensaje