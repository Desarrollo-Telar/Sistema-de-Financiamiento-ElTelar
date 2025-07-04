
# PATH
from django.urls import path, include

# VIEWS
from apps.actividades import views

urlpatterns_notificaciones = [
    path('notification/',views.listar_notificaciones, name='notification'),
    path('notification/<str:uuid>/',views.detalle_notificacion, name='detalle_notificacion'),
    path('cerrar_pestania/', views.cerrar_pestana, name='cerrar_pestania'),
]