# URL
from django.urls import path, include

# Views
from . import views

# Decorador
from django.contrib.auth.decorators import login_required

app_name = 'users'

urlpatterns = [
    path('', login_required(views.list_user), name='users'),
    path('user_profile/', login_required(views.profile), name='profile'),
    path('create_user/', login_required(views.userCreateView.as_view()), name='create'),
]
