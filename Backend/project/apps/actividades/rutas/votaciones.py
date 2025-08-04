
# PATH
from django.urls import path, include

# VIEWS
from apps.actividades import views

urlpatterns_votaciones = [
    path('votacion/cliente/<str:customer_code>/',views.votar_cliente, name='votar_cliente'),
    
]