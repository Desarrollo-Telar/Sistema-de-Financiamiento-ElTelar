
# Serializador
from apps.financings.api.serializers import PaymentSerializer

# MODELS
from apps.financings.models import Payment

# API
from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from django.utils.timezone import datetime

from rest_framework.request import Request

# Tiempo
from datetime import datetime, timedelta

# HISTORIAL Y BITACORA
from apps.actividades.utils import log_user_action, log_system_event
from scripts.conversion_datos import model_to_dict, cambios_realizados

class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.query_params.get('term', '')  # Obtener el parámetro 'term'
        sucursal = getattr(self.request,'sucursal_actual',None)

        if sucursal:
            queryset = queryset.filter(Q(sucursal=sucursal))

        if search_term:
            queryset = queryset.filter(
                
                Q(numero_referencia__icontains =search_term)
            )  # Filtrar por el término de búsqueda
        return queryset
    
    def perform_create(self, serializer):
        pago = serializer.save()
        user = self.request.user
        log_user_action(
            user=user,
            action="Creación de pago",
            details=f"Se creó el pago de tipo {pago.tipo_pago} por un monto de {pago.monto}.",
            request=self.request,
            category_name="Pagos",
            metadata=model_to_dict(pago)
        )
    
    def perform_update(self, serializer):
        instance = self.get_object()
        previous_data = model_to_dict(instance)
        pago = serializer.save()
        new_data = model_to_dict(pago)

        changes = {
            "antes": previous_data,
            "despues": new_data
        }

        log_user_action(
            user=self.request.user,
            action="Actualización de pago",
            details=f"Se actualizó el pago de tipo {pago.tipo_pago}.",
            request=self.request,
            category_name="Pagos",
            metadata=changes
        )
    
    def perform_destroy(self, instance):
        pago_data = model_to_dict(instance)
        tipo_pago = instance.tipo_pago        
        monto = instance.monto
        numero_referencia = instance.numero_referencia

        log_user_action(
            user=self.request.user,
            action="Eliminación de pago",
            details=f"Se eliminó el pago de tipo {tipo_pago} por un monto de {monto}.",
            request=self.request,
            category_name="Pagos",
            metadata=pago_data
        )

        try:
            instance.delete()
            log_user_action(
                user=self.request.user,
                action="Eliminación de pago",
                details=f"e eliminó el pago de tipo {tipo_pago}  por un monto de {monto}.",
                request=self.request,
                category_name="Pagos",
                metadata=pago_data
            )

        except Exception as e:
            import traceback
            log_system_event(
                message=f"Error al eliminar el pago con numero de referencia {numero_referencia}: {str(e)}",
                level_name="ERROR",
                source="PaymentViewSet.perform_destroy",
                category_name="Pagos",
                traceback=traceback.format_exc(),
                metadata=pago_data
            )
            raise  # re-lanza el error para que DRF devuelva la respuesta HTTP 500

