
# Serializador
from apps.financings.api.serializers import  ReciboSerializer

# MODELS
from apps.financings.models import  Recibo

# API
from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from django.utils.timezone import datetime

from rest_framework.request import Request

# Tiempo
from datetime import datetime, timedelta

class ReciboViewSet(viewsets.ModelViewSet):
    serializer_class = ReciboSerializer
    queryset = Recibo.objects.all()

    def get_queryset(self):
        # Obtener parámetros de la solicitud
        request = self.request
        query_params = request.query_params

        # Valores predeterminados
        mes = query_params.get('mes', datetime.now().month)
        anio = query_params.get('anio', datetime.now().year)
        filtro_seleccionado = query_params.get('filtro', 'mora_pagada')

        try:
            mes = int(mes)
            anio = int(anio)
        except ValueError:
            mes = datetime.now().month
            anio = datetime.now().year

        # Filtros por fecha
        filters = Q(fecha__year=anio, fecha__month=mes)

        # Filtros dinámicos según selección del usuario
        filtros_validos = {
            'mora_pagada': 'mora_pagada__gt',
            'interes_pagado': 'interes_pagado__gt',
            'aporte_capital': 'aporte_capital__gt',
        }

        if filtro_seleccionado in filtros_validos:
            filtro_dinamico = {filtros_validos[filtro_seleccionado]: 0}
            return Recibo.objects.filter(filters, **filtro_dinamico)

        return Recibo.objects.filter(filters)

