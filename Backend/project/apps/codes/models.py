from django.db import models

from apps.users.models import User

import random
from django.db.models.signals import pre_save
from django.dispatch import receiver

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
""" 
#Funcion clave para codigos de verificacion
@receiver(pre_save, sender=User)
def set_code_verification(sender, instance, *args, **kwargs):
    num = random.choices('0123456789', k=5)
    code_verification = Code.objects.create(number=num,user=instance)

"""