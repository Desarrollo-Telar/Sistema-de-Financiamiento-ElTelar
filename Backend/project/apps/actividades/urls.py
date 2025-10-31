# PATH
from django.urls import path, include

# API
from apps.actividades.api import routers

# Decorador
from django.contrib.auth.decorators import login_required

# VIEWS
from . import views

# RUTAS
from .rutas import urlpatterns_notificaciones, urlpatterns_votaciones, urlpatterns_logs , urlpatterns_cierre

app_name = 'actividades'

urlpatterns = []

urlpatterns+=routers.urlpatterns + urlpatterns_notificaciones + urlpatterns_votaciones + urlpatterns_logs + urlpatterns_cierre