
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

# SERIALIZADOR
from apps.financings.api.serializers import CreditSerializer

# Paginacion
from .paginacion import StandardResultsSetPagination

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

class DetalleCasosExitoAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        sucursal = getattr(request, 'sucursal_actual', None)
        
        # Aplicamos los mismos filtros de lógica de negocio
        filters = Q(is_paid_off=True, asesor_de_credito__isnull=False)
        if sucursal:
            filters &= Q(sucursal=sucursal)

        # Obtenemos los objetos (QuerySet)
        creditos = Credit.objects.filter(filters).select_related('asesor_de_credito').order_by('id')

        # 2. Instanciar el paginador
        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(creditos, request)

        if page is not None:
            serializer = CreditSerializer(page, many=True)
            # 3. Retornar la respuesta paginada (incluye links a 'next' y 'previous')
            return paginator.get_paginated_response(serializer.data)

        # Usamos tu serializador (many=True porque es una lista)
        serializer = CreditSerializer(creditos, many=True)
        
        return Response(serializer.data)

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
