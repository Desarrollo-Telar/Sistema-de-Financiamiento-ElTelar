# SERIALIZADOR
from rest_framework import serializers

# MODELS
from apps.InvestmentPlan.models import InvestmentPlan

class InvestmentPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentPlan
        fields = [
            'type_of_product_or_service',
            'total_value_of_the_product_or_service',
            'investment_plan_description',
            'initial_amount',
            'monthly_amount',
            'transfers_or_transfer_of_funds',
            'type_of_transfers_or_transfer_of_funds',
            'customer_id',
            'asesor_responsable',
            'estado_aprobacion',
            'fecha_inicio',
            'plazo',
            'plazo_gracia',
            'forma_de_pago',
            'tasa_interes',
            'tipo_documento',
            'tipo_pagare',
            'fiador',
            'credito_anterior_vigente',
            'garantias',
            'sucursal',
            'notarios',
            'riesgo_comercial',
            'diganostico_oportunidad',
            'mitigadores',
            'evaluacion_mercado',


        ]
    