from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.customers.models import Customer
from apps.financings.models import PaymentPlan
from apps.codes.models import TokenCliente

import urllib.parse

class GenerarMensajePagoAPIView(APIView):

    def get(self, request, customer_code, cuota_id):
        cliente = Customer.objects.filter(customer_code=customer_code).first()
        cuota = PaymentPlan.objects.filter(id=cuota_id).first()

        if not cliente or not cuota:
            return Response({
                "detail": "Cliente o cuota no encontrados."
            }, status=status.HTTP_404_NOT_FOUND)

        tokken, created = TokenCliente.objects.get_or_create(cliente=cliente, cuota=cuota)

        telefono = f'502{cliente.telephone}'
        mensaje = f'''
Estimado *{cliente.first_name} {cliente.last_name}*.
Le recordamos la importancia de realizar su pago correspondiente, el total del monto a cancelar es de *Q{cuota.formato_cuota_total()}* para su cuota No. _{cuota.mes}_.
Tiene como fecha límite el *{cuota.mostrar_fecha_limite_mensaje().date()}*. Agradecemos su boleta de manera urgente para evitar recargos adicionales.

Si tiene alguna duda o necesita asistencia, no dude en comunicarse con nosotros.

Nota. En el siguiente link puede cargar su boleta de pago:
https://www.ii-eltelarsa.com/cliente/{tokken.uuid}/
        '''
        mensaje_codificado = urllib.parse.quote(mensaje)

        link = f'https://wa.me/{telefono}?text={mensaje_codificado}'

        return Response({
            "whatsapp_link": link
        }, status=status.HTTP_200_OK)
