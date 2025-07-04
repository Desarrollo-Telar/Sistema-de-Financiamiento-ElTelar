# SERIALIZADOR
from rest_framework import serializers

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

class SeguroSerializers(serializers.ModelSerializer):
    class Meta:
        model = Insurance
        fields = '__all__'