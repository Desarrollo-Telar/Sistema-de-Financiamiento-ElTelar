
# PATH
from django.urls import path, include

# VIEWS
from apps.actividades import views

# Decorador
from django.contrib.auth.decorators import login_required

urlpatterns_logs = [
    path('logs/', login_required(views.listando_logs), name='list_logs'),
    
    
    
    
]