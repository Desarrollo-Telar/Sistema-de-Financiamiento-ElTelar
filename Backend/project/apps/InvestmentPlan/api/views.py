# Serializador
from .serializers import InvestmentPlanSerializer

# Models
from apps.InvestmentPlan.models import InvestmentPlan

# API
from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response

class InvestmentPlanViewSet(viewsets.ModelViewSet):
    serializer_class = InvestmentPlanSerializer
    queryset = InvestmentPlan.objects.all()