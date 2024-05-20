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
    path('update_user/<int:pk>/', login_required(views.userUpdateView.as_view()), name='update'),
    path('change_password/', login_required(views.ChangePassword.as_view()), name='update_password'),
]
