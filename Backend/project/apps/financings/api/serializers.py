# SERIALIZADOR
from rest_framework import serializers

# MODELS
from apps.financings.models import Credit, Guarantees, DetailsGuarantees, Disbursement, Payment, Invoice, Recibo

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
            'customer_id':{
                'first_name':instance.customer_id.first_name,
                'last_name':instance.customer_id.last_name,

            },
            'proposito':instance.proposito,
            'monto':instance.monto,
            'plazo':instance.plazo,
            'tasa_interes':instance.tasa_interes,
            'forma_de_pago':instance.forma_de_pago,
            'frecuencia_pago':instance.frecuencia_pago,
            'fecha_inicio':instance.fecha_inicio,
            'fecha_vencimiento':instance.fecha_vencimiento,
            'tipo_credito':instance.tipo_credito,
            #'destino_id':instance.destino_id,
            'codigo_credito':instance.codigo_credito,
            'saldo_actual':instance.saldo_actual,
            'saldo_pendiente':instance.saldo_pendiente,
        }


class GuaranteesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guarantees
        fields = '__all__'

class DetailsGuaranteesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailsGuarantees
        fields = '__all__'

class DisbursementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disbursement
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'credit',
            'monto',
            'numero_referencia',
            'fecha_emision',
            'descripcion',
            'boleta'
        ]

class FacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'

class ReciboSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recibo
        fields = '__all__'