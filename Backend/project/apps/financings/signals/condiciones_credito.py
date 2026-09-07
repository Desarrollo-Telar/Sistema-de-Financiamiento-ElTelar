from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from apps.financings.models import CondicionesCredito

from apps.financings.func import cuota
from apps.financings.models import Credit

@receiver(pre_save, sender=CondicionesCredito)
def validar_reglas_unicas_credito(sender, instance, **kwargs):
    # Solo validamos si la regla seleccionada es una de las restrictivas
    reglas_restringidas = ['INTERES FIJO', 'CAPITAL FIJO']
    
    if instance.reglas in reglas_restringidas:
        # Buscamos registros existentes para el mismo crédito y la misma regla
        queryset = CondicionesCredito.objects.filter(
            credit=instance.credit,
            reglas=instance.reglas
        )
        
        # Si el objeto ya existe (actualización), lo excluimos de la búsqueda
        if instance.pk:
            queryset = queryset.exclude(pk=instance.pk)
            
        if queryset.exists():
            raise ValidationError(
                f"El crédito ya cuenta con un registro para la regla '{instance.reglas}'."
            )


@receiver(post_save, sender=CondicionesCredito)
def actualizar_cuota_al_guardar_condicion(sender, instance, created, **kwargs):
    # 1. Obtener la cuota activa del crédito
    cuota_actual = cuota(instance.credit)
    
    if cuota_actual:
        # 2. Verificar el tipo de regla y actualizar el campo correspondiente
        if instance.reglas == 'INTERES FIJO':
            cuota_actual.interest = instance.monto
            cuota_actual.save()
            
        elif instance.reglas == 'CAPITAL FIJO':
            cuota_actual.principal = instance.monto
            cuota_actual.save()


@receiver(post_delete, sender=CondicionesCredito)
def recalcular_cuota_al_eliminar_condicion(sender, instance, **kwargs):
    """
    Opcional: Si eliminas la condición desde la interfaz,
    recalcula el valor dinámico original en la cuota actual.
    """
    cuota_actual = cuota(instance.credit)
    
    if cuota_actual:
        if instance.reglas == 'INTERES FIJO':
            cuota_actual.interest = cuota_actual.calculo_interes()
            cuota_actual.save()
            
        elif instance.reglas == 'CAPITAL FIJO':
            cuota_actual.principal = cuota_actual.calculo_capital()
            cuota_actual.save()