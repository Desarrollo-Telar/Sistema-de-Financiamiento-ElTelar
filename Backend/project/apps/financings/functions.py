from decimal import Decimal
from datetime import timedelta
from django.utils import timezone
from django.db.models import Sum  # Importar Sum para el cálculo del saldo pendiente
from apps.financings.models import Credit, PaymentPlan, AccountStatement, Payment, Disbursement
from apps.financings.utils import calcular_capital, calcular_interes, calcular_mora
from datetime import datetime, timedelta

from apps.financings.models import Banco
def realizar_pago(payment, credito_id = None, disbursement_id = None, cliente=None):
    try:
        
        
        
        if disbursement_id:
            pass
        if cliente:
            pass
        
        pagoss = Payment.objects.get(id=payment.id)
        # Obtener el crédito
        """
        if credito_id:
            credito = Credit.objects.get(id=credito_id.id)
            # Verificar si el crédito ya está pagado
            if credito.is_paid_off:
                pagoss.estado_transaccion = 'FALLIDO'
                pagoss.descripcion_estado  = f'\n\nEL REGISTRO DE ESTA BOLETA ES INVALIDA DEBIDO A QUE EL CREDITO AL CUAL SE ESTA ASOCIANDO YA HA SIDO CANCELADO\n\n'
                pagoss.save()
                banco = Banco.objects.filter(referencia=payment.numero_referencia)
                banco.status = True
                banco.save()
                return "Este crédito ya está pagado en su totalidad."
        """

        # Registrar el pago
        
        pagoss.realizar_pago()     
        
        

        
            

        return f"Pago de {pagoss.monto} realizado exitosamente. Saldo restante: "

    except Credit.DoesNotExist:
        return "Crédito no encontrado."
