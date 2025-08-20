
# JSON
import json

# OS
import os

# TIEMPO
from datetime import datetime, time, date
from django.utils.timezone import now

# Modelo
from apps.actividades.models import Checkpoint

def load_counter(DATA_FILE):
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    else:
        return {"date": "", "count": 0}

def save_counter(data,DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)




def ejecutar_max_1_veces_al_dia(reason=None):
    hoy = date.today()
    # Buscar checkpoint de hoy
    checkpoint, created = Checkpoint.objects.get_or_create(
        date=hoy,
        defaults={"count": 0, "reason": reason}
    )

    if checkpoint.count < 1:
        checkpoint.count += 1
        if reason:  # actualizar motivo si lo mandas
            checkpoint.reason = reason
        checkpoint.save()
        print("✅ Ejecutando función...")
        # Aquí va tu lógica principal
        return True
    else:
        print("⛔ Límite de 1 ejecución alcanzado para hoy.")
        return False


