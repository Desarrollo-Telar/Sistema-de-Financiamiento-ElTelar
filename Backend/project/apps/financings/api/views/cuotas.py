# Serializador
from apps.financings.api.serializers import  PaymentPlanSerializer, PaymentPlanSerializerSeguro,PaymentPlanSerializerAcreedor
# MODELS
from apps.financings.models import PaymentPlan

# API
from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from django.utils.timezone import datetime

from rest_framework.request import Request

# Tiempo
from datetime import datetime, timedelta



class PaymentPlanViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentPlanSerializer
    queryset = PaymentPlan.objects.all()

class PaymentPlanUltimoViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentPlanSerializer
    queryset = PaymentPlan.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.query_params.get('term', '')  # Obtener el parámetro 'term'

        if search_term:
            queryset = PaymentPlan.filter(
                Q(id__icontains=search_term) 
            ).first()


        
        return queryset 

class PaymentPlanAmpliacion(viewsets.ModelViewSet):
    serializer_class = PaymentPlanSerializer
    queryset = PaymentPlan.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.query_params.get('term', '')  # Obtener el parámetro 'term'

        if search_term:
            dia = datetime.now().date()
            dia_mas_uno = dia + timedelta(days=1)

            siguiente_pago = PaymentPlan.objects.filter(
                credit_id__id=search_term,
                start_date__lte=dia,
                fecha_limite__gte=dia_mas_uno
            ).first()

            if siguiente_pago is None:
                siguiente_pago = PaymentPlan.objects.filter(
                    credit_id__id=search_term
                ).order_by('-id').first()

            if siguiente_pago:
                return PaymentPlan.objects.filter(id=siguiente_pago.id)
            else:
                return PaymentPlan.objects.none()  # Devuelve un queryset vacío

        return queryset

class PaymentPlanAcreedorUltimoViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentPlanSerializerAcreedor
    queryset = PaymentPlan.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        search_term = self.request.query_params.get('term', '')
        if search_term:
            queryset = queryset.filter(
                Q(id__icontains=search_term) 
            )
        last_item = queryset.order_by('-id').first()
        if last_item:
            serializer = self.get_serializer(last_item)
            return Response(serializer.data)
        return Response([])  # Si no hay datos que coincidan, devolver una lista vacía

class PaymentPlanSeguroUltimoViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentPlanSerializerSeguro
    queryset = PaymentPlan.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        search_term = self.request.query_params.get('term', '')
        if search_term:
            queryset = queryset.filter(
                Q(seguro__id__icontains=search_term) 
            )
        last_item = queryset.order_by('-id').first()
        if last_item:
            serializer = self.get_serializer(last_item)
            return Response(serializer.data)
        return Response([])  # Si no hay datos que coincidan, devolver una lista vacía
    