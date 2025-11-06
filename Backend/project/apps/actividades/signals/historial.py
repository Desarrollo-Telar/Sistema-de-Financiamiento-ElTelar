# signals.py
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.db import models
from apps.actividades.models import ModelHistory
# DECIMAL
from decimal import Decimal, InvalidOperation

from scripts.conversion_datos import model_to_dict, cambios_realizados
