# URL
from django.urls import path, include

# Views
from . import views

# Decorador
from django.contrib.auth.decorators import login_required

app_name = 'roles_permissions'

urlpatterns = [
    path('', login_required(views.role_permission), name='roles_permissions'),
]