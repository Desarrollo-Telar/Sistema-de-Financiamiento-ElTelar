
# ...abs
from django.shortcuts import render, get_object_or_404, redirect

# Paginacion
from project.pagination import paginacion

# Tiempo
from datetime import datetime

# Modelos
from apps.financings.models import Recibo

# Manejo de mensajes
from django.contrib import messages

# Manejador de filtros
from django.db.models import Q

def reportes_sobre_mora(request):
    pass
"""
def eventos_por_mes(request):
    # Inicializamos mes y año con los valores actuales
    mes = datetime.now().month
    anio = datetime.now().year

    # Si el formulario ha sido enviado (POST)
    if request.method == 'POST':
        mes = request.POST.get('mes')
        anio = request.POST.get('anio')

        # Si no se proporcionan valores en el formulario, usamos los valores por defecto
        if not mes:
            mes = datetime.now().month
        else:
            mes = int(mes)
        
        if not anio:
            anio = datetime.now().year
        else:
            anio = int(anio)

    # Filtrar los eventos según el mes y año
    eventos = Evento.objects.filter(fecha_year=anio, fecha_month=mes)

    return render(request, 'eventos/lista_eventos.html', {'eventos': eventos, 'mes': mes, 'anio': anio})

"""