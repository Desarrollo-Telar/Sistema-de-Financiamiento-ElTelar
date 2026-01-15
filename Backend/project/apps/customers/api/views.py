# Serializador
from .serializers import CustomerSerializer, ImmigrationStatusSerializer, CreditCounselorSerializer, CobranzaSerializer, HistorialCobranzaSerializer

# API
from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response

# Models
from apps.customers.models import Customer, ImmigrationStatus, CreditCounselor, Cobranza, HistorialCobranza

from django.db.models import Q

from django.utils.timezone import datetime

# HISTORIAL Y BITACORA
from apps.actividades.utils import log_user_action, log_system_event
from scripts.conversion_datos import model_to_dict, cambios_realizados

import traceback
from rest_framework import status
from rest_framework.exceptions import ValidationError


class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()

        # Obtener el término de búsqueda opcional
        search_term = self.request.query_params.get('term', '')

        # Obtener el mes de creación opcional
        month = self.request.query_params.get('month', None)
        year = self.request.query_params.get('year', None)

        # Filtrar por término de búsqueda si existe
        if search_term:
            queryset = queryset.filter(
                Q(first_name__icontains=search_term) |
                Q(last_name__icontains=search_term) |
                Q(customer_code__icontains=search_term)
            )

        # Filtrar por mes y año si se proporcionan
        if month and year:
            try:
                # Validar que el mes y el año son valores válidos
                month = int(month)
                year = int(year)
                queryset = queryset.filter(
                    created_at__year=year,
                    created_at__month=month
                )
            except ValueError:
                # Si los valores no son válidos, se ignora el filtro de mes/año
                pass

        return queryset

    def perform_create(self, serializer):
        try:
            
            cliente = serializer.save()
            user = self.request.user

            # 2. Intentamos registrar la acción exitosa
            log_user_action(
                user=user,
                action="Creación de Cliente",
                details=f"Se creó el cliente con nombre {cliente.first_name} {cliente.last_name}.",
                request=self.request,
                category_name="Clientes",
                metadata=model_to_dict(cliente)
            )

        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al crear cliente o registrar log: {str(e)}",
                level_name="ERROR",
                source="CustomerViewSet.perform_create",
                category_name="Clientes",
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
                action="Actualización de Cliente",
                details=f"Se actualizó el cliente con codigo cliente {data.customer_code}.",
                request=self.request,
                category_name="Clientes",
                metadata=changes
            )
        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al actualizar cliente o registrar log: {str(e)}",
                level_name="ERROR",
                source="CustomerViewSet.perform_update",
                category_name="Clientes",
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
        nombre = f'{instance.first_name} {instance.last_name}'
        

        log_user_action(
            user=self.request.user,
            action="Eliminación de Cliente",
            details=f"Se eliminó el cliente {nombre}.",
            request=self.request,
            category_name="Clientes",
            metadata=data
        )

        try:
            instance.delete()
            log_user_action(
                user=self.request.user,
                action="Eliminación de Cliente",
                details=f"Se eliminó el cliente {nombre}.",
                request=self.request,
                category_name="Clientes",
                metadata=data
            )

        except Exception as e:
            import traceback
            log_system_event(
                message=f"Error al eliminar el cliente {nombre}: {str(e)}",
                level_name="ERROR",
                source="CustomerViewSet.perform_destroy",
                category_name="Clientes",
                traceback=traceback.format_exc(),
                metadata=data
            )
            raise  # re-lanza el error para que DRF devuelva la respuesta HTTP 500



class CustomerAcceptViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.filter(status='Aprobado')

    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.query_params.get('term', '')  # Obtener el parámetro 'term'
        if search_term:
            queryset = queryset.filter(
                Q(first_name__icontains=search_term) |
                Q(last_name__icontains=search_term) |
                Q(customer_code__icontains=search_term)
                ) # Filtrar por el término de búsqueda
        return queryset
    
    def perform_create(self, serializer):
        try:
            
            cliente = serializer.save()
            user = self.request.user

            # 2. Intentamos registrar la acción exitosa
            log_user_action(
                user=user,
                action="Creación de Cliente",
                details=f"Se creó el cliente con nombre {cliente.first_name} {cliente.last_name}.",
                request=self.request,
                category_name="Clientes",
                metadata=model_to_dict(cliente)
            )

        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al crear cliente o registrar log: {str(e)}",
                level_name="ERROR",
                source="CustomerViewSet.perform_create",
                category_name="Clientes",
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
                action="Actualización de Cliente",
                details=f"Se actualizó el cliente con codigo cliente {data.customer_code}.",
                request=self.request,
                category_name="Clientes",
                metadata=changes
            )
        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al actualizar cliente o registrar log: {str(e)}",
                level_name="ERROR",
                source="CustomerViewSet.perform_update",
                category_name="Clientes",
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
        nombre = f'{instance.first_name} {instance.last_name}'
        

        log_user_action(
            user=self.request.user,
            action="Eliminación de Cliente",
            details=f"Se eliminó el cliente {nombre}.",
            request=self.request,
            category_name="Clientes",
            metadata=data
        )

        try:
            instance.delete()
            log_user_action(
                user=self.request.user,
                action="Eliminación de Cliente",
                details=f"Se eliminó el cliente {nombre}.",
                request=self.request,
                category_name="Clientes",
                metadata=data
            )

        except Exception as e:
            import traceback
            log_system_event(
                message=f"Error al eliminar el cliente {nombre}: {str(e)}",
                level_name="ERROR",
                source="CustomerViewSet.perform_destroy",
                category_name="Clientes",
                traceback=traceback.format_exc(),
                metadata=data
            )
            raise  # re-lanza el error para que DRF devuelva la respuesta HTTP 500



class ImmigrationStatusViewSet(viewsets.ModelViewSet):
    serializer_class = ImmigrationStatusSerializer
    queryset = ImmigrationStatus.objects.all()

    def perform_create(self, serializer):
        try:
            
            data = serializer.save()
            user = self.request.user

            # 2. Intentamos registrar la acción exitosa
            log_user_action(
                user=user,
                action="Creación de Condicion Migratoria",
                details=f"Se creó la condicion migratoria {data.condition_name} .",
                request=self.request,
                category_name="Condicion Migratoria",
                metadata=model_to_dict(data)
            )

        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al crear la condicion migratoria o registrar log: {str(e)}",
                level_name="ERROR",
                source="ImmigrationStatusViewSet.perform_create",
                category_name="Condicion Migratoria",
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
                action="Actualización de Condicion Migratoria",
                details=f"Se actualizó la condicion migratoria {data.condition_name}.",
                request=self.request,
                category_name="Condicion Migratoria",
                metadata=changes
            )
        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al actualizar la condicion migratoria o registrar log: {str(e)}",
                level_name="ERROR",
                source="ImmigrationStatusViewSet.perform_update",
                category_name="Condicion Migratoria",
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
        nombre = f'{instance.condition_name}'
        

        log_user_action(
            user=self.request.user,
            action="Eliminación de Condicion Migratoria",
            details=f"Se eliminó la condicion migratoria: {nombre}.",
            request=self.request,
            category_name="Condicion Migratoria",
            metadata=data
        )

        try:
            instance.delete()
            log_user_action(
                user=self.request.user,
                action="Eliminación de Condicion Migratoria",
                details=f"Se eliminó la condicion migratoria: {nombre}.",
                request=self.request,
                category_name="Condicion Migratoria",
                metadata=data
            )

        except Exception as e:
            import traceback
            log_system_event(
                message=f"Error al eliminar la condicion migratoria. {nombre}: {str(e)}",
                level_name="ERROR",
                source="ImmigrationStatusViewSet.perform_destroy",
                category_name="Condicion Migratoria",
                traceback=traceback.format_exc(),
                metadata=data
            )
            raise  # re-lanza el error para que DRF devuelva la respuesta HTTP 500



class HistorialCobranzaViewSet(viewsets.ModelViewSet):
    serializer_class = HistorialCobranzaSerializer
    queryset = HistorialCobranza.objects.all()

    def perform_create(self, serializer):
        try:
            
            data = serializer.save()
            user = self.request.user

            # 2. Intentamos registrar la acción exitosa
            log_user_action(
                user=user,
                action="Creación de Historial de  Cobranza",
                details=f"Se creó el registro de un historial de Cobranza {data.cobranza} .",
                request=self.request,
                category_name="Historial de Cobranza",
                metadata=model_to_dict(data)
            )

        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al crear el historial de cobranza o registrar log: {str(e)}",
                level_name="ERROR",
                source="HistorialCobranzaViewSet.perform_create",
                category_name="Historial de Cobranza",
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
                action="Actualización de Historial de Cobranza",
                details=f"Se actualizó el historial de cobranza. {data.cobranza}.",
                request=self.request,
                category_name="Historial de Cobranza",
                metadata=changes
            )
        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al actualizar el historial de cobranza o registrar log: {str(e)}",
                level_name="ERROR",
                source="HistorialCobranzaViewSet.perform_update",
                category_name="Historial de Cobranza",
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
        nombre = f'{instance.cobranza}'
        

        log_user_action(
            user=self.request.user,
            action="Eliminación de Historial de Cobranza",
            details=f"Se eliminó el historial de cobranza: {nombre}.",
            request=self.request,
            category_name="Historial de Cobranza",
            metadata=data
        )

        try:
            instance.delete()
            log_user_action(
                user=self.request.user,
                action="Eliminación de Historial de Cobranza",
                details=f"Se eliminó el historial de cobranza: {nombre}.",
                request=self.request,
                category_name="Historial de Cobranza",
                metadata=data
            )


        except Exception as e:
            import traceback
            log_system_event(
                message=f"Error al eliminar el historial de cobranza. {nombre}: {str(e)}",
                level_name="ERROR",
                source="HistorialCobranzaViewSet.perform_destroy",
                category_name="Historial de Cobranza",
                traceback=traceback.format_exc(),
                metadata=data
            )
            raise  # re-lanza el error para que DRF devuelva la respuesta HTTP 500



class CreditCounselorSerializerViewSet(viewsets.ModelViewSet):
    serializer_class = CreditCounselorSerializer

    queryset = CreditCounselor.objects.filter(status=True)

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        request = self.request
        search_term = self.request.query_params.get('term', '')  # Obtener el parámetro 'term'

        # obteniendo la sucursal del usuario
        sucursal = getattr(request,'sucursal_actual',None)

        

        if sucursal:
            queryset = queryset.filter(Q(sucursal=sucursal)| Q(sucursal__isnull=True))


        if search_term:
            queryset = queryset.filter(
                Q(nombre__icontains=search_term) |
                Q(apellido__icontains=search_term) |
                Q(codigo_asesor__icontains=search_term) |
                Q(sucursal__isnull=True)
                )# Filtrar por el término de búsqueda
            
        return queryset
    
    def perform_create(self, serializer):
        try:
            
            data = serializer.save()
            user = self.request.user

            # 2. Intentamos registrar la acción exitosa
            log_user_action(
                user=user,
                action="Creación de Asesor de Credito",
                details=f"Se creó un Asesor de Credito {data.usuario} .",
                request=self.request,
                category_name="Asesor de Credito",
                metadata=model_to_dict(data)
            )

        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al crear un asesor de Credito o registrar log: {str(e)}",
                level_name="ERROR",
                source="CreditCounselorSerializerViewSet.perform_create",
                category_name="Asesor de Credito",
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
                action="Actualización de Asesor de Credito",
                details=f"Se actualizó el Asesor de Credito {data.usuario}.",
                request=self.request,
                category_name="Asesor de Credito",
                metadata=changes
            )
        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al actualizar al asesor de credito o registrar log: {str(e)}",
                level_name="ERROR",
                source="CreditCounselorSerializerViewSet.perform_update",
                category_name="Asesor de Credito",
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
        nombre = f'{instance.usuario}'
        

        log_user_action(
            user=self.request.user,
            action="Eliminación de Asesor de Credito",
            details=f"Se eliminó el asesor de Credito: {nombre}.",
            request=self.request,
            category_name="Asesor de Credito",
            metadata=data
        )

        try:
            instance.delete()
            log_user_action(
                user=self.request.user,
                action="Eliminación de Asesor de Credito",
                details=f"Se eliminó el asesor de Credito: {nombre}.",
                request=self.request,
                category_name="Asesor de Credito",
                metadata=data
            )

        except Exception as e:
            import traceback
            log_system_event(
                message=f"Error al eliminar al asesor de credito. {nombre}: {str(e)}",
                level_name="ERROR",
                source="CreditCounselorSerializerViewSet.perform_destroy",
                category_name="Asesor de Credito",
                traceback=traceback.format_exc(),
                metadata=data
            )
            raise  # re-lanza el error para que DRF devuelva la respuesta HTTP 500


class CobranzaViewSet(viewsets.ModelViewSet):
    serializer_class = CobranzaSerializer

    def get_queryset(self):
        asesor_autenticado = CreditCounselor.objects.filter(usuario=self.request.user).first()

        if not asesor_autenticado:
            return Cobranza.objects.none()

        queryset = Cobranza.objects.filter(asesor_credito=asesor_autenticado)

        # Recoger parámetros de búsqueda
        search_term = self.request.query_params.get('term', '').strip()
        user_code = self.request.query_params.get('user_code', '').strip()

        if search_term:
            queryset = queryset.filter(
                Q(credito__customer_id__first_name__icontains=search_term) |
                Q(credito__customer_id__last_name__icontains=search_term) |
                Q(credito__codigo_credito__icontains=search_term) 
            )

        if user_code:            
            asesor_autenticado = CreditCounselor.objects.filter(usuario__user_code=user_code).first()
            queryset = Cobranza.objects.filter(asesor_credito=asesor_autenticado)

        return queryset

    def perform_create(self, serializer):
        try:
            
            data = serializer.save()
            user = self.request.user

            # 2. Intentamos registrar la acción exitosa
            log_user_action(
                user=user,
                action="Creación de Cobranza",
                details=f"Se creó una cobranza {data.credito} .",
                request=self.request,
                category_name="Cobranza",
                metadata=model_to_dict(data)
            )

        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al crear la cobranza o registrar log: {str(e)}",
                level_name="ERROR",
                source="CobranzaViewSet.perform_create",
                category_name="Cobranza",
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
                action="Actualización de Cobranza",
                details=f"Se actualizó la cobranza {data.credito}.",
                request=self.request,
                category_name="Cobranza",
                metadata=changes
            )
        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al actualizar la cobranza o registrar log: {str(e)}",
                level_name="ERROR",
                source="CobranzaViewSet.perform_update",
                category_name="Cobranza",
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
        nombre = f'{instance.credito}'
        

        log_user_action(
            user=self.request.user,
            action="Eliminación de Cobranza",
            details=f"Se eliminó la cobranza: {nombre}.",
            request=self.request,
            category_name="Cobranza",
            metadata=data
        )

        try:
            instance.delete()
            log_user_action(
                user=self.request.user,
                action="Eliminación de Cobranza",
                details=f"Se eliminó la cobranza: {nombre}.",
                request=self.request,
                category_name="Cobranza",
                metadata=data
            )

        except Exception as e:
            import traceback
            log_system_event(
                message=f"Error al eliminar la cobranza. {nombre}: {str(e)}",
                level_name="ERROR",
                source="CobranzaViewSet.perform_destroy",
                category_name="Cobranza",
                traceback=traceback.format_exc(),
                metadata=data
            )
            raise  # re-lanza el error para que DRF devuelva la respuesta HTTP 500

