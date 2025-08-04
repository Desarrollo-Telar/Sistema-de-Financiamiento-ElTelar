from django.db import models

# RELACION
from apps.users.models import User
from apps.customers.models import Customer
from apps.financings.models import Credit

# Tiempo
from django.utils import timezone

from decimal import Decimal
from django.db.models import Avg
from django.db.models.functions import Coalesce

# Votacion para Cliente
class VotacionCliente(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Usuario Votando")
    cliente = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Cliente Votado")
    puntuacion = models.IntegerField(verbose_name="Puntuacion", blank=True, null=True)
    comentario = models.TextField(verbose_name="Comentario para el cliente", blank=True, null=True)
    creation_date = models.DateTimeField("Fecha de Creación", auto_now_add=True)

    def calcular_promedio_puntuacion(self):
        promedio = VotacionCliente.objects.filter(
            cliente=self.cliente,
            puntuacion__isnull=False
        ).aggregate(prom=Avg('puntuacion'))['prom']

        self.cliente.valoracion = Decimal(promedio) if promedio is not None else Decimal('0.00')
        self.cliente.save()

    def save(self,*args, **kwargs):
        
        super().save(*args, **kwargs)
        self.calcular_promedio_puntuacion()
        

    class Meta:
        verbose_name = "Votacion Para Clientes"
        verbose_name_plural = "Votaciones Para Clientes"


# Votacion para Creditos
class VotacionCredito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Usuario Votando")
    credito = models.ForeignKey(Credit, on_delete=models.CASCADE, verbose_name="Credito Votado")
    puntuacion = models.IntegerField(verbose_name="Puntuacion", blank=True, null=True)
    comentario = models.TextField(verbose_name="Comentario para el Credito", blank=True, null=True)
    creation_date = models.DateTimeField("Fecha de Creación", auto_now_add=True)

    def calcular_promedio_puntuacion(self):
        promedio = VotacionCredito.objects.filter(
            credito=self.credito,
            puntuacion__isnull=False
        ).aggregate(prom=Avg('puntuacion'))['prom']

        self.credito.valoracion = Decimal(promedio) if promedio is not None else Decimal('0.00')
        self.credito.save()

    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)
        self.calcular_promedio_puntuacion()


    class Meta:
        verbose_name = "Votacion Para Credito"
        verbose_name_plural = "Votaciones Para Credito"
