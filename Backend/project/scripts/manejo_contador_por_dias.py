
# JSON
import json

# OS
import os

# TIEMPO
from datetime import datetime, time
from django.utils.timezone import now



def load_counter(DATA_FILE):
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    else:
        return {"date": "", "count": 0}

def save_counter(data,DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

def ejecutar_max_1_veces_al_dia():
    DATA_FILE = 'function_counter.json'
    data = load_counter(DATA_FILE)
    hoy = datetime.now().strftime('%Y-%m-%d')

    if data["date"] != hoy:
        # Nuevo día: reiniciar contador
        data["date"] = hoy
        data["count"] = 0

    if data["count"] < 1:
        data["count"] += 1
        save_counter(data, DATA_FILE)
        print("✅ Ejecutando función...")
        # Aquí va tu lógica principal
        return True
    else:
        print("⛔ Límite de 1 ejecuciones alcanzado para hoy.")
        return False

