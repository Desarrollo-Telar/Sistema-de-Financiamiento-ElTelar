# URL
from django.urls import path, include

# Views
from . import views

# FILTROS

# Decorador
from django.contrib.auth.decorators import login_required

# Routes
from apps.accountings.api import routers


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

    # DETAIL
    path('acreedores/detail/<int:id>', views.detail_acreedores, name='acreedores_detail'),
    path('seguros/detail/<int:id>', views.detail_seguro, name='seguros_detail'),
    path('ingresos/detail/<int:id>', views.detail_ingreso, name='ingresos_detail'),
    path('egresos/detail/<int:id>', views.detail_egreso, name='egresos_detail'),

    # BOLETAS
    path('seguros/boleta', views.add_boleta_seguro, name='seguros_boleta'),
    path('acreedores/boleta', views.add_boleta_acreedor, name='acreedores_boleta'),

    # UPDATE
    path('egresos/update/<int:id>/',views.actualizar_egresos, name='egresos_update'),
    path('ingresos/update/<int:id>/',views.actualizar_ingresos, name='ingresos_update')

    
]

urlpatterns+=routers.urlpatterns