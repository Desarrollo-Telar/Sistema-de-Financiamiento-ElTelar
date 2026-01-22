
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
from apps.financings.models import Credit

class CreditosPorMesAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

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
    permission_classes = [permissions.IsAuthenticated]

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
    permission_classes = [permissions.IsAuthenticated]

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

class CasosExitoAsesorAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        sucursal = getattr(request,'sucursal_actual',None)
        filters = Q()

        if sucursal:
            filters &= Q(sucursal=sucursal)
        
        filters &= Q(is_paid_off=True)
        filters &= Q(asesor_de_credito__isnull=False)

        data = (
            Credit.objects
            .filter(filters)
            .values(
                'asesor_de_credito__nombre',
                'asesor_de_credito__apellido'
            )
            .annotate(cantidad=Count('id'))
        )
        return Response(data)



class CreditosPorAsesorMesAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        sucursal = getattr(request,'sucursal_actual',None)
        filters = Q()

        if sucursal:
            filters &= Q(sucursal=sucursal)
        
        filters &= Q(asesor_de_credito__isnull=False)

        data = (
            Credit.objects
            .filter(filters)
            .annotate(mes=TruncMonth('creation_date'))
            .values(
                'mes',
                'asesor_de_credito__nombre',
                'asesor_de_credito__apellido'
            )
            .annotate(total=Count('id'))
            .order_by('-mes')
        )
        return Response(data)
