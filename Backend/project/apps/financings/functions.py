from decimal import Decimal
from datetime import timedelta
from django.utils import timezone
from django.db.models import Sum  # Importar Sum para el cálculo del saldo pendiente
from apps.financings.models import Credit, PaymentPlan, AccountStatement, Payment
from apps.financings.utils import calcular_capital, calcular_interes, calcular_mora
from datetime import datetime, timedelta
def realizar_pago(credito_id,  payment):
    try:
        # Obtener el crédito
        credito = Credit.objects.get(id=credito_id.id)  
        pagoss = Payment.objects.get(id=payment.id)
        # Verificar si el crédito ya está pagado
        if credito.is_paid_off:
            pagoss.estado_transaccion = 'FALLIDO'
            pagoss.save()
            return "Este crédito ya está pagado en su totalidad."


        # Registrar el pago
           
        pagoss.realizar_pago()     
        
        

        
            

        return f"Pago de {pagoss.monto} realizado exitosamente. Saldo restante: "

    except Credit.DoesNotExist:
        return "Crédito no encontrado."
