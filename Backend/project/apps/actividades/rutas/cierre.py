
# PATH
from django.urls import path, include

# VIEWS
from apps.actividades import views

# Decorador
from django.contrib.auth.decorators import login_required

urlpatterns_cierre = [
    path('cierre_diario/', login_required(views.listar_cierre_diario), name='listar_cierres'),
    
]