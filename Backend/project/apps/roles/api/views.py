# Serializador
from .serializers import RoleSerializer, PermisoSerializer

# Models
from apps.roles.models import Role, Permiso

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

class RoleViewSet(viewsets.ModelViewSet):
    serializer_class = RoleSerializer
    queryset = Role.objects.all()

    def perform_create(self, serializer):
        try:
            
            data = serializer.save()
            user = self.request.user

            # 2. Intentamos registrar la acción exitosa
            log_user_action(
                user=user,
                action="Creación de Rol",
                details=f"Se creó un Rol {data.role_name} .",
                request=self.request,
                category_name="Rol",
                metadata=model_to_dict(data)
            )

        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al crear un rol o registrar log: {str(e)}",
                level_name="ERROR",
                source="RoleViewSet.perform_create",
                category_name="Rol",
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
                action="Actualización de Rol",
                details=f"Se actualizó el rol {data.role_name}.",
                request=self.request,
                category_name="Rol",
                metadata=changes
            )
        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al actualizar el rol o registrar log: {str(e)}",
                level_name="ERROR",
                source="RoleViewSet.perform_update",
                category_name="Rol",
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
        nombre = f'{instance.role_name}'
        

        log_user_action(
            user=self.request.user,
            action="Eliminación de Rol",
            details=f"Se eliminó el Rol: {nombre}.",
            request=self.request,
            category_name="Rol",
            metadata=data
        )

        try:
            instance.delete()
            log_user_action(
                user=self.request.user,
                action="Eliminación de Rol",
                details=f"Se eliminó el Rol: {nombre}.",
                request=self.request,
                category_name="Rol",
                metadata=data
            )

        except Exception as e:
            import traceback
            log_system_event(
                message=f"Error al eliminar el rol. {nombre}: {str(e)}",
                level_name="ERROR",
                source="RoleViewSet.perform_destroy",
                category_name="Rol",
                traceback=traceback.format_exc(),
                metadata=data
            )
            raise  # re-lanza el error para que DRF devuelva la respuesta HTTP 500



class PermisoViewSet(viewsets.ModelViewSet):
    serializer_class = PermisoSerializer
    queryset = Permiso.objects.all()

    def perform_create(self, serializer):
        try:
            
            data = serializer.save()
            user = self.request.user

            # 2. Intentamos registrar la acción exitosa
            log_user_action(
                user=user,
                action="Creación de Permiso",
                details=f"Se creó una permiso {data.nombre} .",
                request=self.request,
                category_name="Permiso",
                metadata=model_to_dict(data)
            )

        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al crear un permiso o registrar log: {str(e)}",
                level_name="ERROR",
                source="PermisoViewSet.perform_create",
                category_name="Permiso",
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
                action="Actualización de Permiso",
                details=f"Se actualizó el permiso {data.nombre}.",
                request=self.request,
                category_name="Permiso",
                metadata=changes
            )
        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al actualizar el permiso o registrar log: {str(e)}",
                level_name="ERROR",
                source="PermisoViewSet.perform_update",
                category_name="Permiso",
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
        nombre = f'{instance.nombre}'
        

        log_user_action(
            user=self.request.user,
            action="Eliminación de Permiso",
            details=f"Se eliminó el permiso: {nombre}.",
            request=self.request,
            category_name="Permiso",
            metadata=data
        )

        try:
            instance.delete()
            log_user_action(
                user=self.request.user,
                action="Eliminación de Permiso",
                details=f"Se eliminó el permiso: {nombre}.",
                request=self.request,
                category_name="Permiso",
                metadata=data
            )

        except Exception as e:
            import traceback
            log_system_event(
                message=f"Error al eliminar el permiso. {nombre}: {str(e)}",
                level_name="ERROR",
                source="PermisoViewSet.perform_destroy",
                category_name="Permiso",
                traceback=traceback.format_exc(),
                metadata=data
            )
            raise  # re-lanza el error para que DRF devuelva la respuesta HTTP 500

