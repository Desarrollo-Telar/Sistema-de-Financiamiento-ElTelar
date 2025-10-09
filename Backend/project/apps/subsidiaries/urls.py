# URL
from django.urls import path, include

# Views
from . import views

# Decorador
from django.contrib.auth.decorators import login_required

app_name = 'sucursal'

urlpatterns = [
    path('clasificacion/',views.view_clasificacion ,name='clasificacion'),
    path('seleccionado/<int:id>/',views.view_seleccionado ,name='seleccionado'),
]