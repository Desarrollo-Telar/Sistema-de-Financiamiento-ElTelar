
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from rest_framework.views import APIView
from rest_framework.response import Response

# Filtrado
from django.db.models import Q

# Modelo
from apps.financings.models import Credit

class CreditosPorMesAPIView(APIView):
    def get(self, request):
        sucursal = getattr(request,'sucursal_actual',None)
        filters = Q()

        if sucursal:
            filters &= Q(sucursal=sucursal)

        data = (
            Credit.objects.filter(filters)
            .annotate(mes=TruncMonth('creation_date'))
            .values('mes')
            .annotate(total=Count('id'))
            .order_by('-mes')
        )
        return Response(data)

class TiposCreditoAPIView(APIView):
    def get(self, request):
        sucursal = getattr(request,'sucursal_actual',None)
        filters = Q()

        if sucursal:
            filters &= Q(sucursal=sucursal)

        data = (
            Credit.objects.filter(filters)
            .values('tipo_credito')
            .annotate(cantidad=Count('id'))
        )
        return Response(data)

class FormasPagoAPIView(APIView):
    def get(self, request):
        sucursal = getattr(request,'sucursal_actual',None)
        filters = Q()

        if sucursal:
            filters &= Q(sucursal=sucursal)

        data = (
            Credit.objects.filter(filters)
            .values('forma_de_pago')
            .annotate(cantidad=Count('id'))
        )
        return Response(data)
