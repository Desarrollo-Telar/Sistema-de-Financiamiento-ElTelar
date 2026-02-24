
# ORM
from django.db.models import Count, Case, When, Q, IntegerField, DecimalField, Sum
from django.db.models.functions import TruncMonth, Coalesce

# REST
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

# Tiempo
from datetime import datetime


# Modelo
from apps.financings.models import Credit

# SERIALIZADOR
from apps.financings.api.serializers import CreditReporteSerializer, CreditSerializer

# Paginacion
from .paginacion import StandardResultsSetPagination

class CreditosPorMesAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        sucursal = getattr(request,'sucursal_actual',None)
        filters = Q()

        dia = datetime.now()
        anio = dia.year

        filters &= Q(creation_date__year = anio)

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
    




class AsesorCarteraAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # 1. Obtener sucursal del request (ajustado a tu lógica)
        sucursal = getattr(request, 'sucursal_actual', None)
        
        # 2. Definir filtros de créditos "limpios" y vigentes
        filters = Q(
            is_paid_off=False,
            estado_judicial=False,
            categoria_credito_demandado__isnull=True,
            asesor_de_credito__isnull=False
        )

        if sucursal:
            filters &= Q(sucursal=sucursal)

        # 3. Construir la consulta
        data = (
            Credit.objects.filter(filters)
            .values(
                'asesor_de_credito__nombre', 
                'asesor_de_credito__apellido'
            )
            .annotate(
                # Conteo de créditos
                total_creditos=Count('id'),
                creditos_en_atraso=Count(
                    Case(When(estados_fechas=False, then=1))
                ),
                
                # Montos de saldo pendiente (Capital)
                saldo_cartera_total=Coalesce(
                    Sum('saldo_pendiente'), 
                    0, 
                    output_field=DecimalField()
                ),
                saldo_en_atraso=Coalesce(
                    Sum(
                        Case(
                            When(estados_fechas=False, then='saldo_pendiente'),
                            default=0,
                            output_field=DecimalField()
                        )
                    ),
                    0, 
                    output_field=DecimalField()
                )
            )
            .order_by('-saldo_cartera_total')
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
        sucursal = getattr(request, 'sucursal_actual', None)
        
        # 1. Definimos la condición de "Crédito Válido" (No judicial y sin categoría)
        # Esto equivale a: categoria_id IS NULL AND estado_judicial = FALSE
        condicion_limpio = Q(
            categoria_credito_demandado__isnull=True, 
            estado_judicial=False
        )

        # 2. Filtros base (Asesor existente y Sucursal si aplica)
        base_filters = Q(asesor_de_credito__isnull=False)
        if sucursal:
            base_filters &= Q(sucursal=sucursal)
        
        # Agregamos la condición de limpieza al filtro base para que 
        # el "Total otorgados" solo cuente los que cumplen tu SQL
        base_filters &= condicion_limpio

        data = (
            Credit.objects
            .filter(base_filters)
            .values(
                'asesor_de_credito__nombre',
                'asesor_de_credito__apellido'
            )
            .annotate(
                # TOTAL DE CREDITOS OTORGADOS (Cumpliendo base_filters)
                total_otorgados=Count('id'),
                
                # TOTAL DE CREDITOS CANCELADOS
                # Además de los filtros base, debe ser is_paid_off = True
                total_cancelados=Count(
                    Case(
                        When(is_paid_off=True, then=1)
                    )
                )
            )
            .order_by('-total_otorgados')
        )
        
        return Response(data)



class CasosJudicialAsesorAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        sucursal = getattr(request, 'sucursal_actual', None)
        
        # Filtros base: Siempre queremos ver créditos NO pagados y con asesor
        base_filters = Q(asesor_de_credito__isnull=False, is_paid_off=False)
        if sucursal:
            base_filters &= Q(sucursal=sucursal)

        data = (
            Credit.objects
            .filter(base_filters)
            .values(
                'asesor_de_credito__nombre',
                'asesor_de_credito__apellido'
            )
            .annotate(
                # TOTAL DE CREDITOS OTORGADOS (Limpio: sin categoría Y no judicial)
                total_otorgados=Count(
                    Case(
                        When(
                            Q(categoria_credito_demandado__isnull=True) & 
                            Q(estado_judicial=False),
                            then=1
                        ),
                        output_field=IntegerField()
                    )
                ),
                
                # TOTAL DE CREDITOS DEMANDADOS (Con categoría Y judicial)
                total_demandados=Count(
                    Case(
                        When(
                             #Q(categoria_credito_demandado__isnull=False) &
                             Q(estado_judicial=True),
                            then=1
                        ),
                        output_field=IntegerField()
                    )
                )
            )
            .order_by('-total_otorgados')
        )
        
        return Response(data)

class CasosAtrasoAsesorAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        sucursal = getattr(request, 'sucursal_actual', None)
        
        # Filtros generales (Base para todos los cálculos)
        base_filters = Q(asesor_de_credito__isnull=False, is_paid_off=False)
        if sucursal:
            base_filters &= Q(sucursal=sucursal)

        data = (
            Credit.objects
            .filter(base_filters)
            .values(
                'asesor_de_credito__nombre',
                'asesor_de_credito__apellido'
            )
            .annotate(
                # Cuenta total de créditos asignados
                total_otorgados=Count(
                    Case(
                        When(
                            Q(categoria_credito_demandado__isnull=True) & Q(estado_judicial=False),
                            then=1
                        ),
                        output_field=IntegerField()
                    )),
                
                total_atrasados=Count(
                    Case(
                        When(
                            (Q(estados_fechas=False) & Q(estado_judicial=False)) & (Q(categoria_credito_demandado__isnull=True)),
                            then=1
                        ),
                        output_field=IntegerField()
                    )
                )
            )
            .order_by('-total_otorgados') # Ordenar por el que más ha otorgado
        )
        
        return Response(data)
    
class CasosAlDiaAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        sucursal = getattr(request, 'sucursal_actual', None)
        
        # Filtros generales (Base para todos los cálculos)
        base_filters = Q(asesor_de_credito__isnull=False)
        if sucursal:
            base_filters &= Q(sucursal=sucursal)

        data = (
            Credit.objects
            .filter(base_filters)
            .values(
                'asesor_de_credito__nombre',
                'asesor_de_credito__apellido'
            )
            .annotate(
                # Cuenta total de créditos asignados
                total_otorgados=Count('id'),
                # Cuenta solo donde is_paid_off es True
                total_atrasados=Count(
                    Case(When(estados_fechas=True, then=1))
                )
            )
            .order_by('-total_otorgados') # Ordenar por el que más ha otorgado
        )
        
        return Response(data)
    
class DetalleCasosExitoAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        sucursal = getattr(request, 'sucursal_actual', None)
        
        # Aplicamos los mismos filtros de lógica de negocio
        filters = Q()
        if sucursal:
            filters &= Q(sucursal=sucursal)

        # Obtenemos los objetos (QuerySet)
        creditos = Credit.objects.filter(filters).select_related('asesor_de_credito').order_by('id')

        if request.query_params.get('no_page') == 'true':
            serializer = CreditSerializer(creditos, many=True)
            return Response(serializer.data)

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
        dia = datetime.now()
        anio = dia.year

        filters &= Q(creation_date__year = anio)

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
