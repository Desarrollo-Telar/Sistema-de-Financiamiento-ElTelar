# Serializador
from apps.financings.api.serializers import  PaymentPlanSerializer, PaymentPlanSerializerSeguro,PaymentPlanSerializerAcreedor
# MODELS
from apps.financings.models import PaymentPlan

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

class PaymentPlanViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentPlanSerializer
    queryset = PaymentPlan.objects.all()

    def perform_create(self, serializer):
        try:
            
            data = serializer.save()
            user = self.request.user

            # 2. Intentamos registrar la acción exitosa
            log_user_action(
                user=user,
                action="Creación de Cuota",
                details=f"Se creó una cuota {data.id} .",
                request=self.request,
                category_name="Cuotas",
                metadata=model_to_dict(data)
            )

        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al crear la cuota o registrar log: {str(e)}",
                level_name="ERROR",
                source="PaymentPlanViewSet.perform_create",
                category_name="Cuotas",
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
                action="Actualización de Cuota",
                details=f"Se actualizó la cuota {data.id}.",
                request=self.request,
                category_name="Cuotas",
                metadata=changes
            )
        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al actualizar la cuota o registrar log: {str(e)}",
                level_name="ERROR",
                source="PaymentPlanViewSet.perform_update",
                category_name="Cuotas",
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
            action="Eliminación de Cuota",
            details=f"Se eliminó la cuota: {nombre}.",
            request=self.request,
            category_name="Cuotas",
            metadata=data
        )

        try:
            instance.delete()
            log_user_action(
                user=self.request.user,
                action="Eliminación de Cuota",
                details=f"Se eliminó la cuota: {nombre}.",
                request=self.request,
                category_name="Cuotas",
                metadata=data
            )

        except Exception as e:
            import traceback
            log_system_event(
                message=f"Error al eliminar la cuota. {nombre}: {str(e)}",
                level_name="ERROR",
                source="PaymentPlanViewSet.perform_destroy",
                category_name="Cuotas",
                traceback=traceback.format_exc(),
                metadata=data
            )
            raise  # re-lanza el error para que DRF devuelva la respuesta HTTP 500




class PaymentPlanUltimoViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentPlanSerializer
    queryset = PaymentPlan.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.query_params.get('term', '')  # Obtener el parámetro 'term'

        if search_term:
            queryset = PaymentPlan.filter(
                Q(id__icontains=search_term) 
            ).first()


        
        return queryset 
    
    def perform_create(self, serializer):
        try:
            
            data = serializer.save()
            user = self.request.user

            # 2. Intentamos registrar la acción exitosa
            log_user_action(
                user=user,
                action="Creación de Cuota",
                details=f"Se creó una cuota {data.id} .",
                request=self.request,
                category_name="Cuotas",
                metadata=model_to_dict(data)
            )

        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al crear la cuota o registrar log: {str(e)}",
                level_name="ERROR",
                source="PaymentPlanUltimoViewSet.perform_create",
                category_name="Cuotas",
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
                action="Actualización de Cuota",
                details=f"Se actualizó la cuota {data.id}.",
                request=self.request,
                category_name="Cuotas",
                metadata=changes
            )
        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al actualizar la cuota o registrar log: {str(e)}",
                level_name="ERROR",
                source="PaymentPlanUltimoViewSet.perform_update",
                category_name="Cuotas",
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
            action="Eliminación de Cuota",
            details=f"Se eliminó la Cuota: {nombre}.",
            request=self.request,
            category_name="Cuotas",
            metadata=data
        )

        try:
            instance.delete()
            log_user_action(
                user=self.request.user,
                action="Eliminación de Cuota",
                details=f"Se eliminó la Cuota: {nombre}.",
                request=self.request,
                category_name="Cuotas",
                metadata=data
            )

        except Exception as e:
            import traceback
            log_system_event(
                message=f"Error al eliminar la cuota. {nombre}: {str(e)}",
                level_name="ERROR",
                source="PaymentPlanUltimoViewSet.perform_destroy",
                category_name="Cuotas",
                traceback=traceback.format_exc(),
                metadata=data
            )
            raise  # re-lanza el error para que DRF devuelva la respuesta HTTP 500




class PaymentPlanAmpliacion(viewsets.ModelViewSet):
    serializer_class = PaymentPlanSerializer
    queryset = PaymentPlan.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.query_params.get('term', '')  # Obtener el parámetro 'term'

        if search_term:
            dia = datetime.now().date()
            dia_mas_uno = dia + timedelta(days=1)

            siguiente_pago = PaymentPlan.objects.filter(
                credit_id__id=search_term,
                start_date__lte=dia,
                fecha_limite__gte=dia_mas_uno
            ).first()

            if siguiente_pago is None:
                siguiente_pago = PaymentPlan.objects.filter(
                    credit_id__id=search_term
                ).order_by('-id').first()

            if siguiente_pago:
                return PaymentPlan.objects.filter(id=siguiente_pago.id)
            else:
                return PaymentPlan.objects.none()  # Devuelve un queryset vacío

        return queryset
    
    def perform_create(self, serializer):
        try:
            
            data = serializer.save()
            user = self.request.user

            # 2. Intentamos registrar la acción exitosa
            log_user_action(
                user=user,
                action="Creación de Cuota",
                details=f"Se creó una cuota {data.id} .",
                request=self.request,
                category_name="Cuotas",
                metadata=model_to_dict(data)
            )

        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al crear la cuota o registrar log: {str(e)}",
                level_name="ERROR",
                source="PaymentPlanAmpliacion.perform_create",
                category_name="Cuotas",
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
                action="Actualización de Cuota",
                details=f"Se actualizó la cuota {data.id}.",
                request=self.request,
                category_name="Cuotas",
                metadata=changes
            )
        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al actualizar la cuota o registrar log: {str(e)}",
                level_name="ERROR",
                source="PaymentPlanAmpliacion.perform_update",
                category_name="Cuotas",
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
            action="Eliminación de Cuota",
            details=f"Se eliminó la Cuota: {nombre}.",
            request=self.request,
            category_name="Cuotas",
            metadata=data
        )

        try:
            instance.delete()
            log_user_action(
                user=self.request.user,
                action="Eliminación de Cuota",
                details=f"Se eliminó la Cuota: {nombre}.",
                request=self.request,
                category_name="Cuotas",
                metadata=data
            )

        except Exception as e:
            import traceback
            log_system_event(
                message=f"Error al eliminar la cuota. {nombre}: {str(e)}",
                level_name="ERROR",
                source="PaymentPlanAmpliacion.perform_destroy",
                category_name="Cuotas",
                traceback=traceback.format_exc(),
                metadata=data
            )
            raise  # re-lanza el error para que DRF devuelva la respuesta HTTP 500




class PaymentPlanAcreedorUltimoViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentPlanSerializerAcreedor
    queryset = PaymentPlan.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        search_term = self.request.query_params.get('term', '')
        if search_term:
            queryset = queryset.filter(
                Q(id__icontains=search_term) 
            )
        last_item = queryset.order_by('-id').first()
        if last_item:
            serializer = self.get_serializer(last_item)
            return Response(serializer.data)
        return Response([])  # Si no hay datos que coincidan, devolver una lista vacía
    
    def perform_create(self, serializer):
        try:
            
            data = serializer.save()
            user = self.request.user

            # 2. Intentamos registrar la acción exitosa
            log_user_action(
                user=user,
                action="Creación de Cuota",
                details=f"Se creó una cuota {data.id} .",
                request=self.request,
                category_name="Cuotas",
                metadata=model_to_dict(data)
            )

        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al crear la cuota o registrar log: {str(e)}",
                level_name="ERROR",
                source="PaymentPlanAcreedorUltimoViewSet.perform_create",
                category_name="Cuotas",
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
                action="Actualización de Cuota",
                details=f"Se actualizó la cuota {data.id}.",
                request=self.request,
                category_name="Cuotas",
                metadata=changes
            )
        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al actualizar la cuota o registrar log: {str(e)}",
                level_name="ERROR",
                source="PaymentPlanAcreedorUltimoViewSet.perform_update",
                category_name="Cuotas",
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
            action="Eliminación de Cuota",
            details=f"Se eliminó la Cuota: {nombre}.",
            request=self.request,
            category_name="Cuotas",
            metadata=data
        )

        try:
            instance.delete()
            log_user_action(
                user=self.request.user,
                action="Eliminación de Cuota",
                details=f"Se eliminó la Cuota: {nombre}.",
                request=self.request,
                category_name="Cuotas",
                metadata=data
            )

        except Exception as e:
            import traceback
            log_system_event(
                message=f"Error al eliminar la cuota. {nombre}: {str(e)}",
                level_name="ERROR",
                source="PaymentPlanAcreedorUltimoViewSet.perform_destroy",
                category_name="Cuotas",
                traceback=traceback.format_exc(),
                metadata=data
            )
            raise  # re-lanza el error para que DRF devuelva la respuesta HTTP 500




class PaymentPlanSeguroUltimoViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentPlanSerializerSeguro
    queryset = PaymentPlan.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        search_term = self.request.query_params.get('term', '')
        if search_term:
            queryset = queryset.filter(
                Q(seguro__id__icontains=search_term) 
            )
        last_item = queryset.order_by('-id').first()
        if last_item:
            serializer = self.get_serializer(last_item)
            return Response(serializer.data)
        return Response([])  # Si no hay datos que coincidan, devolver una lista vacía
    
    def perform_create(self, serializer):
        try:
            
            data = serializer.save()
            user = self.request.user

            # 2. Intentamos registrar la acción exitosa
            log_user_action(
                user=user,
                action="Creación de Cuota",
                details=f"Se creó una cuota {data.id} .",
                request=self.request,
                category_name="Cuotas",
                metadata=model_to_dict(data)
            )

        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al crear la cuota o registrar log: {str(e)}",
                level_name="ERROR",
                source="PaymentPlanSeguroUltimoViewSet.perform_create",
                category_name="Cuotas",
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
                action="Actualización de Cuota",
                details=f"Se actualizó la cuota {data.id}.",
                request=self.request,
                category_name="Cuotas",
                metadata=changes
            )
        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al actualizar la cuota o registrar log: {str(e)}",
                level_name="ERROR",
                source="PaymentPlanSeguroUltimoViewSet.perform_update",
                category_name="Cuotas",
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
            action="Eliminación de Cuota",
            details=f"Se eliminó la Cuota: {nombre}.",
            request=self.request,
            category_name="Cuotas",
            metadata=data
        )

        try:
            instance.delete()
            log_user_action(
                user=self.request.user,
                action="Eliminación de Cuota",
                details=f"Se eliminó la Cuota: {nombre}.",
                request=self.request,
                category_name="Cuotas",
                metadata=data
            )

        except Exception as e:
            import traceback
            log_system_event(
                message=f"Error al eliminar la cuota. {nombre}: {str(e)}",
                level_name="ERROR",
                source="PaymentPlanSeguroUltimoViewSet.perform_destroy",
                category_name="Cuotas",
                traceback=traceback.format_exc(),
                metadata=data
            )
            raise  # re-lanza el error para que DRF devuelva la respuesta HTTP 500


    