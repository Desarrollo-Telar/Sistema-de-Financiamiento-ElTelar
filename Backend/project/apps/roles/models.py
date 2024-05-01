from django.db import models

# Create your models here.
class Role(models.Model):
    roles = [
        ('Administrador', 'Administrador'),
        ('Contabilidad', 'Contabilidad'),
        ('Secretaria', 'Secretaria'),
        ('Programador', 'Programador')
    ]
    role_name = models.CharField(choices=roles, max_length=75)
    description = models.TextField()

    def __str__(self):
        return self.role_name