
# ORM
from django.db.models import Q, Sum, OuterRef, Subquery, Max
from django.db.models.functions import TruncMonth

# REST
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions



# Modelo
from apps.financings.models import Payment, Recibo, Banco, AccountStatement, PaymentPlan
from apps.accountings.models import Egress

class DesembolsosPorMesAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        sucursal = getattr(request,'sucursal_actual',None)
        filters = Q()

        if sucursal:
            filters &= Q(sucursal=sucursal)
        
        filters &= Q(tipo_pago='DESEMBOLSO')
        filters &= Q(registro_ficticio=False)
        data = (
            Payment.objects
            .filter(
                filters
                
            )
            .annotate(mes=TruncMonth('fecha_emision'))
            .values('mes')
            .annotate(total=Count('id'))
            .order_by('-mes')
        )
        return Response(data)



class RecuperacionMensualAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        sucursal = getattr(request,'sucursal_actual',None)
        filters = Q()

        if sucursal:
            filters &= Q(sucursal=sucursal)
        
        filters &= Q(cliente__isnull=False)
        
        data = (
            Recibo.objects
            .filter(filters)
            .annotate(mes=TruncMonth('fecha'))
            .values('mes')
            .annotate(
                mora=Sum('mora_pagada'),
                interes=Sum('interes_pagado'),
                capital=Sum('aporte_capital'),
                recibos=Count('id')
            )
            .order_by('mes')
        )
        return Response(data)



class EgresosPorCodigoMesAPIView(APIView):
    def get(self, request):
        sucursal = getattr(request,'sucursal_actual',None)
        filters = Q()

        if sucursal:
            filters &= Q(sucursal=sucursal)

        data = (
            Egress.objects
            .filter(filters)
            .annotate(mes=TruncMonth('fecha'))
            .values('codigo_egreso', 'mes')
            .annotate(
                cantidad=Count('id'),
                monto=Sum('monto')
            )
            .order_by('mes', 'codigo_egreso')
        )
        return Response(data)





class BancosPorMesAPIView(APIView):
    def get(self, request):
        sucursal = getattr(request, 'sucursal_actual', None)
        filters = Q(registro_ficticio=False)

        if sucursal:
            filters &= Q(sucursal=sucursal)

        # 1. Definimos una subquery para encontrar el ID del último registro de cada mes
        # Usamos OuterRef('mes') para vincularlo con el agrupamiento principal
        ultimo_registro_id = Banco.objects.filter(
            filters,
            fecha__year=OuterRef('mes__year'),
            fecha__month=OuterRef('mes__month')
        ).order_by('-fecha', '-id').values('saldo_disponible')[:1]

        # 2. Query principal
        data = (
            Banco.objects
            .filter(filters)
            .annotate(mes=TruncMonth('fecha'))
            .values('mes')
            .annotate(
                ingreso=Sum('credito'),
                egreso=Sum('debito'),
                # Obtenemos el saldo del último movimiento del mes
                saldos=Subquery(ultimo_registro_id)
            )
            .order_by('mes')
        )
        
        return Response(data)




class AcreedoresPorMesAPIView(APIView):
    def get(self, request):
        sucursal = getattr(request,'sucursal_actual',None)
        filters = Q()

        if sucursal:
            filters &= Q(acreedor__sucursal=sucursal)
        
        filters &= Q(payment__isnull=False)
        filters &= Q(acreedor__isnull=False)

        data = (
            AccountStatement.objects
            .filter(filters)
            .annotate(mes=TruncMonth('issue_date'))
            .values('mes')
            .annotate(
                mora_pagada=Sum('late_fee_paid'),
                interes_pagado=Sum('interest_paid'),
                aporte_capital=Sum('capital_paid'),
                saldos=Sum('saldo_pendiente'),
                pagos=Sum('abono')
            )
            .order_by('mes')
        )
        return Response(data)



class MorosidadPorMesAPIView(APIView):
    def get(self, request):
        sucursal = getattr(request, 'sucursal_actual', None)
        filters = Q(
            cuota_vencida=True,
            credit_id__isnull=False,
            mora__gt=0
        )

        if sucursal:
            filters &= Q(sucursal=sucursal)

        data = (
            PaymentPlan.objects
            .filter(filters)
            .annotate(periodo=TruncMonth('fecha_limite'))
            .values('periodo')
            .annotate(cantidad=Count('id'))
            .order_by('periodo')
        )

        return Response(data)
