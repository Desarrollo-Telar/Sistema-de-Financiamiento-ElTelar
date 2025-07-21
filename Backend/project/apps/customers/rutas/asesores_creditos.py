# URL
from django.urls import path, include

# vistas
from apps.customers import views

# Decorador
from django.contrib.auth.decorators import login_required


urlpatterns_asesores_creditos = [
    path('asesores_credito/',login_required( views.AsesoresCreditosList.as_view()), name='asesores_creditos'),
    path('asesores_credito/detail/<str:codigo_asesor>/',login_required( views.detail_asesor), name='detail_asesor'),

]