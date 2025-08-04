
# PATH
from django.urls import path, include

# VIEWS
from apps.actividades import views

urlpatterns_votaciones = [
    path('votacion/cliente/<str:customer_code>/',views.votar_cliente, name='votar_cliente'),
    path('votacion/credito/<int:id>/',views.votar_credito, name='votar_credito'),
    
]