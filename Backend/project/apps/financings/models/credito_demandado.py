
from django.db import models
from math import floor


# FORMATO
from apps.financings.formato import formatear_numero
from decimal import Decimal

# TIEMPO
from datetime import datetime, date
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.db.models import Q

class CategoriaCreditoDemandado(models.Model):
    titulo = models.CharField("Titulo", max_length=150) 
    descripcion = models.TextField("Descripcion", blank=True, null=True)
    creation_date = models.DateTimeField("Fecha de Creación", auto_now_add=True)

    def __str__(self):
        return self.titulo
    