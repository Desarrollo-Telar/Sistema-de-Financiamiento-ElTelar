# API
from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from django.utils.timezone import datetime
from datetime import datetime
from rest_framework.request import Request

# MODELOS
from apps.accountings.models import Creditor, Insurance

# SERIALIZAERS
from .serializers import AcreedorSerializers, SeguroSerializers

# HISTORIAL Y BITACORA
from apps.actividades.utils import log_user_action, log_system_event
from scripts.conversion_datos import model_to_dict, cambios_realizados

import traceback
from rest_framework import status
from rest_framework.exceptions import ValidationError

class AcreedoresVigentesViewSet(viewsets.ModelViewSet):
    serializer_class = AcreedorSerializers
    queryset = Creditor.objects.filter(is_paid_off=False)

    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.query_params.get('term', '')  # Obtener el parámetro 'term'
        sucursal = getattr(self.request,'sucursal_actual',None)

        if sucursal:
            queryset = queryset.filter(Q(sucursal=sucursal))

        if search_term:
            queryset = queryset.filter(
                Q(codigo_acreedor__icontains =search_term) |
                Q(nombre_acreedor__icontains=search_term)
            )  # Filtrar por el término de búsqueda
        return queryset
    
    def perform_create(self, serializer):
        try:
            acreedor = serializer.save()
            user = self.request.user
            
            log_user_action(
                user=user,
                action="Creación de Acreedor",
                details=f"Se creó el acreedor por un monto de {acreedor.monto}.",
                request=self.request,
                category_name="Acreedor",
                metadata=model_to_dict(acreedor)
            )
        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al crear un Acreedor o registrar log: {str(e)}",
                level_name="ERROR",
                source="AcreedoresVigentesViewSet.perform_create",
                category_name="Acreedor",
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
            acreedor = serializer.save()
            new_data = model_to_dict(acreedor)

            changes = {
                "antes": previous_data,
                "despues": new_data
            }

            log_user_action(
                user=self.request.user,
                action="Actualización de Acreedor",
                details=f"Se actualizó el acreedor  {acreedor.codigo_acreedor}.",
                request=self.request,
                category_name="Acreedor",
                metadata=changes
            )
        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al crear un Acreedor o registrar log: {str(e)}",
                level_name="ERROR",
                source="AcreedoresVigentesViewSet.perform_update",
                category_name="Acreedor",
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
        acreedor_data = model_to_dict(instance)
              
        log_user_action(
            user=self.request.user,
            action="Eliminación de Acreedor",
            details=f"Se eliminó el acreedor con codigo {instance.codigo_acreedor} por un monto de {instance.monto}.",
            request=self.request,
            category_name="Acreedor",
            metadata=acreedor_data
        )

        try:
            instance.delete()
            log_user_action(
                user=self.request.user,
                action="Eliminación de Acreedor",
                details=f"Se eliminó el acreedor con codigo {instance.codigo_acreedor} por un monto de {instance.monto}.",
                request=self.request,
                category_name="Acreedor",
                metadata=acreedor_data
            )

        except Exception as e:
            import traceback
            log_system_event(
                message=f"Error al eliminar el acreedor con el codigo {instance.codigo_acreedor}: {str(e)}",
                level_name="ERROR",
                source="AcreedoresVigentesViewSet.perform_destroy",
                category_name="Acreedor",
                traceback=traceback.format_exc(),
                metadata=acreedor_data
            )
            raise  # re-lanza el error para que DRF devuelva la respuesta HTTP 500

class SegurosVigentesViewSet(viewsets.ModelViewSet):
    serializer_class = SeguroSerializers
    queryset = Insurance.objects.filter(is_paid_off=False)

    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.query_params.get('term', '')  # Obtener el parámetro 'term'
        sucursal = getattr(self.request,'sucursal_actual',None)

        if sucursal:
            queryset = queryset.filter(Q(sucursal=sucursal))

        if search_term:
            queryset = queryset.filter(
                Q(codigo_seguro__icontains =search_term) |
                Q(nombre_acreedor__icontains=search_term)
            )  # Filtrar por el término de búsqueda
        return queryset
    
    def perform_create(self, serializer):
        try:
            seguro = serializer.save()
            user = self.request.user
            
            log_user_action(
                user=user,
                action="Creación de Seguro",
                details=f"Se creó el seguro por un monto de {seguro.monto}.",
                request=self.request,
                category_name="Seguro",
                metadata=model_to_dict(seguro)
            )
        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al crear un seguro o registrar log: {str(e)}",
                level_name="ERROR",
                source="SegurosVigentesViewSet.perform_create",
                category_name="Seguro",
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
            seguro = serializer.save()
            new_data = model_to_dict(seguro)

            changes = {
                "antes": previous_data,
                "despues": new_data
            }

            log_user_action(
                user=self.request.user,
                action="Actualización de Seguro",
                details=f"Se actualizó el seguro  {seguro.codigo_seguro}.",
                request=self.request,
                category_name="Seguro",
                metadata=changes
            )
        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al crear un seguro o registrar log: {str(e)}",
                level_name="ERROR",
                source="SegurosVigentesViewSet.perform_update",
                category_name="Seguro",
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
        seguro_data = model_to_dict(instance)
              
        log_user_action(
            user=self.request.user,
            action="Eliminación de Seguro",
            details=f"Se eliminó el seguro con codigo {instance.codigo_seguro} por un monto de {instance.monto}.",
            request=self.request,
            category_name="Seguro",
            metadata=seguro_data
        )

        try:
            instance.delete()
            log_user_action(
                user=self.request.user,
                action="Eliminación de Seguro",
                details=f"Se eliminó el seguro con codigo {instance.codigo_seguro} por un monto de {instance.monto}.",
                request=self.request,
                category_name="Seguro",
                metadata=seguro_data
            )

        except Exception as e:
            import traceback
            log_system_event(
                message=f"Error al eliminar el seguro con el codigo {instance.codigo_seguro}: {str(e)}",
                level_name="ERROR",
                source="SegurosVigentesViewSet.perform_destroy",
                category_name="Acreedor",
                traceback=traceback.format_exc(),
                metadata=seguro_data
            )
            raise  # re-lanza el error para que DRF devuelva la respuesta HTTP 500