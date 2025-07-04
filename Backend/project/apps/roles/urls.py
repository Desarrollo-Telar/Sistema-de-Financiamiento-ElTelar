# URL
from django.urls import path, include

# Views
from . import views

# Decorador
from django.contrib.auth.decorators import login_required

# API
from apps.roles.api import routers

app_name = 'roles_permisos'

urlpatterns = [
    path('asignacion/<int:user_id>/', views.asignacion_permisos, name='asignacion_permisos'),
    path('guardar-permisos/<int:user_id>/', views.guardar_permisos_usuario, name='guardar_permisos_usuario'),
    
]

urlpatterns += routers.urlpatterns