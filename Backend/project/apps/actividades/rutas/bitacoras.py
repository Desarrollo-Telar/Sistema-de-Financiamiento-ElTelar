
# PATH
from django.urls import path, include

# VIEWS
from apps.actividades import views

# Decorador
from django.contrib.auth.decorators import login_required

urlpatterns_historial = [
    path('historial/', login_required(views.historial), name='listar_historial'),
    
]