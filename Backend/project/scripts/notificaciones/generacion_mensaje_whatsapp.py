# Codificar
import urllib.parse

# Modelos
from apps.customers.models import Customer
from apps.financings.models import PaymentPlan
from apps.codes.models import TokenCliente 

def mensaje_cliente_por_credito(customer_code, cuota):

    cliente = Customer.objects.filter(customer_code=customer_code).first() # Obtener la información del cliente
    cuota = PaymentPlan.objects.filter(id=cuota).first() # Obtener la información de la cuota a pagar

    tokken, create = TokenCliente.objects.get_or_create(cliente=cliente, cuota=cuota)

    
    telefono = f'502{cliente.telephone}'
    mensaje = f'''
Estimado *{cliente.first_name} {cliente.last_name}*.
Le recordamos la importancia de realizar su pago correspondiente, el total del monto a cancelar es de *Q{cuota.formato_cuota_total()}* para su cuota No. _{cuota.mes}_.
Tiene como fecha de pago el *{cuota.due_date.date()}*. Agradecemos su boleta de manera urgente para evitar recargos adicionales.

Si tiene alguna duda o necesita asistencia, no dude en comunicarse con nosotros.

Nota. En el siguiente link puede cargar su boleta de pago.
https://www.ii-eltelarsa.com/cliente/{tokken.uuid}/
    '''
    mensaje_codificado = urllib.parse.quote(mensaje)

    link = f'https://wa.me/{telefono}?text={mensaje_codificado}'

    return link
