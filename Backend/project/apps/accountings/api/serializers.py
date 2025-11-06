# SERIALIZADOR
from rest_framework import serializers
from apps.subsidiaries.api.seriealizer import SubsidiarySerializer

# FORMATO
from apps.financings.formato import formatear_numero

# DIAS
from datetime import datetime
from dateutil.relativedelta import relativedelta

# MODELOS
from apps.accountings.models import Creditor, Insurance



class AcreedorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Creditor
        fields = '__all__'
    
   
    def to_representation(self, instance):
        sucursal = SubsidiarySerializer(instance.sucursal).data if instance.sucursal else None
        rep = super().to_representation(instance)
        rep['boleta'] = instance.boleta.url if instance.boleta else None
        rep['monto_formateado'] = instance.fmonto()
        rep['saldo_actual_formateado'] = instance.formato_saldo_actual()
        rep['saldo_pendiente_formateado'] = instance.formato_saldo_pendiente()
        rep['estado_aportacion_texto'] = instance.formato_estado_aportacion()
        rep['estado_fecha_texto'] = instance.formato_estado_fecha()
        rep['estado_credito_texto'] = instance.formato_credito_cancelado()
        rep['sucursal'] = sucursal
        return rep

class SeguroSerializers(serializers.ModelSerializer):
    class Meta:
        model = Insurance
        fields = '__all__'
        
    def to_representation(self, instance):
        sucursal = SubsidiarySerializer(instance.sucursal).data if instance.sucursal else None
        rep = super().to_representation(instance)
        rep['boleta'] = instance.boleta.url if instance.boleta else None
        rep['monto_formateado'] = instance.fmonto()
        rep['saldo_actual_formateado'] = instance.formato_saldo_actual()
        rep['saldo_pendiente_formateado'] = instance.formato_saldo_pendiente()
        rep['estado_aportacion_texto'] = instance.formato_estado_aportacion()
        rep['estado_fecha_texto'] = instance.formato_estado_fecha()
        rep['estado_credito_texto'] = instance.formato_credito_cancelado()
        rep['sucursal'] = sucursal
        return rep