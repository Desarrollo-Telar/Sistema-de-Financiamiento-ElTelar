from django.db import models


class Profession(models.Model):
    codigo_profesion = models.CharField("Codigo de Profesion", max_length=100, null=False, blank=False)
    nombre = models.CharField("Tipo de Profesión",  max_length=100, unique=True)

    def __str__(self):
        return f'{self.nombre}'

    class Meta:
        verbose_name = "Profesión"
        verbose_name_plural = "Profesiones"
