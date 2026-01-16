# Serializador
from .serializers import WorkingInformationSerializer, OtherSourcesOfIncomeSerializer, ReferenceSerializer

# API
from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response

# MODELS
from apps.FinancialInformation.models import WorkingInformation, OtherSourcesOfIncome, Reference

# HISTORIAL Y BITACORA
from apps.actividades.utils import log_user_action, log_system_event
from scripts.conversion_datos import model_to_dict, cambios_realizados

import traceback
from rest_framework import status
from rest_framework.exceptions import ValidationError

class WorkingInformationViewSet(viewsets.ModelViewSet):
    serializer_class = WorkingInformationSerializer
    queryset = WorkingInformation.objects.all()

    def perform_create(self, serializer):
        try:
            
            data = serializer.save()
            user = self.request.user

            # 2. Intentamos registrar la acción exitosa
            log_user_action(
                user=user,
                action="Creación de Informacion Laboral",
                details=f"Se creó una Informacion Laboral {data.position} .",
                request=self.request,
                category_name="Informacion Laboral",
                metadata=model_to_dict(data)
            )

        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al crear una informacion laboral o registrar log: {str(e)}",
                level_name="ERROR",
                source="WorkingInformationViewSet.perform_create",
                category_name="Informacion Laboral",
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
                action="Actualización de Informacion Laboral",
                details=f"Se actualizó la informacion laboral: {data.position}.",
                request=self.request,
                category_name="Informacion Laboral",
                metadata=changes
            )
        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al actualizar la informacion laboral o registrar log: {str(e)}",
                level_name="ERROR",
                source="WorkingInformationViewSet.perform_update",
                category_name="Informacion Laboral",
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
        nombre = f'{instance.position}'
        

        log_user_action(
            user=self.request.user,
            action="Eliminación de Informacion Laboral",
            details=f"Se eliminó la informacion laboral: {nombre}.",
            request=self.request,
            category_name="Informacion Laboral",
            metadata=data
        )

        try:
            instance.delete()
            log_user_action(
                user=self.request.user,
                action="Eliminación de Informacion Laboral",
                details=f"Se eliminó la Informacion Laboral: {nombre}.",
                request=self.request,
                category_name="Informacion Laboral",
                metadata=data
            )

        except Exception as e:
            import traceback
            log_system_event(
                message=f"Error al eliminar la Informacion Laboral. {nombre}: {str(e)}",
                level_name="ERROR",
                source="WorkingInformationViewSet.perform_destroy",
                category_name="Informacion Laboral",
                traceback=traceback.format_exc(),
                metadata=data
            )
            raise  # re-lanza el error para que DRF devuelva la respuesta HTTP 500



class OtherSourcesOfIncomeViewSet(viewsets.ModelViewSet):
    serializer_class = OtherSourcesOfIncomeSerializer
    queryset = OtherSourcesOfIncome.objects.all()

    def perform_create(self, serializer):
        try:
            
            data = serializer.save()
            user = self.request.user

            # 2. Intentamos registrar la acción exitosa
            log_user_action(
                user=user,
                action="Creación Otra Fuente De Ingresos",
                details=f"Se creó Otra Fuente De Ingresos {data.source_of_income} .",
                request=self.request,
                category_name="Otra Fuente de Ingresos",
                metadata=model_to_dict(data)
            )

        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al crear otra fuente de ingresos o registrar log: {str(e)}",
                level_name="ERROR",
                source="OtherSourcesOfIncomeViewSet.perform_create",
                category_name="Otra Fuente de Ingresos",
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
                action="Actualización de Otra Fuente de Ingresos",
                details=f"Se actualizó Otra Fuente de Ingresos {data.source_of_income}.",
                request=self.request,
                category_name="Otra Fuente de Ingresos",
                metadata=changes
            )
        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al actualizar otra fuente de ingresos o registrar log: {str(e)}",
                level_name="ERROR",
                source="OtherSourcesOfIncomeViewSet.perform_update",
                category_name="Otra Fuente de Ingresos",
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
        nombre = f'{instance.source_of_income}'
        

        log_user_action(
            user=self.request.user,
            action="Eliminación de Otra Fuente de Ingresos",
            details=f"Se eliminó otra fuente de ingresos: {nombre}.",
            request=self.request,
            category_name="Otra Fuente de Ingresos",
            metadata=data
        )

        try:
            instance.delete()
            log_user_action(
                user=self.request.user,
                action="Eliminación de Otra Fuente de Ingresos",
                details=f"Se eliminó otra fuente de ingresos: {nombre}.",
                request=self.request,
                category_name="Otra Fuente de Ingresos",
                metadata=data
            )

        except Exception as e:
            import traceback
            log_system_event(
                message=f"Error al eliminar otra fuente de ingresos. {nombre}: {str(e)}",
                level_name="ERROR",
                source="OtherSourcesOfIncomeViewSet.perform_destroy",
                category_name="Otra Fuente de Ingresos",
                traceback=traceback.format_exc(),
                metadata=data
            )
            raise  # re-lanza el error para que DRF devuelva la respuesta HTTP 500



class ReferenceViewSet(viewsets.ModelViewSet):
    serializer_class = ReferenceSerializer
    queryset = Reference.objects.all()

    def perform_create(self, serializer):
        try:
            
            data = serializer.save()
            user = self.request.user

            # 2. Intentamos registrar la acción exitosa
            log_user_action(
                user=user,
                action="Creación de Referencia",
                details=f"Se creó una referencia: {data.full_name} .",
                request=self.request,
                category_name="Referencia",
                metadata=model_to_dict(data)
            )

        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al crear una referencia o registrar log: {str(e)}",
                level_name="ERROR",
                source="ReferenceViewSet.perform_create",
                category_name="Referencia",
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
                action="Actualización de Referencia",
                details=f"Se actualizó la referencia {data.full_name}.",
                request=self.request,
                category_name="Referencia",
                metadata=changes
            )
        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al actualizar la referencia o registrar log: {str(e)}",
                level_name="ERROR",
                source="ReferenceViewSet.perform_update",
                category_name="Referencia",
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
        nombre = f'{instance.full_name}'
        

        log_user_action(
            user=self.request.user,
            action="Eliminación de Referencia",
            details=f"Se eliminó la referencia: {nombre}.",
            request=self.request,
            category_name="Referencia",
            metadata=data
        )

        try:
            instance.delete()
            log_user_action(
                user=self.request.user,
                action="Eliminación de Referencia",
                details=f"Se eliminó el Referencia: {nombre}.",
                request=self.request,
                category_name="Referencia",
                metadata=data
            )

        except Exception as e:
            import traceback
            log_system_event(
                message=f"Error al eliminar la Referencia. {nombre}: {str(e)}",
                level_name="ERROR",
                source="ReferenceViewSet.perform_destroy",
                category_name="Referencia",
                traceback=traceback.format_exc(),
                metadata=data
            )
            raise  # re-lanza el error para que DRF devuelva la respuesta HTTP 500

