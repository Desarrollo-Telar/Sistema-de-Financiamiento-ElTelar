# Serializador
from apps.financings.api.serializers import  GuaranteesSerializer, DetailsGuaranteesSerializer, DisbursementSerializer, EstadoCuentaSerializer

# MODELS
from apps.financings.models import Guarantees, DetailsGuarantees, Disbursement, AccountStatement


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

import traceback
from rest_framework import status
from rest_framework.exceptions import ValidationError

class EstadoCuentaViewSet(viewsets.ModelViewSet):
    serializer_class = EstadoCuentaSerializer
    queryset = AccountStatement.objects.all()

    def perform_create(self, serializer):
        try:
            
            data = serializer.save()
            user = self.request.user

            # 2. Intentamos registrar la acción exitosa
            log_user_action(
                user=user,
                action="Creación de Estado De Cuentas",
                details=f"Se creó un estado de cuenta {data.id} .",
                request=self.request,
                category_name="Estados De Cuentas",
                metadata=model_to_dict(data)
            )

        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al crear el estado de cuenta o registrar log: {str(e)}",
                level_name="ERROR",
                source="EstadoCuentaViewSet.perform_create",
                category_name="Estados De Cuentas",
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
                action="Actualización de Estados de Cuentas",
                details=f"Se actualizó el estado de cuenta: {data.id}.",
                request=self.request,
                category_name="Estados De Cuentas",
                metadata=changes
            )
        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al actualizar el estado de cuenta o registrar log: {str(e)}",
                level_name="ERROR",
                source="EstadoCuentaViewSet.perform_update",
                category_name="Estados De Cuentas",
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
        nombre = f'{instance.id}'
        

        log_user_action(
            user=self.request.user,
            action="Eliminación de Estado De Cuenta",
            details=f"Se eliminó el estado de cuenta: {nombre}.",
            request=self.request,
            category_name="Estados De Cuentas",
            metadata=data
        )

        try:
            instance.delete()
            log_user_action(
                user=self.request.user,
                action="Eliminación de Estado de Cuenta",
                details=f"Se eliminó el estado de cuenta: {nombre}.",
                request=self.request,
                category_name="Estados De Cuentas",
                metadata=data
            )

        except Exception as e:
            import traceback
            log_system_event(
                message=f"Error al eliminar el estado de cuenta. {nombre}: {str(e)}",
                level_name="ERROR",
                source="EstadoCuentaViewSet.perform_destroy",
                category_name="Documento",
                traceback=traceback.format_exc(),
                metadata=data
            )
            raise  # re-lanza el error para que DRF devuelva la respuesta HTTP 500



class GuaranteesViewSet(viewsets.ModelViewSet):
    serializer_class = GuaranteesSerializer
    queryset = Guarantees.objects.all()

    def perform_create(self, serializer):
        try:
            
            data = serializer.save()
            user = self.request.user

            # 2. Intentamos registrar la acción exitosa
            log_user_action(
                user=user,
                action="Creación de Garantia",
                details=f"Se creó una garantia {data.id} .",
                request=self.request,
                category_name="Garantias",
                metadata=model_to_dict(data)
            )

        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al crear la garantia o registrar log: {str(e)}",
                level_name="ERROR",
                source="GuaranteesViewSet.perform_create",
                category_name="Garantias",
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
                action="Actualización de Garantia",
                details=f"Se actualizó la garantia {data.id}.",
                request=self.request,
                category_name="Garantias",
                metadata=changes
            )
        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al actualizar la garantia o registrar log: {str(e)}",
                level_name="ERROR",
                source="GuaranteesViewSet.perform_update",
                category_name="Garantias",
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
        nombre = f'{instance.id}'
        

        log_user_action(
            user=self.request.user,
            action="Eliminación de Garantia",
            details=f"Se eliminó la garantia: {nombre}.",
            request=self.request,
            category_name="Garantias",
            metadata=data
        )

        try:
            instance.delete()
            log_user_action(
                user=self.request.user,
                action="Eliminación de Garantia",
                details=f"Se eliminó la garantia: {nombre}.",
                request=self.request,
                category_name="Garantias",
                metadata=data
            )

        except Exception as e:
            import traceback
            log_system_event(
                message=f"Error al eliminar la garantia. {nombre}: {str(e)}",
                level_name="ERROR",
                source="GuaranteesViewSet.perform_destroy",
                category_name="Documento",
                traceback=traceback.format_exc(),
                metadata=data
            )
            raise  # re-lanza el error para que DRF devuelva la respuesta HTTP 500



class DetailsGuaranteesViewSet(viewsets.ModelViewSet):
    serializer_class = DetailsGuaranteesSerializer
    queryset = DetailsGuarantees.objects.all()

    def perform_create(self, serializer):
        try:
            
            data = serializer.save()
            user = self.request.user

            # 2. Intentamos registrar la acción exitosa
            log_user_action(
                user=user,
                action="Creación de Detalle de Garantia",
                details=f"Se creó un detalle de garantia {data.id} .",
                request=self.request,
                category_name="Garantias",
                metadata=model_to_dict(data)
            )

        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al crear el detalle de garantia o registrar log: {str(e)}",
                level_name="ERROR",
                source="DetailsGuaranteesViewSet.perform_create",
                category_name="Garantias",
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
                action="Actualización de detalle de garantia",
                details=f"Se actualizó el detalle de garantia: {data.id}.",
                request=self.request,
                category_name="Garantias",
                metadata=changes
            )
        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al actualizar el detalle de garantia o registrar log: {str(e)}",
                level_name="ERROR",
                source="DetailsGuaranteesViewSet.perform_update",
                category_name="Garantias",
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
        nombre = f'{instance.id}'
        

        log_user_action(
            user=self.request.user,
            action="Eliminación de detalle de garantia",
            details=f"Se eliminó el detalle de garantia: {nombre}.",
            request=self.request,
            category_name="Garantias",
            metadata=data
        )

        try:
            instance.delete()
            log_user_action(
                user=self.request.user,
                action="Eliminación de detalle de garantia",
                details=f"Se eliminó el detalle de garantia: {nombre}.",
                request=self.request,
                category_name="Garantias",
                metadata=data
            )

        except Exception as e:
            import traceback
            log_system_event(
                message=f"Error al eliminar el detalle de garantia. {nombre}: {str(e)}",
                level_name="ERROR",
                source="DetailsGuaranteesViewSet.perform_destroy",
                category_name="Garantias",
                traceback=traceback.format_exc(),
                metadata=data
            )
            raise  # re-lanza el error para que DRF devuelva la respuesta HTTP 500



class DisbursementViewSet(viewsets.ModelViewSet):
    serializer_class = DisbursementSerializer
    queryset = Disbursement.objects.all()
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.query_params.get('term', '')  # Obtener el parámetro 'term'
        if search_term:
            queryset = queryset.filter(
                #Q(credit_id__id__icontains=search_term) |
                #Q(credit_id__customer_id__last_name__icontains =search_term)|
                Q(credit_id__codigo_credito__icontains =search_term)
            )  # Filtrar por el término de búsqueda
        return queryset
    
    def perform_create(self, serializer):
        try:
            
            data = serializer.save()
            user = self.request.user

            # 2. Intentamos registrar la acción exitosa
            log_user_action(
                user=user,
                action="Creación de Desembolso",
                details=f"Se creó un desembolso {data.id} .",
                request=self.request,
                category_name="Desembolsos",
                metadata=model_to_dict(data)
            )

        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al crear el desembolso o registrar log: {str(e)}",
                level_name="ERROR",
                source="DisbursementViewSet.perform_create",
                category_name="Desembolsos",
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
                action="Actualización de desembolso",
                details=f"Se actualizó el desembolso {data.id}.",
                request=self.request,
                category_name="Desembolsos",
                metadata=changes
            )
        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al actualizar el desembolso o registrar log: {str(e)}",
                level_name="ERROR",
                source="DisbursementViewSet.perform_update",
                category_name="Desembolsos",
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
        nombre = f'{instance.id}'
        

        log_user_action(
            user=self.request.user,
            action="Eliminación de desembolso",
            details=f"Se eliminó el desembolso: {nombre}.",
            request=self.request,
            category_name="Desembolsos",
            metadata=data
        )

        try:
            instance.delete()
            log_user_action(
                user=self.request.user,
                action="Eliminación de desembolso",
                details=f"Se eliminó el desembolso: {nombre}.",
                request=self.request,
                category_name="Desembolsos",
                metadata=data
            )

        except Exception as e:
            import traceback
            log_system_event(
                message=f"Error al eliminar el desembolso. {nombre}: {str(e)}",
                level_name="ERROR",
                source="DisbursementViewSet.perform_destroy",
                category_name="Desembolsos",
                traceback=traceback.format_exc(),
                metadata=data
            )
            raise  # re-lanza el error para que DRF devuelva la respuesta HTTP 500

