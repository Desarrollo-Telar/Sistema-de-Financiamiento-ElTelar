# signals.py
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.db import models
from apps.actividades.models import ModelHistory

def get_audit_user():
    """Obtiene el usuario actual para auditoría"""
    from django.contrib.auth import get_user
    try:
        user = get_user(None)
        if user and user.is_authenticated:
            return user
    except:
        pass
    return None

def model_to_dict(instance):
    """Convierte una instancia de modelo a diccionario, excluyendo campos no deseados"""
    exclude_fields = ['_state', 'password']  # Excluir campos internos y sensibles
    data = {}
    for field in instance._meta.fields:
        if field.name in exclude_fields:
            continue
        value = getattr(instance, field.name)
        # Convertir tipos que no son JSON-serializables
        if hasattr(value, 'pk'):
            value = value.pk  # Para ForeignKeys
        elif isinstance(value, models.Model):
            value = value.pk
        data[field.name] = value
    return data

def register_history(sender, instance, created, **kwargs):
    """Registra en el historial cuando se crea o actualiza un modelo"""
    if sender._meta.label_lower in ['admin.logentry', 'contenttypes.contenttype', 'sessions.session']:
        return  # No registrar cambios en modelos del sistema

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
                if old_value != new_value:
                    changes[field.name] = {
                        'old': old_value,
                        'new': new_value
                    }
        except sender.DoesNotExist:
            changes = None

    ModelHistory.objects.create(
        content_type=sender._meta.label,
        object_id=instance.pk,
        action=action,
        data=model_to_dict(instance),
        changes=changes,
        user=get_audit_user()
    )

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

# Conectar las señales a todos los modelos
for model in models.Model.__subclasses__():
    # Solo conectar a modelos que no sean del sistema
    if not model._meta.abstract and not model._meta.proxy:
        post_save.connect(register_history, sender=model)
        pre_delete.connect(delete_history, sender=model)