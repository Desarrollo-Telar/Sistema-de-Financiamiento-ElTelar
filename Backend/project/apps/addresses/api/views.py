from rest_framework import generics

# Serializador
from .serializers import AddressSerializaer, MunicipioSerializaer, DepartamentoSerializaer

# API
from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response

# Model
from apps.addresses.models import Address, Municiopio, Departamento

# HISTORIAL Y BITACORA
from apps.actividades.utils import log_user_action, log_system_event
from scripts.conversion_datos import model_to_dict, cambios_realizados

class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializaer
    queryset = Address.objects.all()

    def perform_create(self, serializer):
        direccion = serializer.save()
        user = self.request.user
        
        log_user_action(
            user=user,
            action="Creación de Direccion",
            details=f"Se creó la dirección de  {direccion.type_address}.",
            request=self.request,
            category_name="Direccion",
            metadata=model_to_dict(direccion)
        )
    
    def perform_update(self, serializer):
        instance = self.get_object()
        previous_data = model_to_dict(instance)
        direccion = serializer.save()
        new_data = model_to_dict(direccion)

        changes = {
            "antes": previous_data,
            "despues": new_data
        }

        log_user_action(
            user=self.request.user,
            action="Actualización de Direccion",
            details=f"Se actualizó la direccion {direccion.id}.",
            request=self.request,
            category_name="Direccion",
            metadata=changes
        )
    
    def perform_destroy(self, instance):
        direccion_data = model_to_dict(instance)
        

        log_user_action(
            user=self.request.user,
            action="Eliminación de Dirección",
            details=f"Se eliminó la dirección {instance.id}",
            request=self.request,
            category_name="Direccion",
            metadata=direccion_data
        )

        try:
            instance.delete()
            log_user_action(
                user=self.request.user,
                action="Eliminación de Direccion",
                details=f"Se eliminó la dirección {instance.id}",
                request=self.request,
                category_name="Direccion",
                metadata=direccion_data
            )

        except Exception as e:
            import traceback
            log_system_event(
                message=f"Error al eliminar la direccion {instance.id}: {str(e)}",
                level_name="ERROR",
                source="AddressViewSet.perform_destroy",
                category_name="Direccion",
                traceback=traceback.format_exc(),
                metadata=direccion_data
            )
            raise  


class MunicipioViewSet(viewsets.ModelViewSet):
    serializer_class = MunicipioSerializaer
    queryset = Municiopio.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.query_params.get('term', '')  # Obtener el parámetro 'term'
        if search_term:
            queryset = queryset.filter(nombre__icontains=search_term)  # Filtrar por el término de búsqueda
        return queryset

    def perform_create(self, serializer):
        municipio = serializer.save()
        user = self.request.user
        
        log_user_action(
            user=user,
            action="Creación de Municipio",
            details=f"Se creó el siguiente municipio {municipio.nombre}.",
            request=self.request,
            category_name="Direccion",
            metadata=model_to_dict(municipio)
        )
    
    def perform_update(self, serializer):
        instance = self.get_object()
        previous_data = model_to_dict(instance)
        direccion = serializer.save()
        new_data = model_to_dict(direccion)

        changes = {
            "antes": previous_data,
            "despues": new_data
        }

        log_user_action(
            user=self.request.user,
            action="Actualización de Municipio",
            details=f"Se actualizó el municipio {direccion.nombre}.",
            request=self.request,
            category_name="Direccion",
            metadata=changes
        )
    
    def perform_destroy(self, instance):
        direccion_data = model_to_dict(instance)
        

        log_user_action(
            user=self.request.user,
            action="Eliminación de Municipio",
            details=f"Se eliminó el municipio {instance.nombre}",
            request=self.request,
            category_name="Direccion",
            metadata=direccion_data
        )

        try:
            instance.delete()
            log_user_action(
                user=self.request.user,
                action="Eliminación de Municipio",
                details=f"Se eliminó el municipio {instance.nombre}",
                request=self.request,
                category_name="Direccion",
                metadata=direccion_data
            )

        except Exception as e:
            import traceback
            log_system_event(
                message=f"Error al eliminar el municipio {instance.id}: {str(e)}",
                level_name="ERROR",
                source="MunicipioViewSet.perform_destroy",
                category_name="Direccion",
                traceback=traceback.format_exc(),
                metadata=direccion_data
            )
            raise  



class DepartamentoViewSet(viewsets.ModelViewSet):
    serializer_class = DepartamentoSerializaer
    queryset = Departamento.objects.all()
    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.query_params.get('term', '')  # Obtener el parámetro 'term'
        if search_term:
            queryset = queryset.filter(nombre__icontains=search_term)  # Filtrar por el término de búsqueda
        return queryset

    def perform_create(self, serializer):
        municipio = serializer.save()
        user = self.request.user
        
        log_user_action(
            user=user,
            action="Creación de Departamento",
            details=f"Se creó el siguiente departamento {municipio.nombre}.",
            request=self.request,
            category_name="Direccion",
            metadata=model_to_dict(municipio)
        )
    
    def perform_update(self, serializer):
        instance = self.get_object()
        previous_data = model_to_dict(instance)
        direccion = serializer.save()
        new_data = model_to_dict(direccion)

        changes = {
            "antes": previous_data,
            "despues": new_data
        }

        log_user_action(
            user=self.request.user,
            action="Actualización de Departamento",
            details=f"Se actualizó el departamento {direccion.nombre}.",
            request=self.request,
            category_name="Direccion",
            metadata=changes
        )
    
    def perform_destroy(self, instance):
        direccion_data = model_to_dict(instance)
        

        log_user_action(
            user=self.request.user,
            action="Eliminación de Departamento",
            details=f"Se eliminó el Departamento {instance.nombre}",
            request=self.request,
            category_name="Direccion",
            metadata=direccion_data
        )

        try:
            instance.delete()
            log_user_action(
                user=self.request.user,
                action="Eliminación de Departamento",
                details=f"Se eliminó el Departamento {instance.nombre}",
                request=self.request,
                category_name="Direccion",
                metadata=direccion_data
            )

        except Exception as e:
            import traceback
            log_system_event(
                message=f"Error al eliminar el Departamento {instance.id}: {str(e)}",
                level_name="ERROR",
                source="DepartamentoViewSet.perform_destroy",
                category_name="Direccion",
                traceback=traceback.format_exc(),
                metadata=direccion_data
            )
            raise  

