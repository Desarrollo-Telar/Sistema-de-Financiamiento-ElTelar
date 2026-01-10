# Serializador
from .serializers import UserSerializer, PermisoUsuarioSerializer

# Models
from apps.users.models import User, PermisoUsuario

# API
from rest_framework import viewsets, status, generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

# HISTORIAL Y BITACORA
from apps.actividades.utils import log_user_action, log_system_event
from scripts.conversion_datos import model_to_dict, cambios_realizados

import traceback
from rest_framework import status
from rest_framework.exceptions import ValidationError

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    
    def perform_create(self, serializer):
        try:
            # 1. Intentamos guardar el usuario
            usuario = serializer.save()
            user = self.request.user

            # 2. Intentamos registrar la acción exitosa
            log_user_action(
                user=user,
                action="Creación de Usuario",
                details=f"Se creó el usuario con username {usuario.username}.",
                request=self.request,
                category_name="Usuarios",
                metadata=model_to_dict(usuario)
            )

        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al crear usuario o registrar log: {str(e)}",
                level_name="ERROR",
                source="UserViewSet.perform_create",
                category_name="Usuarios",
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
            usuario = serializer.save()
            new_data = model_to_dict(usuario)

            changes = {
                "antes": previous_data,
                "despues": new_data
            }

            log_user_action(
                user=self.request.user,
                action="Actualización de Usuario",
                details=f"Se actualizó el usuario con username {usuario.username}.",
                request=self.request,
                category_name="Usuarios",
                metadata=changes
            )
        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al actualizar usuario o registrar log: {str(e)}",
                level_name="ERROR",
                source="UserViewSet.perform_update",
                category_name="Usuarios",
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
        user_data = model_to_dict(instance)
        username = instance.username
        

        log_user_action(
            user=self.request.user,
            action="Eliminación de Usuario",
            details=f"Se eliminó el usuario con username {username}.",
            request=self.request,
            category_name="Usuarios",
            metadata=user_data
        )

        try:
            instance.delete()
            log_user_action(
                user=self.request.user,
                action="Eliminación de Usuarios",
                details=f"Se eliminó el usuario con username {username}.",
                request=self.request,
                category_name="Usuarios",
                metadata=user_data
            )

        except Exception as e:
            import traceback
            log_system_event(
                message=f"Error al eliminar el usuario con username {username}: {str(e)}",
                level_name="ERROR",
                source="UserViewSet.perform_destroy",
                category_name="Usuarios",
                traceback=traceback.format_exc(),
                metadata=user_data
            )
            raise  # re-lanza el error para que DRF devuelva la respuesta HTTP 500


class PermisoUsuarioViewSet(viewsets.ModelViewSet):
    serializer_class = PermisoUsuarioSerializer
    queryset = PermisoUsuario.objects.all()