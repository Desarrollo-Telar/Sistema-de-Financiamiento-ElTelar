# Serializador
from rest_framework import serializers

# Models
from apps.FinancialInformation.models import WorkingInformation, OtherSourcesOfIncome, Reference, TipoGasto, GastoCliente

class WorkingInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkingInformation
        fields = '__all__'

    def to_representation(self, instance):
        from apps.customers.api.serializers import CustomerSerializer
        cliente = CustomerSerializer(instance.customer_id).data if instance.customer_id else None

        return {
            'id':instance.id,
            'position':instance.position,
            'company_name':instance.company_name,
            'start_date':instance.start_date,
            'description':instance.description,
            'salary':instance.salary,
            'working_hours':instance.working_hours,
            'phone_number':instance.phone_number,
            'source_of_income':instance.source_of_income,
            'income_detail':instance.income_detail,
            'employment_status':instance.employment_status,
            'customer_id': cliente
        }

class OtherSourcesOfIncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherSourcesOfIncome
        fields = '__all__'
    
    def to_representation(self, instance):
        from apps.customers.api.serializers import CustomerSerializer
        cliente = CustomerSerializer(instance.customer_id).data if instance.customer_id else None

        return {
            'id':instance.id,
            'source_of_income':instance.source_of_income,
            'nit':instance.nit,
            'phone_number':instance.phone_number,
            'salary':instance.salary,            
            'customer_id': cliente
        }

class ReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reference
        fields = '__all__'

    def to_representation(self, instance):
        from apps.customers.api.serializers import CustomerSerializer
        cliente = CustomerSerializer(instance.customer_id).data if instance.customer_id else None

        return {
            'id':instance.id,
            'full_name':instance.full_name,
            'phone_number':instance.phone_number,
            'reference_type':instance.reference_type,           
            'customer_id': cliente
        }

class TipoGastoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoGasto
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'id':instance.id,
            'nombre':instance.nombre,
            
        }

class GastoClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = GastoCliente
        fields = '__all__'

    """def to_representation(self, instance):
        from apps.customers.api.serializers import CustomerSerializer
        cliente = CustomerSerializer(instance.customer_id).data if instance.customer_id else None
        tipo_gasto = TipoGastoSerializer(instance.tipo_gasto).data if instance.tipo_gasto else None

        return {
            'id':instance.id,
            'monto':instance.monto,
            'frecuencia':instance.frecuencia,
            'observaciones':instance.observaciones,
            'descripcion':instance.descripcion,
            'tipo_gasto':tipo_gasto,           
            'customer': cliente
        }"""