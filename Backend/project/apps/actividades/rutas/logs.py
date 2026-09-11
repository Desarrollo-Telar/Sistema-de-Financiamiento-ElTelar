
# PATH
from django.urls import path, include

# VIEWS
from apps.actividades import views

# Decorador
from django.contrib.auth.decorators import login_required

urlpatterns_logs = [
    path('logs/sistema/', login_required(views.listando_logs), name='list_logs'),
    path('logs/usuario/', login_required(views.listando_user_logs), name='list_user_logs'),
    
    
]