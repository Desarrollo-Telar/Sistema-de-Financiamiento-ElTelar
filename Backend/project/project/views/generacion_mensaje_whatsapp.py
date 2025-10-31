from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.customers.models import Customer
from apps.financings.models import PaymentPlan, Credit
from apps.codes.models import TokenCliente

import urllib.parse
from apps.financings.formato import formatear_numero
class GenerarMensajePagoAPIView(APIView):

    def get(self, request, customer_code, cuota_id):
        cliente = Customer.objects.filter(customer_code=customer_code).first()
        cuota = PaymentPlan.objects.filter(id=cuota_id).first()

        if (not cliente) or (not cuota):
            if not cliente:
                return Response({
                    "detail": "Cliente no encontrados."
                }, status=status.HTTP_404_NOT_FOUND)
            
            if not cuota:
                return Response({
                    "detail": "Cuota no encontrados."
                }, status=status.HTTP_404_NOT_FOUND)

        tokken = TokenCliente.objects.filter(cliente=cliente, cuota=cuota).first()

        if tokken is None:
            tokken = TokenCliente.objects.create(
                cliente=cliente, cuota=cuota
            )

        telefono = f'502{cliente.telephone}'
        mensaje = f'''
Estimado *{cliente.first_name} {cliente.last_name}*.
Le recordamos la importancia de realizar su pago correspondiente, el total del monto a cancelar es de *Q{cuota.formato_cuota_total()}* para su cuota No. _{cuota.mes}_.
Tiene como fecha de pago el *{cuota.due_date.date()}*. Agradecemos su boleta de manera urgente para evitar recargos adicionales.

Si tiene alguna duda o necesita asistencia, no dude en comunicarse con nosotros.

Nota. En el siguiente link puede cargar su boleta de pago:
https://www.ii-eltelarsa.com/cliente/{tokken.uuid}/
        '''
        mensaje_codificado = urllib.parse.quote(mensaje)

        link = f'https://wa.me/{telefono}?text={mensaje_codificado}'

        return Response({
            "whatsapp_link": link
        }, status=status.HTTP_200_OK)

class GenerandoMensajeSaldoApi(APIView):

    def get(self, request, credito):
        obtener_credito = Credit.objects.filter(id=credito).first()

        if obtener_credito is None:
            return Response({"detail": "Credito no encontrados."}, status=status.HTTP_200_OK)
        
        telefono = f'502{obtener_credito.customer_id.telephone}'
        
        mensaje = f'''
Estimado *{obtener_credito.customer_id.first_name} {obtener_credito.customer_id.last_name}*.
Le queremos informar que su saldo actual es de *Q {formatear_numero(obtener_credito.saldo_actual)}*
Si requiere verificar detalles, aclarar dudas o necesita asistencia, nuestro equipo está a su disposición. No dude en escribirnos.

        '''
        mensaje_codificado = urllib.parse.quote(mensaje)

        link = f'https://wa.me/{telefono}?text={mensaje_codificado}'

        return Response({
            "whatsapp_link": link
        }, status=status.HTTP_200_OK)