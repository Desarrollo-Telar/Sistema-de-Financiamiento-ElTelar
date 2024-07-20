# SERIALIZADOR
from rest_framework import serializers

# MODELS
from apps.financings.models import Credit, Guarantees, DetailsGuarantees

class CreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credit
        fields = [
            'proposito',
            'monto',
            'plazo',
            'tasa_interes',
            'forma_de_pago',
            'frecuencia_pago',
            'fecha_inicio',
            'fecha_vencimiento',
            'tipo_credito',
            'destino_id',
            'customer_id',
            
        ]

    def to_representation(self, instance):
        return {
            'id':instance.id,
            'proposito':instance.proposito,
            'monto':instance.monto,
            'plazo':instance.plazo,
            'tasa_interes':instance.tasa_interes,
            'forma_de_pago':instance.forma_de_pago,
            'frecuecia_pago':instance.frecuencia_pago,
            'fecha_inicio':instance.fecha_inicio,
            'fecha_vencimiento':instance.fecha_vencimiento,
            'tipo_credito':instance.tipo_credito,
            'codigo_credito':instance.codigo_credito,
            #'destino_id':instance.destino_id,
            'customer_id':instance.customer_id.id
        }

class GuaranteesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guarantees
        fields = '__all__'

class DetailsGuaranteesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailsGuarantees
        fields = '__all__'