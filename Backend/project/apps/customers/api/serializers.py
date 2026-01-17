# Serializador
from rest_framework import serializers
from apps.users.api.serializers import UserSerializer, SubsidiarySerializer


# Models
from apps.customers.models import Customer, ImmigrationStatus, CreditCounselor, Cobranza, HistorialCobranza



class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "first_name",
            "last_name",
            "type_identification",
            "identification_number",
            "telephone",
            "email",
            "status",
            "date_birth",
            "number_nit",
            "place_birth",
            "marital_status",
            "profession_trade",
            "gender",
            "nationality",
            "person_type",
            "user_id",
            "immigration_status_id",
            "description",
            "asesor",
            "fehca_vencimiento_de_tipo_identificacion",
            "new_asesor_credito",
        ]

    def to_representation(self, instance):
        usuario_serializado = UserSerializer(instance.user_id).data if instance.user_id else None
        asesor_serializado = CreditCounselorSerializer(instance.new_asesor_credito).data if instance.new_asesor_credito else None
        condicion_migratoria_serializado = ImmigrationStatusSerializer(instance.immigration_status_id).data if instance.immigration_status_id else None
        ocupacion_serializado = None
        profesion_serializado = None
        sucursal_serializado = SubsidiarySerializer(instance.sucursal).data if instance.sucursal else None


        return {
            'id': instance.id,
            "first_name": instance.first_name,
            "last_name": instance.last_name,
            "type_identification": instance.type_identification,
            "identification_number": instance.identification_number,
            "customer_code":instance.customer_code,
            "telephone":instance.telephone,
            "email":instance.email,
            "status":instance.status,
            "date_birth":instance.date_birth,
            "number_nit":instance.number_nit,
            "place_birth":instance.place_birth,
            "marital_status":instance.marital_status,
            "profession_trade":instance.profession_trade,
            "gender":instance.gender,
            "nationality":instance.nationality,
            "person_type":instance.person_type,
            "description":instance.description,
            "creation_date":instance.creation_date,
            "fehca_vencimiento_de_tipo_identificacion":instance.fehca_vencimiento_de_tipo_identificacion,
            "other_telephone":instance.other_telephone,
            "level_of_education":instance.level_of_education,
            "level_of_education_superior":instance.level_of_education_superior,
            "lugar_emision_tipo_identificacion_departamento":instance.lugar_emision_tipo_identificacion_departamento,
            "lugar_emision_tipo_identificacion_municipio":instance.lugar_emision_tipo_identificacion_municipio,
            "valoracion":instance.valoracion,
            "numero_identificacion_sucursal":instance.numero_identificacion_sucursal,
            "user_id":usuario_serializado,
            "new_asesor_credito":asesor_serializado,
            "immigration_status_id":condicion_migratoria_serializado,
            "sucursal":sucursal_serializado,
            "ocupacion":ocupacion_serializado,
            "profesion":profesion_serializado,
            "asesor":instance.asesor if instance.asesor else None,

           
        }



class ImmigrationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImmigrationStatus
        fields = '__all__'
    
    def to_representation(self, instance):
        return {
            "id":instance.id,
            "condition_name":instance.condition_name,
            "description":instance.description
        }

class CreditCounselorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCounselor
        fields = '__all__'

    def to_representation(self, instance):
        usuario_serializado = UserSerializer(instance.usuario).data if instance.usuario else None
        sucursal_serializado = SubsidiarySerializer(instance.sucursal).data if instance.sucursal else None

        return {
            "id":instance.id,
            "nombre":instance.nombre,
            "apellido":instance.apellido,
            "codigo_asesor":instance.codigo_asesor,
            "type_identification":instance.type_identification,
            "identification_number":instance.identification_number,
            "telephone":instance.telephone,
            "email":instance.email,
            "creation_date":instance.creation_date,
            "fecha_actualizacion":instance.fecha_actualizacion,
            "status":instance.status,
            "gender":instance.gender,
            "nit":instance.nit,
            "recordatorio_clientes":instance.recordatorio_clientes,
            "sucursal":sucursal_serializado,
            "usuario":usuario_serializado
        }

class CobranzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cobranza
        fields = '__all__'
    
    def to_representation(self, instance):
        from apps.financings.api.serializers import CreditSerializer, PaymentPlanSerializer
        credito_serializado = CreditSerializer(instance.credito).data if instance.credito else None
        asesor_credito_serializado = CreditCounselorSerializer(instance.asesor_credito).data  if instance.asesor_credito else None
        cuota_serializado = PaymentPlanSerializer(instance.cuota).data if instance.cuota else None

        return {
            "id":instance.id,
            "tipo_cobranza":instance.tipo_cobranza,
            "fecha_registro":instance.fecha_registro,
            "fecha_gestion":instance.fecha_gestion,
            "fecha_seguimiento":instance.fecha_seguimiento,
            "tipo_gestion":instance.tipo_gestion,
            "resultado":instance.resultado,
            "monto_pendiente":instance.monto_pendiente,
            "interes_pendiente":instance.interes_pendiente,
            "mora_pendiente":instance.mora_pendiente,
            "fecha_limite_cuota":instance.fecha_limite_cuota,
            "fecha_promesa_pago":instance.fecha_promesa_pago,
            "observaciones":instance.observaciones,
            "estado_cobranza":instance.estado_cobranza,
            "telefono_contacto":instance.telefono_contacto,
            "fecha_actualizacion":instance.fecha_actualizacion,
            "codigo_gestion":instance.codigo_gestion,
            "credito":credito_serializado,
            "asesor_credito":asesor_credito_serializado,
            "cuota":cuota_serializado
        }

class HistorialCobranzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialCobranza
        fields = '__all__'
        
    def to_representation(self, instance):
        usuario = None
        cobranza = None
        
        if instance.usuario:
            usuario = UserSerializer(instance.usuario).data

        observaciones_cambio = None

        if instance.datos_nuevos['observaciones']:
            observaciones_cambio = instance.datos_nuevos['observaciones']
        
        if instance.cobranza:
            cobranza = CobranzaSerializer(instance.cobranza).data

        return {
            'id':instance.id,
            'fecha_cambio': instance.fecha_cambio,
            'accion':instance.accion,
            'datos_anteriores': instance.datos_anteriores,
            'usuario':usuario,
            'datos_nuevos':instance.datos_nuevos,
            'cobranza':cobranza,
            'observaciones_cambio': observaciones_cambio,


        }
