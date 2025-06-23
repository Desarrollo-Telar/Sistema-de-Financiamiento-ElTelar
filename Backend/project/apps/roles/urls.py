# URL
from django.urls import path, include

# Views
from . import views

# Decorador
from django.contrib.auth.decorators import login_required

# API
from apps.roles.api import routers

app_name = 'roles_permissions'

urlpatterns = [
    
]

urlpatterns += routers.urlpatterns