# Serializador
from .serializers import InvestmentPlanSerializer

# Models
from apps.InvestmentPlan.models import InvestmentPlan

# API
from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response

# HISTORIAL Y BITACORA
from apps.actividades.utils import log_user_action, log_system_event
from scripts.conversion_datos import model_to_dict, cambios_realizados

import traceback
from rest_framework import status
from rest_framework.exceptions import ValidationError

class InvestmentPlanViewSet(viewsets.ModelViewSet):
    serializer_class = InvestmentPlanSerializer
    queryset = InvestmentPlan.objects.all()

    def perform_create(self, serializer):
        try:
            
            data = serializer.save()
            user = self.request.user

            # 2. Intentamos registrar la acción exitosa
            log_user_action(
                user=user,
                action="Creación de Pagare",
                details=f"Se creó un pagare {data.type_of_product_or_service} .",
                request=self.request,
                category_name="Pagare",
                metadata=model_to_dict(data)
            )

        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al crear el pagare o registrar log: {str(e)}",
                level_name="ERROR",
                source="InvestmentPlanViewSet.perform_create",
                category_name="Pagare",
                traceback=error_stack,
                metadata={
                    "request_data": self.request.data,
                    "user_attempting": str(self.request.user)
                }
            )
            
            # 4. Relanzamos una excepción para que el cliente reciba un error 400/500
            raise ValidationError({
                "error": "No se pudo completar la operación. El incidente ha sido reportado al sistema."
            })
    
    def perform_update(self, serializer):
        try:
            instance = self.get_object()
            previous_data = model_to_dict(instance)
            data = serializer.save()
            new_data = model_to_dict(data)

            changes = {
                "antes": previous_data,
                "despues": new_data
            }

            log_user_action(
                user=self.request.user,
                action="Actualización de Pagare",
                details=f"Se actualizó el pagare {data.type_of_product_or_service}.",
                request=self.request,
                category_name="Pagare",
                metadata=changes
            )
        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al actualizar el pagare o registrar log: {str(e)}",
                level_name="ERROR",
                source="InvestmentPlanViewSet.perform_update",
                category_name="Pagare",
                traceback=error_stack,
                metadata={
                    "request_data": self.request.data,
                    "user_attempting": str(self.request.user)
                }
            )
            
            # 4. Relanzamos una excepción para que el cliente reciba un error 400/500
            raise ValidationError({
                "error": "No se pudo completar la operación. El incidente ha sido reportado al sistema."
            })

    def perform_destroy(self, instance):
        data = model_to_dict(instance)
        nombre = f'{instance.type_of_product_or_service}'
        

        log_user_action(
            user=self.request.user,
            action="Eliminación de Pagare",
            details=f"Se eliminó el pagare: {nombre}.",
            request=self.request,
            category_name="Pagare",
            metadata=data
        )

        try:
            instance.delete()
            log_user_action(
                user=self.request.user,
                action="Eliminación de Pagare",
                details=f"Se eliminó el pagare: {nombre}.",
                request=self.request,
                category_name="Pagare",
                metadata=data
            )

        except Exception as e:
            import traceback
            log_system_event(
                message=f"Error al eliminar el pagare. {nombre}: {str(e)}",
                level_name="ERROR",
                source="InvestmentPlanViewSet.perform_destroy",
                category_name="Pagare",
                traceback=traceback.format_exc(),
                metadata=data
            )
            raise  # re-lanza el error para que DRF devuelva la respuesta HTTP 500

