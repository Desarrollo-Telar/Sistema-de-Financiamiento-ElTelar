# Serializador
from rest_framework import serializers

# Models
from apps.actividades.models import Notification, DetalleInformeCobranza

import locale
from django.utils.timezone import localtime

class NotificationSerializaer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
    
    def to_representation(self, instance):
         # Asegúrate de que la fecha esté en tu zona horaria local
        fecha = localtime(instance.created_at)

        # Formato personalizado: 8 de julio de 2025 a las 11:15
        meses = [
            "enero", "febrero", "marzo", "abril", "mayo", "junio",
            "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
        ]
        fecha_formateada = f"{fecha.day} de {meses[fecha.month - 1]} de {fecha.year} a las {fecha.strftime('%H:%M')}"

        return {
            'id':instance.id,
            'title':instance.title,
            "message": instance.message,
            'created_at': fecha_formateada,
            "read": instance.read,
            "user": instance.user.id,
            'especificaciones':instance.especificaciones,
            'uuid':instance.uuid
        }

class DetalleInformeCobranzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleInformeCobranza
        fields = '__all__'
    
    def to_representation(self, instance):
        reporte = None
        cobranza = None

        if instance.reporte:
            reporte = {
                'id': instance.reporte.id,
            }
        
        if instance.cobranza:
            credito = None

            if instance.cobranza.credito :
                credito = {
                    'id':instance.cobranza.credito.id,
                    'codigo_credito':instance.cobranza.credito.codigo_credito

                }
            cobranza = {
                'id':instance.cobranza.id,
                'estado_cobranza':instance.cobranza.estado_cobranza,
                'credito':credito,
                'fecha_promesa_pago':instance.cobranza.fecha_promesa_pago,
                'fecha_seguimiento': instance.cobranza.fecha_seguimiento,
                'resultado':instance.cobranza.resultado,
                'codigo_gestion':instance.cobranza.codigo_gestion
            }


        return {
            'id':instance.id,
            'reporte': reporte,
            'cobranza':cobranza,
            'porcentajes':instance.porcentajes_cobranza(),
            
        }