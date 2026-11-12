from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone

from apps.InvestmentPlan.models import Acta


@receiver(pre_save, sender=Acta)
def asignar_numero_acta(sender, instance, raw=False, **kwargs):
    if raw or not instance._state.adding or instance.numero_acta:
        return

    year = timezone.localdate().year
    counter = 1

    while True:
        numero = f"{counter}-{year}"

        if not sender.objects.filter(numero_acta=numero).exists():
            instance.numero_acta = numero
            break

        counter += 1