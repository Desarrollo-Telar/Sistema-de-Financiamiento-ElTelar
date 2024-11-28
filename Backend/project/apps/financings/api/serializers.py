# SERIALIZADOR
from rest_framework import serializers

# FORMATO
from apps.financings.formato import formatear_numero
# DIAS
from datetime import datetime
from dateutil.relativedelta import relativedelta

# MODELS
from apps.financings.models import Credit, Guarantees, DetailsGuarantees, Disbursement, Payment, Invoice, Recibo
from apps.financings.models import PaymentPlan, AccountStatement

# ------------ FUNCIONES ----------------------
def mostrar_fecha_limite(fecha_limite):
        limite = fecha_limite - relativedelta(days=1)
        #limite = fecha_limite.replace(hour=5, minute=59, second=0, microsecond=0)
        return limite

def total(capital, interes,mora):
    total = 0
    total = interes + mora + capital
    return formatear_numero(total)

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


class EstadoCuentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountStatement
        fields = '__all__'


class PaymentPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentPlan
        fields = '__all__'
    def to_representation(self, instance):
        return {
            "id":instance.id,
            "mes": instance.mes,
            "start_date": instance.start_date,
            "due_date": instance.due_date,
            "outstanding_balance": formatear_numero(instance.outstanding_balance),
            "mora": formatear_numero(instance.mora),
            "interest": formatear_numero(instance.interest),
            "principal": formatear_numero(instance.principal),
            "installment": formatear_numero(instance.installment),
            "status": instance.status,
            "saldo_pendiente": formatear_numero(instance.saldo_pendiente),
            "interes_pagado": instance.interes_pagado,
            "mora_pagado": instance.mora_pagado,
            "fecha_limite": mostrar_fecha_limite(instance.fecha_limite),
            "cambios": instance.cambios,
            "numero_referencia":instance.numero_referencia,
            "cuota_vencida":instance.cuota_vencida,
            'total_cancelar': total(instance.principal,instance.interest,instance.mora),
            "capital_generado":instance.capital_generado,
            "credit_id":{
                "id":instance.credit_id.id,
                "codigo_credito":instance.credit_id.codigo_credito,
            }
        }