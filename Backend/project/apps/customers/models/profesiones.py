from django.db import models


class Profession(models.Model):
    codigo_profesion = models.CharField("Codigo de Profesion", max_length=100, null=False, blank=False)
    nombre = models.CharField("Tipo de Profesión",  max_length=100, unique=True)
    creation_date = models.DateTimeField("Fecha de Creación", auto_now_add=True)
    def __str__(self):
        return f'{self.nombre}'

    class Meta:
        verbose_name = "Profesión"
        verbose_name_plural = "Profesiones"
