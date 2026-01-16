# SERIALIZADOR
from .serializers import DocumentCustomerSerializer,DocumentGuaranteeSerializer, DocumentOtherSerializer,DocumentSerializer,DocumentAddressSerializer
# MODELS
from apps.documents.models import Document,DocumentAddress,DocumentCustomer,DocumentGuarantee,DocumentOther
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

class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    queryset = Document.objects.all()

    def perform_create(self, serializer):
        try:
            
            data = serializer.save()
            user = self.request.user

            # 2. Intentamos registrar la acción exitosa
            log_user_action(
                user=user,
                action="Creación de Documento",
                details=f"Se creó un documento {data.description} .",
                request=self.request,
                category_name="Documento",
                metadata=model_to_dict(data)
            )

        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al crear el documento o registrar log: {str(e)}",
                level_name="ERROR",
                source="DocumentViewSet.perform_create",
                category_name="Documento",
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
                action="Actualización de Documento",
                details=f"Se actualizó el documento {data.description}.",
                request=self.request,
                category_name="Documento",
                metadata=changes
            )
        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al actualizar el documento o registrar log: {str(e)}",
                level_name="ERROR",
                source="DocumentViewSet.perform_update",
                category_name="Documento",
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
        nombre = f'{instance.description}'
        

        log_user_action(
            user=self.request.user,
            action="Eliminación de Documento",
            details=f"Se eliminó el documento: {nombre}.",
            request=self.request,
            category_name="Documento",
            metadata=data
        )

        try:
            instance.delete()
            log_user_action(
                user=self.request.user,
                action="Eliminación de Documento",
                details=f"Se eliminó el documento: {nombre}.",
                request=self.request,
                category_name="Documento",
                metadata=data
            )

        except Exception as e:
            import traceback
            log_system_event(
                message=f"Error al eliminar el documento. {nombre}: {str(e)}",
                level_name="ERROR",
                source="DocumentViewSet.perform_destroy",
                category_name="Documento",
                traceback=traceback.format_exc(),
                metadata=data
            )
            raise  # re-lanza el error para que DRF devuelva la respuesta HTTP 500



class DocumentAddressViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentAddressSerializer
    queryset = DocumentAddress.objects.all()

    def perform_create(self, serializer):
        try:
            
            data = serializer.save()
            user = self.request.user

            # 2. Intentamos registrar la acción exitosa
            log_user_action(
                user=user,
                action="Creación de Documento",
                details=f"Se creó un documento {data.id} .",
                request=self.request,
                category_name="Documento",
                metadata=model_to_dict(data)
            )

        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al crear el documento o registrar log: {str(e)}",
                level_name="ERROR",
                source="DocumentAddressViewSet.perform_create",
                category_name="Documento",
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
                action="Actualización de Documento",
                details=f"Se actualizó el documento {data.id}.",
                request=self.request,
                category_name="Documento",
                metadata=changes
            )
        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al actualizar el documento o registrar log: {str(e)}",
                level_name="ERROR",
                source="DocumentAddressViewSet.perform_update",
                category_name="Documento",
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
            action="Eliminación de Documento",
            details=f"Se eliminó el documento: {nombre}.",
            request=self.request,
            category_name="Documento",
            metadata=data
        )

        try:
            instance.delete()
            log_user_action(
                user=self.request.user,
                action="Eliminación de Documento",
                details=f"Se eliminó el documento: {nombre}.",
                request=self.request,
                category_name="Documento",
                metadata=data
            )

        except Exception as e:
            import traceback
            log_system_event(
                message=f"Error al eliminar el documento. {nombre}: {str(e)}",
                level_name="ERROR",
                source="DocumentAddressViewSet.perform_destroy",
                category_name="Documento",
                traceback=traceback.format_exc(),
                metadata=data
            )
            raise  # re-lanza el error para que DRF devuelva la respuesta HTTP 500



    

class DocumentCustomerViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentCustomerSerializer
    queryset = DocumentCustomer.objects.all()

    def perform_create(self, serializer):
        try:
            
            data = serializer.save()
            user = self.request.user

            # 2. Intentamos registrar la acción exitosa
            log_user_action(
                user=user,
                action="Creación de Documento",
                details=f"Se creó un documento {data.id} .",
                request=self.request,
                category_name="Documento",
                metadata=model_to_dict(data)
            )

        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al crear el documento o registrar log: {str(e)}",
                level_name="ERROR",
                source="DocumentCustomerViewSet.perform_create",
                category_name="Documento",
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
                action="Actualización de Documento",
                details=f"Se actualizó el documento {data.id}.",
                request=self.request,
                category_name="Documento",
                metadata=changes
            )
        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al actualizar el documento o registrar log: {str(e)}",
                level_name="ERROR",
                source="DocumentCustomerViewSet.perform_update",
                category_name="Documento",
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
            action="Eliminación de Documento",
            details=f"Se eliminó el documento: {nombre}.",
            request=self.request,
            category_name="Documento",
            metadata=data
        )

        try:
            instance.delete()
            log_user_action(
                user=self.request.user,
                action="Eliminación de Documento",
                details=f"Se eliminó el documento: {nombre}.",
                request=self.request,
                category_name="Documento",
                metadata=data
            )

        except Exception as e:
            import traceback
            log_system_event(
                message=f"Error al eliminar el documento. {nombre}: {str(e)}",
                level_name="ERROR",
                source="DocumentCustomerViewSet.perform_destroy",
                category_name="Documento",
                traceback=traceback.format_exc(),
                metadata=data
            )
            raise  # re-lanza el error para que DRF devuelva la respuesta HTTP 500




class DocumentOtherViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentOtherSerializer
    queryset = DocumentOther.objects.all()

    def perform_create(self, serializer):
        try:
            
            data = serializer.save()
            user = self.request.user

            # 2. Intentamos registrar la acción exitosa
            log_user_action(
                user=user,
                action="Creación de Documento",
                details=f"Se creó un documento {data.id} .",
                request=self.request,
                category_name="Documento",
                metadata=model_to_dict(data)
            )

        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al crear el documento o registrar log: {str(e)}",
                level_name="ERROR",
                source="DocumentOtherViewSet.perform_create",
                category_name="Documento",
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
                action="Actualización de Documento",
                details=f"Se actualizó el documento {data.id}.",
                request=self.request,
                category_name="Documento",
                metadata=changes
            )
        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al actualizar el documento o registrar log: {str(e)}",
                level_name="ERROR",
                source="DocumentOtherViewSet.perform_update",
                category_name="Documento",
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
            action="Eliminación de Documento",
            details=f"Se eliminó el documento: {nombre}.",
            request=self.request,
            category_name="Documento",
            metadata=data
        )

        try:
            instance.delete()
            log_user_action(
                user=self.request.user,
                action="Eliminación de Documento",
                details=f"Se eliminó el documento: {nombre}.",
                request=self.request,
                category_name="Documento",
                metadata=data
            )

        except Exception as e:
            import traceback
            log_system_event(
                message=f"Error al eliminar el documento. {nombre}: {str(e)}",
                level_name="ERROR",
                source="DocumentOtherViewSet.perform_destroy",
                category_name="Documento",
                traceback=traceback.format_exc(),
                metadata=data
            )
            raise  # re-lanza el error para que DRF devuelva la respuesta HTTP 500




class DocumentGuaranteeViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentGuaranteeSerializer
    queryset = DocumentGuarantee.objects.all()

    def perform_create(self, serializer):
        try:
            
            data = serializer.save()
            user = self.request.user

            # 2. Intentamos registrar la acción exitosa
            log_user_action(
                user=user,
                action="Creación de Documento",
                details=f"Se creó un documento {data.id} .",
                request=self.request,
                category_name="Documento",
                metadata=model_to_dict(data)
            )

        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al crear el documento o registrar log: {str(e)}",
                level_name="ERROR",
                source="DocumentGuaranteeViewSet.perform_create",
                category_name="Documento",
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
                action="Actualización de Documento",
                details=f"Se actualizó el documento {data.id}.",
                request=self.request,
                category_name="Documento",
                metadata=changes
            )
        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al actualizar el documento o registrar log: {str(e)}",
                level_name="ERROR",
                source="DocumentGuaranteeViewSet.perform_update",
                category_name="Documento",
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
            action="Eliminación de Documento",
            details=f"Se eliminó el documento: {nombre}.",
            request=self.request,
            category_name="Documento",
            metadata=data
        )

        try:
            instance.delete()
            log_user_action(
                user=self.request.user,
                action="Eliminación de Documento",
                details=f"Se eliminó el documento: {nombre}.",
                request=self.request,
                category_name="Documento",
                metadata=data
            )

        except Exception as e:
            import traceback
            log_system_event(
                message=f"Error al eliminar el documento. {nombre}: {str(e)}",
                level_name="ERROR",
                source="DocumentGuaranteeViewSet.perform_destroy",
                category_name="Documento",
                traceback=traceback.format_exc(),
                metadata=data
            )
            raise  # re-lanza el error para que DRF devuelva la respuesta HTTP 500


