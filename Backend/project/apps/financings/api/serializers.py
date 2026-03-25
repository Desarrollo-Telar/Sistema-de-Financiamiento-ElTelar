# SERIALIZADOR
from rest_framework import serializers

# FORMATO
from apps.financings.formato import formatear_numero
# DIAS
from datetime import datetime
from dateutil.relativedelta import relativedelta

# MODELS
from apps.financings.models import Credit, Guarantees, DetailsGuarantees, Disbursement, Payment, Invoice, Recibo
from apps.financings.models import PaymentPlan, AccountStatement, Banco


# ------------ FUNCIONES ----------------------
def mostrar_fecha_limite(fecha_limite):
        limite = fecha_limite - relativedelta(days=1)
        #limite = fecha_limite.replace(hour=5, minute=59, second=0, microsecond=0)
        return limite

def total(capital, interes,mora, aporte_capital):
    total = 0
    capitals = capital - aporte_capital
    if capitals <=0:
        capitals = 0
    total = interes + mora + capitals
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
            'saldo_pendiente',
            'estados_fechas',
            'plazo_restante',
            'is_paid_off',
            'estado_aportacion',
            'saldo_actual',
            'sucursal',
            'asesor_de_credito',
            'plazo_gracia',
            'fecha_finalizacion_gracia'
        ]

    def to_representation(self, instance):
        from apps.customers.api.serializers import CustomerSerializer
        from apps.subsidiaries.api.seriealizer import SubsidiarySerializer
       
        cliente_serializado = CustomerSerializer(instance.customer_id).data if instance.customer_id else None
        sucursal_serializado = SubsidiarySerializer(instance.sucursal).data if instance.sucursal else None
        data = super().to_representation(instance)

        data['customer_id'] = cliente_serializado
        data['Fmonto'] = formatear_numero(instance.monto)
        data['Fsaldo_actual'] = formatear_numero(instance.saldo_actual)
        data['sucursal'] = sucursal_serializado
        data['creation_date'] = instance.creation_date.date() if instance.creation_date else None
        data['categoria_credito_demandado'] = instance.categoria_credito_demandado.titulo if instance.categoria_credito_demandado else None
        data['codigo_credito'] = instance.codigo_credito
        data['id'] = instance.id
        return data

       

class CreditReporteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Credit
        fields = '__all__'
       

    def to_representation(self, instance):
        from apps.customers.api.serializers import CustomerSerializer
        from apps.subsidiaries.api.seriealizer import SubsidiarySerializer
       
        cliente_serializado = CustomerSerializer(instance.customer_id).data if instance.customer_id else None
        sucursal_serializado = SubsidiarySerializer(instance.sucursal).data if instance.sucursal else None
        data = super().to_representation(instance)

        return data


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

    def to_representation(self,instance):
        return {
            "id":instance.id,
    "forma_desembolso": instance.forma_desembolso,
    "monto_credito": instance.monto_credito,
    "saldo_anterior": instance.saldo_anterior,
    "honorarios": instance.honorarios,
    "poliza_seguro": instance.poliza_seguro,
    "monto_total_desembolso": instance.monto_total_desembolso,
    'monto_credito_agregar':instance.monto_credito_agregar,
    'monto_credito_cancelar':instance.monto_credito_cancelar,
    'description':instance.description,
    "credit_id": {
        "id":instance.credit_id.id,
        'customer_id':{
                'first_name':instance.credit_id.customer_id.first_name,
                'last_name':instance.credit_id.customer_id.last_name,

        },
        'codigo_credito':instance.credit_id.codigo_credito,

    }
}

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'credit',
            'monto',
            'numero_referencia',
            'fecha_emision',
            'descripcion',
            'boleta',
            'tipo_pago',
            'disbursement',
            'cliente',
            'sucursal'
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

def resultado_capital(capital_aportado, capital_generado):
    resutaldo = 0
    resultado = capital_generado - capital_aportado
    if resultado <0:
        resultado = 0
    return formatear_numero(resultado)

class PaymentPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentPlan
        fields = '__all__'
    def to_representation(self, instance):
        credit_data = None
        data = super().to_representation(instance)

        data['credit_id'] = CreditSerializer(instance.credit_id).data if instance.credit_id else None
        data['outstanding_balance'] = formatear_numero(instance.outstanding_balance)
        data['mora'] = formatear_numero(instance.mora)
        data['interest'] = formatear_numero(instance.interest)
        data['principal'] = formatear_numero(instance.principal)
        data['installment'] = formatear_numero(instance.installment)
        data['saldo_pendiente'] = formatear_numero(instance.saldo_pendiente)
        data['fecha_limite'] =  mostrar_fecha_limite(instance.fecha_limite)
        data['fecha_limite_d'] = mostrar_fecha_limite(instance.fecha_limite).date()
        data['total_cancelar'] = total(instance.capital_generado, instance.interest, instance.mora, instance.principal)

        data['capital_generado'] = resultado_capital(instance.principal, instance.capital_generado)
        data['interes_vencido'] = formatear_numero(instance.calculo_interes_acumulado())
        data['interes_actual'] = formatear_numero(instance.calculo_interes_actual())

        return data

        

     

class PaymentPlanSerializerAcreedor(serializers.ModelSerializer):
    class Meta:
        model = PaymentPlan
        fields = '__all__'
    def to_representation(self, instance):
        return {
            "id":instance.id,
            "mes": instance.mes,
            "start_date": instance.start_date,
            "due_date": instance.due_date,
            "Fstart_date": instance.start_date,
            "Fdue_date": instance.due_date,
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
            'total_cancelar': total(instance.capital_generado,instance.interest,instance.mora,instance.principal),
            "capital_generado": resultado_capital(instance.principal, instance.capital_generado),
            "interes_generado":instance.interes_generado,
            "interes_acumulado_generado":instance.interes_acumulado_generado,
            "mora_acumulado_generado":instance.mora_acumulado_generado,
            "mora_generado": instance.mora_generado,
            "acreedor":{
                "id":instance.acreedor.id,
                "codigo_acreedor":instance.acreedor.codigo_acreedor,
                "is_paid_off":instance.acreedor.is_paid_off,
                "estado_aportacion":instance.acreedor.estado_aportacion,
                "estados_fechas":instance.acreedor.estados_fechas,
                
            }
        }

class PaymentPlanSerializerSeguro(serializers.ModelSerializer):
    class Meta:
        model = PaymentPlan
        fields = '__all__'
    def to_representation(self, instance):
        return {
            "id":instance.id,
            "mes": instance.mes,
            "start_date": instance.start_date,
            "due_date": instance.due_date,
            "Fstart_date": instance.start_date,
            "Fdue_date": instance.due_date,
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
            'total_cancelar': total(instance.capital_generado,instance.interest,instance.mora,instance.principal),
            "capital_generado": resultado_capital(instance.principal, instance.capital_generado),
            "interes_generado":instance.interes_generado,
            "interes_acumulado_generado":instance.interes_acumulado_generado,
            "mora_acumulado_generado":instance.mora_acumulado_generado,
            "mora_generado": instance.mora_generado,
            "seguro":{
                "id":instance.seguro.id,
                "codigo_seguro":instance.seguro.codigo_seguro,
                "is_paid_off":instance.seguro.is_paid_off,
                "estado_aportacion":instance.seguro.estado_aportacion,
                "estados_fechas":instance.seguro.estados_fechas,
                
            }
        }