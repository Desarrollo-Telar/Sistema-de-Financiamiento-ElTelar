from django.db import models



# Relacion
from apps.users.models import User
from apps.customers.models import Customer
from apps.financings.models import PaymentPlan

# Signals
from django.db.models.signals import pre_save
from django.dispatch import receiver

# UUID
import uuid

# Random
import random

# Create your models here.
class Code(models.Model):
    number = models.CharField(max_length=5, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


    def __str__(self):
        return str(self.number)
    
    def save(self, *args, **kwargs):
        number_list = [x for x in range(10)]
        code_items = []

        for i in range(5):
            num = random.choice(number_list)
            code_items.append(num)
        
        code_string = "".join(str(item) for item in code_items)
        self.number = code_string
        super().save()
    
    class Meta:
        verbose_name = 'Codigo'
        verbose_name_plural = 'Codigos'

class TokenCliente(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    cliente = models.OneToOneField(Customer, on_delete=models.CASCADE)
    cuota = models.OneToOneField(PaymentPlan, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.uuid} - {self.cliente}'
    
"""#Funcion clave para codigos de verificacion
@receiver(pre_save, sender=User)
def set_code_verification(sender, instance, *args, **kwargs):
    num = random.choices('0123456789', k=5)
    Code.objects.create(number=num,user=instance)"""

