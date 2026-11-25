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
            'sub_destino',
            'clase_de_documento',
            'cargos_administrativos'


        ]

    def validate(self, attrs):
        instance = getattr(self, 'instance', None)

        tipo_documento = attrs.get(
            'tipo_documento',
            getattr(instance, 'tipo_documento', None) if instance else None,
        )
        clase_de_documento = attrs.get(
            'clase_de_documento',
            getattr(instance, 'clase_de_documento', None) if instance else None,
        )
        fiador_data = attrs.get(
            'fiador',
            getattr(instance, 'fiador', None) if instance else None,
        )
        garantias_data = attrs.get(
            'garantias',
            getattr(instance, 'garantias', None) if instance else None,
        )

        tipo_doc_norm = str(tipo_documento or '').strip().upper()
        clase_norm = str(clase_de_documento or '').strip().upper()

        if tipo_doc_norm == 'RECONOCIMIENTO DE DEUDA':
            if not clase_norm:
                raise serializers.ValidationError({
                    'clase_de_documento': 'Debe seleccionar la clase de documento para el Reconocimiento de Deuda.'
                })

            # Normalizar lista de fiadores
            if isinstance(fiador_data, dict):
                fiadores_lista = [fiador_data]
            elif isinstance(fiador_data, list):
                fiadores_lista = fiador_data
            else:
                fiadores_lista = []

            fiadores_validos = [
                f for f in fiadores_lista
                if (isinstance(f, dict) and f.get('id')) or isinstance(f, int)
            ]

            if clase_norm in ('FIDUCIARIO', 'FIDUCIARIA') and len(fiadores_validos) == 0:
                raise serializers.ValidationError({
                    'fiador': 'Para un Reconocimiento de Deuda de clase Fiduciario debe registrar al menos un fiador.'
                })

            if clase_norm in ('MOBILIARIO', 'MOBILIARIA'):
                todas_garantias = []
                if isinstance(garantias_data, list):
                    todas_garantias.extend(g for g in garantias_data if isinstance(g, dict))
                for f in fiadores_lista:
                    if isinstance(f, dict) and isinstance(f.get('garantias'), list):
                        todas_garantias.extend(g for g in f.get('garantias') if isinstance(g, dict))

                tiene_mobiliaria = any(
                    str(g.get('tipo') or g.get('tipo_garantia') or '').strip().upper() == 'MOBILIARIA'
                    for g in todas_garantias
                )
                if not tiene_mobiliaria:
                    raise serializers.ValidationError({
                        'garantias': 'Para un Reconocimiento de Deuda de clase Mobiliario debe registrar al menos una garantía de tipo MOBILIARIA (en el deudor o en algún fiador).'
                    })

        return attrs

    def to_representation(self, instance):
           
    
        return{
                "id":instance.id,
        }
    