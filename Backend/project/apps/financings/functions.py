from decimal import Decimal
from datetime import timedelta
from django.utils import timezone
from django.db.models import Sum  # Importar Sum para el cálculo del saldo pendiente
# MODELOS
from apps.financings.models import Credit, PaymentPlan, AccountStatement, Payment, Disbursement, Banco
from apps.accountings.models import Creditor, Insurance
# CALCULOS
from apps.financings.utils import calcular_capital, calcular_interes, calcular_mora
from datetime import datetime, timedelta

from apps.financings.models import Banco
def realizar_pago(payment):
    try:
        pagoss = Payment.objects.get(id=payment.id)
        banco = Banco.objects.get(referencia = payment.numero_referencia)
        acreedor = Creditor.objects.get(numero_referencia = payment.numero_referencia)
        seguro = Insurance.objects.get(numero_referencia = payment.numero_referencia)
        if acreedor:
            acreedor.status = True
            acreedor.save()
        
        if seguro:
            seguro.status = True
            seguro.save()


        if pagoss.cliente:
            pagoss.estado_transaccion = 'COMPLETADO'
            pagoss.save()
            return f'REGISTRO DE PAGO A CLIENTE'
        
        if pagoss.tipo_pago == 'DESEMBOLSO':
            # registrar en el apartado de desembolso
            pagoss.estado_transaccion = 'COMPLETADO'
            pagoss.save()
            return f'REGISTRO DE DESEMBOLSO'
        
        if pagoss.credit and pagoss.credit.is_paid_off:
            pagoss.estado_transaccion = 'FALLIDO'
            pagoss.descripcion_estado = f'\n\nEL REGISTRO DE ESTA BOLETA ES INVALIDA DEBIDO A QUE EL CREDITO AL CUAL SE ESTA ASOCIANDO YA HA SIDO CANCELADO\n\n'
            pagoss.save()
            banco.status = False
            banco.save()

            

            return f'EL CREDITO YA FUE PAGO'
        
        if pagoss.acreedor and pagoss.acreedor.is_paid_off:
            pagoss.estado_transaccion = 'FALLIDO'
            pagoss.descripcion_estado = f'\n\nEL REGISTRO DE ESTA BOLETA ES INVALIDA DEBIDO A QUE EL ACREEDOR AL CUAL SE ESTA ASOCIANDO YA HA SIDO CANCELADO\n\n'
            pagoss.save()
            banco.status = False
            banco.save()

            acreedor.status = False
            acreedor.save()
            return f'EL ACREEDOR YA FUE PAGO'
        
        if pagoss.seguro and pagoss.seguro.is_paid_off:
            pagoss.estado_transaccion = 'FALLIDO'
            pagoss.descripcion_estado = f'\n\nEL REGISTRO DE ESTA BOLETA ES INVALIDA DEBIDO A QUE EL SEGURO AL CUAL SE ESTA ASOCIANDO YA HA SIDO CANCELADO\n\n'
            pagoss.save()
            banco.status = False
            banco.save()
            
            acreedor.status = False
            acreedor.save()
            return f'EL SEGURO YA FUE PAGO'

        # Registrar el pago
        
        pagoss.realizar_pago()     
        
        

        
            

        return f"Pago de {pagoss.monto} realizado exitosamente. Saldo restante: "

    except Credit.DoesNotExist:
        return "Crédito no encontrado."
