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
        

        if payment.numero_referencia.endswith(("-D", "-d")):
            referencia_sin_d = payment.numero_referencia[:-2]
            banco = Banco.objects.filter(referencia = referencia_sin_d).first()
            

        else:
            banco = Banco.objects.filter(referencia = payment.numero_referencia).first()
            
        acreedor = Creditor.objects.filter(numero_referencia = payment.numero_referencia).first()
        seguro = Insurance.objects.filter(numero_referencia = payment.numero_referencia).first()

        if acreedor is not None:
            acreedor.status = True
            
            payment.estado_transaccion = 'COMPLETADO'
            banco.status = True
            acreedor.save()
            banco.save()
            payment.save()
            return f'VALIDACION DE LA BOLETA PARA ACREEDORES'
        
        if seguro is not None:
            seguro.status = True
            seguro.save()

            payment.estado_transaccion = 'COMPLETADO'
            banco.status = True

            banco.save()
            payment.save()
            return f'VALIDACION DE LA BOLETA PARA SEGUROS'
        
        if payment.cliente is not None:
            payment.estado_transaccion = 'COMPLETADO'
            payment.tipo_pago = 'CLIENTE'
            banco.status = True

            banco.save()
            payment.save()

            return f'REGISTRO DE PAGO A CLIENTE'
        
        if payment.tipo_pago == 'DESEMBOLSO' or payment.tipo_pago == 'INGRESO' or payment.tipo_pago == 'EGRESO':
            payment.estado_transaccion = 'COMPLETADO'
            banco.status = True

            banco.save()
            payment.save()
            return f'REGISTRO PARA LOS DIFERENTES TIPOS DE PAGOS: EGRESO, INGRESO, DESEMBOLSO'

        if payment.credit and payment.credit.is_paid_off or payment.credit.estado_judicial :
            payment.estado_transaccion = 'FALLIDO'
            
            payment.descripcion_estado = f'\n\nEL REGISTRO DE ESTA BOLETA ES INVALIDA DEBIDO A QUE EL CREDITO AL CUAL SE ESTA ASOCIANDO YA HA SIDO CANCELADO\n\n'

            if payment.credit.estado_judicial:
                payment.descripcion_estado = f'\n\nEL REGISTRO DE ESTA BOLETA ES INVALIDA DEBIDO A QUE EL CREDITO ACTUALMENTE SE ENCUENTRA EN UN PROCESO JUDICIAL, POR EL CUAL NO ES POSIBLE REALIZAR ALGUN PAGO\n\n'

            payment.save()
            banco.status = False
            banco.save()
            return f'EL CREDITO YA FUE PAGO'
        
        if payment.acreedor and payment.acreedor.is_paid_off:
            payment.estado_transaccion = 'FALLIDO'
            payment.descripcion_estado = f'\n\nEL REGISTRO DE ESTA BOLETA ES INVALIDA DEBIDO A QUE EL ACREEDOR AL CUAL SE ESTA ASOCIANDO YA HA SIDO CANCELADO\n\n'
            payment.save()
            banco.status = False
            banco.save()

            acreedor.status = False
            acreedor.save()
            return f'EL ACREEDOR YA FUE PAGO'
        
        if payment.seguro and payment.seguro.is_paid_off:
            payment.estado_transaccion = 'FALLIDO'
            payment.descripcion_estado = f'\n\nEL REGISTRO DE ESTA BOLETA ES INVALIDA DEBIDO A QUE EL SEGURO AL CUAL SE ESTA ASOCIANDO YA HA SIDO CANCELADO\n\n'
            payment.save()
            banco.status = False
            banco.save()
            
            acreedor.status = False
            acreedor.save()
            return f'EL SEGURO YA FUE PAGO'

        payment.realizar_pago()  
        return f"Pago de {payment.monto} realizado exitosamente.  "

        

    except Exception as e:
        print(f'Error en funciones 2: {e}')
