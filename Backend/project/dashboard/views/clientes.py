from apps.customers.models import Customer
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from rest_framework.views import APIView
from rest_framework.response import Response

from django.db.models import Q

class ClientesPorMesAPIView(APIView):
    def get(self, request):
        sucursal = getattr(request,'sucursal_actual',None)
        filters = Q()

        if sucursal:
            filters &= Q(sucursal=sucursal)

        data = (
            Customer.objects.filter(filters)
            .annotate(mes=TruncMonth('creation_date'))
            .values('mes')
            .annotate(total=Count('id'))
            .order_by('-mes')
        )
        return Response(data)

