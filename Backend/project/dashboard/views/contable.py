
# ORM
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth

# REST
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

# Filtrado
from django.db.models import Q

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
        sucursal = getattr(request,'sucursal_actual',None)
        filters = Q()

        if sucursal:
            filters &= Q(sucursal=sucursal)
        
        filters &= Q(registro_ficticio=False)
        data = (
            Banco.objects
            .filter(filters)
            .annotate(mes=TruncMonth('fecha'))
            .values('mes')
            .annotate(
                ingreso=Sum('credito'),
                egreso=Sum('debito'),
                saldos=Sum('saldo_disponible')
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
