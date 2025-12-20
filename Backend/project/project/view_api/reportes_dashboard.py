# views.py
from rest_framework.views import APIView
from rest_framework.response import Response

# Consultas
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth

# Modelos
from apps.financings.models import Credit, Banco
from apps.accountings.models import Egress

class CreditosPorTipoAPIView(APIView):

    def get(self, request):
        sucursal = getattr(request,'sucursal_actual',None)
        query_set = Credit.objects.values("tipo_credito").annotate(cantidad=Count("id")).order_by("tipo_credito")

        if sucursal:
            query_set = query_set.filter(sucursal=sucursal)

        data = (query_set)

        return Response(data)

class GatosAPIView(APIView):
    def get(self, request):
        sucursal = getattr(request,'sucursal_actual',None)
        query_set = Egress.objects.annotate(mes=TruncMonth("fecha")).values("codigo_egreso", "mes").annotate(
                cantidad=Count("id"),
                monto=Sum("monto")
            ).order_by("mes", "codigo_egreso")
        
        if sucursal:
            query_set = query_set.filter(sucursal=sucursal)

        data = (query_set)

        return Response(data)

class BancosAPIView(APIView):
    def get(self, request):
        sucursal = getattr(request,'sucursal_actual',None)
        query_set = Banco.objects.annotate(mes=TruncMonth("fecha")).values("mes").annotate(ingreso=Sum("credito"), egreso=Sum("debito"), saldo=Sum("saldo_disponible")).order_by("mes")

        if sucursal:
            query_set = query_set.filter(sucursal=sucursal)
        
        data = (query_set)

        return Response(data)