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
    path('',views.list_modulos,name='modulos_contables'),
    path('reports/acreedores/',login_required(views.reportes_generales_acreedores),name='reportes_acreedores'),
    path('reports/seguros/',login_required(views.reportes_generales_seguros),name='reportes_seguros'),
    # LIST
    path('acreedores/', views.AcreedoresListView.as_view(), name='acreedores'),
    path('seguros/', views.SeguroListView.as_view(), name='seguros'),
    path('ingresos/', login_required( views.IngresosList.as_view()), name='ingresos'),
    path('egresos/', login_required(views.EgresosList.as_view()), name='egresos'),

    # CREATE
    path('acreedores/create/', views.add_acreedor, name='acreedores_create'),
    path('seguros/create/', views.add_seguro, name='seguros_create'),
    path('ingresos/create/', views.add_ingreso, name='ingresos_create'),
    path('egresos/create/', views.add_egresos, name='egresos_create'),

    # DETAIL
    path('acreedores/detail/<int:id>/', views.detail_acreedores, name='acreedores_detail'),
    path('seguros/detail/<int:id>/', views.detail_seguro, name='seguros_detail'),
    path('ingresos/detail/<int:id>/', views.detail_ingreso, name='ingresos_detail'),
    path('egresos/detail/<int:id>/', views.detail_egreso, name='egresos_detail'),

    # BOLETAS
    path('seguros/boleta/', views.add_boleta_seguro, name='seguros_boleta'),
    path('acreedores/boleta/', views.add_boleta_acreedor, name='acreedores_boleta'),

    # UPDATE
    path('egresos/update/<int:id>/',views.actualizar_egresos, name='egresos_update'),
    path('ingresos/update/<int:id>/',views.actualizar_ingresos, name='ingresos_update'),


    # SEARCH 
    path('acreedores/search/', views.AcreedoresSearch.as_view(), name='acreedores_search'),
    path('seguros/search/', views.SeguroSearch.as_view(), name='seguros_search'),
    path('ingresos/search/', views.IngresoSearch.as_view(), name='ingresos_search'),
    path('egresos/search/', views.EgresoSearch.as_view(), name='egresos_search'),

    # FILTRO
    path('ingresos/pendiente/', views.pendiente_ingresos_vincular, name='pendiente_ingresos_vincular'),
    path('ingresos/completados/', views.ingresos_vinculados, name='ingresos_vinculados'),

    path('egresos/pendiente/', views.pendiente_egresos_vincular, name='pendiente_egresos_vincular'),
    path('egresos/completados/', views.egresos_vinculados, name='egresos_vinculados'),
    
    path('seguros/seguros_cancelados/',views.seguro_cancelado, name='seguro_cancelado'),
    path('seguros/atraso_en_aportacion/',views.seguros_atraso_aportacion, name='seguros_atraso_aportacion'),
    path('seguros/atraso_por_fechas/',views.seguros_atraso_fechas, name='seguros_atraso_fechas'),

    path('acreedores/acreedores_cancelados/',views.acreedores_cancelado, name='acreedores_cancelado'),
    path('acreedores/atraso_en_aportacion/',views.acreedores_atraso_aportacion, name='acreedores_atraso_aportacion'),
    path('acreedores/atraso_por_fechas/',views.acreedores_atraso_fechas, name='acreedores_atraso_fechas'),

    
]

urlpatterns+=routers.urlpatterns