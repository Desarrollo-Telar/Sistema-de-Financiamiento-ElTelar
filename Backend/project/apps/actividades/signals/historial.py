# signals.py
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.db import models
from apps.actividades.models import ModelHistory
# DECIMAL
from decimal import Decimal, InvalidOperation

from scripts.conversion_datos import model_to_dict, cambios_realizados

def get_audit_user():
    """Obtiene el usuario actual para auditoría de manera segura"""
    try:
        from django.contrib.auth import get_user
        user = get_user(None)
        if user and user.is_authenticated:
            return user
    except Exception as e:
        print(f"Error al obtener usuario para auditoría: {e}")
    
    return None



# signals.py
def register_history(sender, instance, created, **kwargs):
    """Registra en el historial cuando se crea o actualiza un modelo"""
    # Excluir modelos del sistema y el propio ModelHistory para evitar recursión
    excluded_models = [
        'admin.logentry', 
        'contenttypes.contenttype', 
        'sessions.session'
       
    ]
    
    if sender._meta.label_lower in excluded_models:
        return

    action = 'create' if created else 'update'
    
    # Para updates, determinar qué campos cambiaron
    changes = None
    if not created and instance.pk:
        try:
            old_instance = sender.objects.get(pk=instance.pk)
            changes = {}
            for field in instance._meta.fields:
                if field.name in ['_state', 'password']:
                    continue
                    
                old_value = getattr(old_instance, field.name)
                new_value = getattr(instance, field.name)
                
                # Comparar valores serializados
                old_serialized = serialize_value(old_value)
                new_serialized = serialize_value(new_value)
                
                if old_serialized != new_serialized:
                    changes[field.name] = {
                        'old': old_serialized,
                        'new': new_serialized
                    }
        except sender.DoesNotExist:
            changes = None
        except Exception as e:
            # Capturar cualquier error para evitar que falle el guardado principal
            print(f"Error al calcular cambios para historial: {e}")
            changes = None

    try:
        ModelHistory.objects.create(
            content_type=sender._meta.label,
            object_id=instance.pk,
            action=action,
            data=model_to_dict(instance),
            changes=changes,
            user=get_audit_user()
        )
    except Exception as e:
        # Capturar error pero permitir que el guardado principal continúe
        print(f"Error al crear registro de historial: {e}")

def serialize_value(value):
    """Serializa un valor para comparación en el historial de cambios"""
    if value is None:
        return None
    elif hasattr(value, 'isoformat'):  # datetime, date, time
        return value.isoformat()
    elif isinstance(value, Decimal):
        return float(value)
    elif hasattr(value, 'pk'):  # Model instances
        return value.pk
    elif isinstance(value, models.Model):
        return value.pk
    else:
        return value


def delete_history(sender, instance, **kwargs):
    """Registra en el historial cuando se elimina un modelo"""
    if sender._meta.label_lower in ['admin.logentry', 'contenttypes.contenttype', 'sessions.session']:
        return
    
    ModelHistory.objects.create(
        content_type=sender._meta.label,
        object_id=instance.pk,
        action='delete',
        data=model_to_dict(instance),
        user=get_audit_user()
    )

