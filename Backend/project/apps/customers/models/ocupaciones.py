from django.db import models

class Occupation(models.Model):
    codigo_ocupacion = models.CharField("Codigo de Ocupación", max_length=100, null=False, blank=False)
    nombre = models.CharField("Tipo de Ocupación",  max_length=100, unique=True)
    
    def __str__(self):
        return f'{self.nombre}'

    class Meta:
        verbose_name = "Ocupación"
        verbose_name_plural = "Ocupaciones"