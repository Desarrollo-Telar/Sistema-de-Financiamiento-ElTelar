# Serializador
from .serializers import ImagenAddressSerializer, ImagenSerializer, ImagenCustomerSerializer, ImagenOtherSerializer, ImagenGuaranteeSerializer

# Models
from apps.pictures.models import Imagen, ImagenAddress, ImagenCustomer, ImagenOther, ImagenGuarantee

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


class ImagenViewSet(viewsets.ModelViewSet):
    serializer_class = ImagenSerializer
    queryset = Imagen.objects.all()

    def perform_create(self, serializer):
        try:
            
            data = serializer.save()
            user = self.request.user

            # 2. Intentamos registrar la acción exitosa
            log_user_action(
                user=user,
                action="Creación de Imagen",
                details=f"Se creó una Imagen {data.id} .",
                request=self.request,
                category_name="Imagen",
                metadata=model_to_dict(data)
            )

        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al crear la Imagen o registrar log: {str(e)}",
                level_name="ERROR",
                source="ImagenViewSet.perform_create",
                category_name="Imagen",
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
                action="Actualización de Imagen",
                details=f"Se actualizó la Imagen {data.id}.",
                request=self.request,
                category_name="Imagen",
                metadata=changes
            )
        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al actualizar la Imagen o registrar log: {str(e)}",
                level_name="ERROR",
                source="ImagenViewSet.perform_update",
                category_name="Imagen",
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
            action="Eliminación de Imagen",
            details=f"Se eliminó la Imagen: {nombre}.",
            request=self.request,
            category_name="Imagen",
            metadata=data
        )

        try:
            instance.delete()
            log_user_action(
                user=self.request.user,
                action="Eliminación de Imagen",
                details=f"Se eliminó la Imagen: {nombre}.",
                request=self.request,
                category_name="Imagen",
                metadata=data
            )

        except Exception as e:
            import traceback
            log_system_event(
                message=f"Error al eliminar la Imagen. {nombre}: {str(e)}",
                level_name="ERROR",
                source="ImagenViewSet.perform_destroy",
                category_name="Imagen",
                traceback=traceback.format_exc(),
                metadata=data
            )
            raise  # re-lanza el error para que DRF devuelva la respuesta HTTP 500



class ImagenAddressViewSet(viewsets.ModelViewSet):
    serializer_class = ImagenAddressSerializer
    queryset = ImagenAddress.objects.all()

    def perform_create(self, serializer):
        try:
            
            data = serializer.save()
            user = self.request.user

            # 2. Intentamos registrar la acción exitosa
            log_user_action(
                user=user,
                action="Creación de Imagen",
                details=f"Se creó una Imagen {data.id} .",
                request=self.request,
                category_name="Imagen",
                metadata=model_to_dict(data)
            )

        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al crear la Imagen o registrar log: {str(e)}",
                level_name="ERROR",
                source="ImagenAddressViewSet.perform_create",
                category_name="Imagen",
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
                action="Actualización de Imagen",
                details=f"Se actualizó la Imagen {data.id}.",
                request=self.request,
                category_name="Imagen",
                metadata=changes
            )
        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al actualizar la Imagen o registrar log: {str(e)}",
                level_name="ERROR",
                source="ImagenAddressViewSet.perform_update",
                category_name="Imagen",
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
            action="Eliminación de Imagen",
            details=f"Se eliminó la Imagen: {nombre}.",
            request=self.request,
            category_name="Imagen",
            metadata=data
        )

        try:
            instance.delete()
            log_user_action(
                user=self.request.user,
                action="Eliminación de Imagen",
                details=f"Se eliminó la Imagen: {nombre}.",
                request=self.request,
                category_name="Imagen",
                metadata=data
            )

        except Exception as e:
            import traceback
            log_system_event(
                message=f"Error al eliminar la Imagen. {nombre}: {str(e)}",
                level_name="ERROR",
                source="ImagenAddressViewSet.perform_destroy",
                category_name="Imagen",
                traceback=traceback.format_exc(),
                metadata=data
            )
            raise  # re-lanza el error para que DRF devuelva la respuesta HTTP 500



class ImagenCustomerViewSet(viewsets.ModelViewSet):
    serializer_class = ImagenCustomerSerializer
    queryset = ImagenCustomer.objects.all()

    def perform_create(self, serializer):
        try:
            
            data = serializer.save()
            user = self.request.user

            # 2. Intentamos registrar la acción exitosa
            log_user_action(
                user=user,
                action="Creación de Imagen",
                details=f"Se creó una Imagen {data.id} .",
                request=self.request,
                category_name="Imagen",
                metadata=model_to_dict(data)
            )

        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al crear la Imagen o registrar log: {str(e)}",
                level_name="ERROR",
                source="ImagenCustomerViewSet.perform_create",
                category_name="Imagen",
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
                action="Actualización de Imagen",
                details=f"Se actualizó la Imagen {data.id}.",
                request=self.request,
                category_name="Imagen",
                metadata=changes
            )
        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al actualizar la Imagen o registrar log: {str(e)}",
                level_name="ERROR",
                source="ImagenCustomerViewSet.perform_update",
                category_name="Imagen",
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
            action="Eliminación de Imagen",
            details=f"Se eliminó la Imagen: {nombre}.",
            request=self.request,
            category_name="Imagen",
            metadata=data
        )

        try:
            instance.delete()
            log_user_action(
                user=self.request.user,
                action="Eliminación de Imagen",
                details=f"Se eliminó la Imagen: {nombre}.",
                request=self.request,
                category_name="Imagen",
                metadata=data
            )

        except Exception as e:
            import traceback
            log_system_event(
                message=f"Error al eliminar la Imagen. {nombre}: {str(e)}",
                level_name="ERROR",
                source="ImagenCustomerViewSet.perform_destroy",
                category_name="Imagen",
                traceback=traceback.format_exc(),
                metadata=data
            )
            raise  # re-lanza el error para que DRF devuelva la respuesta HTTP 500



class ImagenOtherViewSet(viewsets.ModelViewSet):
    serializer_class = ImagenOtherSerializer
    queryset = ImagenOther.objects.all()

    def perform_create(self, serializer):
        try:
            
            data = serializer.save()
            user = self.request.user

            # 2. Intentamos registrar la acción exitosa
            log_user_action(
                user=user,
                action="Creación de Imagen",
                details=f"Se creó una Imagen {data.id} .",
                request=self.request,
                category_name="Imagen",
                metadata=model_to_dict(data)
            )

        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al crear la Imagen o registrar log: {str(e)}",
                level_name="ERROR",
                source="ImagenOtherViewSet.perform_create",
                category_name="Imagen",
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
                action="Actualización de Imagen",
                details=f"Se actualizó la Imagen {data.id}.",
                request=self.request,
                category_name="Imagen",
                metadata=changes
            )
        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al actualizar la Imagen o registrar log: {str(e)}",
                level_name="ERROR",
                source="ImagenOtherViewSet.perform_update",
                category_name="Imagen",
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
            action="Eliminación de Imagen",
            details=f"Se eliminó la Imagen: {nombre}.",
            request=self.request,
            category_name="Imagen",
            metadata=data
        )

        try:
            instance.delete()
            log_user_action(
                user=self.request.user,
                action="Eliminación de Imagen",
                details=f"Se eliminó la Imagen: {nombre}.",
                request=self.request,
                category_name="Imagen",
                metadata=data
            )

        except Exception as e:
            import traceback
            log_system_event(
                message=f"Error al eliminar la Imagen. {nombre}: {str(e)}",
                level_name="ERROR",
                source="ImagenOtherViewSet.perform_destroy",
                category_name="Imagen",
                traceback=traceback.format_exc(),
                metadata=data
            )
            raise  # re-lanza el error para que DRF devuelva la respuesta HTTP 500



class ImagenGuaranteeViewSet(viewsets.ModelViewSet):
    serializer_class = ImagenGuaranteeSerializer
    queryset = ImagenGuarantee.objects.all()

    def perform_create(self, serializer):
        try:
            
            data = serializer.save()
            user = self.request.user

            # 2. Intentamos registrar la acción exitosa
            log_user_action(
                user=user,
                action="Creación de Imagen",
                details=f"Se creó una Imagen {data.id} .",
                request=self.request,
                category_name="Imagen",
                metadata=model_to_dict(data)
            )

        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al crear la Imagen o registrar log: {str(e)}",
                level_name="ERROR",
                source="ImagenGuaranteeViewSet.perform_create",
                category_name="Imagen",
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
                action="Actualización de Imagen",
                details=f"Se actualizó la Imagen {data.id}.",
                request=self.request,
                category_name="Imagen",
                metadata=changes
            )
        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al actualizar la Imagen o registrar log: {str(e)}",
                level_name="ERROR",
                source="ImagenGuaranteeViewSet.perform_update",
                category_name="Imagen",
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
            action="Eliminación de Imagen",
            details=f"Se eliminó la Imagen: {nombre}.",
            request=self.request,
            category_name="Imagen",
            metadata=data
        )

        try:
            instance.delete()
            log_user_action(
                user=self.request.user,
                action="Eliminación de Imagen",
                details=f"Se eliminó la Imagen: {nombre}.",
                request=self.request,
                category_name="Imagen",
                metadata=data
            )

        except Exception as e:
            import traceback
            log_system_event(
                message=f"Error al eliminar la Imagen. {nombre}: {str(e)}",
                level_name="ERROR",
                source="ImagenGuaranteeViewSet.perform_destroy",
                category_name="Imagen",
                traceback=traceback.format_exc(),
                metadata=data
            )
            raise  # re-lanza el error para que DRF devuelva la respuesta HTTP 500

