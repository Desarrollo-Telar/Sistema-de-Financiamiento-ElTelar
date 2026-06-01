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
Le recordamos que su cuota No. _{cuota.mes}_., tiene fecha de pago el para su cuota *{cuota.due_date.date()}* por un monto de *Q{cuota.formato_cuota_total()}*.

Actualmente, mantiene un saldo pendiente total de *Q{cuota.formato_saldo_actual()}*.
Le agradecemos realizar su pago a la brevedad y enviar su boleta de pago para evitar recargos adicionales o inconvenientes futuros.

Si tiene alguna duda o necesita asistencia, puede comunicarse con nosotros con toda confianza.
Quedamos atentos a su pronta respuesta.        
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
Le informamos que, después de aplicar el pago realizado, su nuevo saldo de capital pendiente es de *Q {formatear_numero(obtener_credito.saldo_actual)}*
Si desea verificar el detalle de su saldo, aclarar alguna duda o necesita asistencia adicional, nuestro equipo está a su disposición. No dude en comunicarse con nosotros.

        '''
        mensaje_codificado = urllib.parse.quote(mensaje)

        link = f'https://wa.me/{telefono}?text={mensaje_codificado}'

        return Response({
            "whatsapp_link": link
        }, status=status.HTTP_200_OK)