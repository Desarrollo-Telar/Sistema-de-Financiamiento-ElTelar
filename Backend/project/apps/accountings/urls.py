# URL
from django.urls import path, include

# Views
from . import views

# FILTROS

# Decorador
from django.contrib.auth.decorators import login_required

# Routes


app_name = 'contable'

urlpatterns = [
    # LIST
    path('acreedores', views.list_acreedores, name='acreedores'),
    path('seguros', views.list_seguros, name='seguros'),
    path('ingresos', views.list_ingresos, name='ingresos'),
    path('egresos', views.list_egresos, name='egresos'),

    # CREATE
    path('acreedores/create', views.add_acreedor, name='acreedores_create'),
    path('seguros/create', views.add_seguro, name='seguros_create'),
    path('ingresos/create', views.add_ingreso, name='ingresos_create'),
    path('egresos/create', views.add_egresos, name='egresos_create'),

    
]