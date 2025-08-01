# PATH
from django.urls import path, include

# API
from apps.actividades.api import routers

# Decorador
from django.contrib.auth.decorators import login_required

# VIEWS
from . import views

# RUTAS
from .rutas import urlpatterns_notificaciones

app_name = 'actividades'

urlpatterns = []

urlpatterns+=routers.urlpatterns + urlpatterns_notificaciones