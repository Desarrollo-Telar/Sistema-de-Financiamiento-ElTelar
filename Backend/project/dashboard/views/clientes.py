
# ORM
from django.db.models import Count, Sum


from django.db.models.functions import TruncMonth, Concat
from django.db.models import Value, CharField

# REST
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

# Filtrado
from django.db.models import Q

# Modelo
from apps.customers.models import Customer



class ClientesPorMesAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        sucursal = getattr(request,'sucursal_actual',None)
        filters = Q()

        

        data = (
            Customer.objects.filter(filters)
            .annotate(mes=TruncMonth('creation_date'))
            .values('mes')
            .annotate(total=Count('id'))
            .order_by('mes')
        )
        return Response(data)

class ClientesPorAsesorMesAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        sucursal = getattr(request,'sucursal_actual',None)
        filters = Q()

        if sucursal:
            filters &= Q(sucursal=sucursal)

        filters &= Q(new_asesor_credito__isnull=False)


        data = (
            Customer.objects.filter(filters)
            .annotate(
        mes=TruncMonth('creation_date'),
        nombre_asesor=Concat(
            'new_asesor_credito__nombre',
            Value(' '),
            'new_asesor_credito__apellido',
            output_field=CharField()
        )
    )
    .values('mes', 'nombre_asesor')
    .annotate(total=Count('id'))
    .order_by('mes')
        )
        return Response(data)
