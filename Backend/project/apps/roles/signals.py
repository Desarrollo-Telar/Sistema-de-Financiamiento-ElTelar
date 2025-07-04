# SIGNALS
from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.dispatch import receiver

# MODELO
from .models import CategoriaPermiso, Permiso

def recorrido_permisos(instance, estado):
    for permiso in Permiso.objects.filter(categoria_permiso=instance):
        permiso.estado = estado
        permiso.save()

@receiver(post_save, sender=CategoriaPermiso)
def actualizacion_estados_permisos(sender, instance, created, **kwargs):
    if not instance.estado:
        recorrido_permisos(instance, False)
        
    else:
        recorrido_permisos(instance, True)

