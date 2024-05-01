
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('correo_prueba/', views.prueba, name='prueba'),
    path('admin/', admin.site.urls),
]
