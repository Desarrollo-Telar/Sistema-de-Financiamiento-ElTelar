
from django.db import models
condition = [
        ('Residente temporal','Residente temporal'),
        ('Turista o visitante','Turista o visitante'),
        ('Residente permanente','Residente permanente'),
        ('Permiso de trabajo','Permiso de trabajo'),
        ('Persona en tránsito','Persona en tránsito'),
        ('Permiso consular o similar','Permiso consular o similar'),
        ('Otra','Otra'),
    ]


class ImmigrationStatus(models.Model):
    condition_name = models.CharField(max_length=50, blank=False, null=False, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.condition_name

    class Meta:
        verbose_name = "Condicion Migratoria"
        verbose_name_plural = "Condiciones Migratorias"