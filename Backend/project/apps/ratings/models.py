from django.db import models

from apps.customers.models import Customer
from apps.users.models import User

# Create your models here.
class Rating(models.Model):
    votos = [
        ('A','A'), # DESDE 100 AL 93
        ('A-','A-'), # DESDE 93 AL 90
        ('B+','B+'), # DESDE 90 AL 87
        ('B','B'), # DESDE 87 AL 83
        ('B-','B-'),# DESDE 83 AL 80
        ('C+','C+'),# DESDE 80 AL 77
        ('C','C'),# DESDE 77 AL 73
        ('C-','C-'),# DESDE 73 AL 70
        ('D+','D+'),# DESDE 70 AL 67
        ('D','D'),# DESDE 67 AL 60
        ('F','F'),# DESDE 60 AL 0
    ]
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False, verbose_name="Usuario votacion")
    cliente = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=False, null=False, verbose_name="Cliente votado")
    calificacion = models.CharField("Calificacion", max_length=75)
    descripcion = models.TextField("Descripcion", blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Calificacion'
        verbose_name_plural = 'Calificaciones'