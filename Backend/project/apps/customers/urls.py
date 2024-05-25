# URL
from django.urls import path, include

# Views
from . import views

# Decorador
from django.contrib.auth.decorators import login_required

# Routes
from apps.customers.api import routers

app_name = 'customers'

urlpatterns = [
    path('', views.list_customer, name='customers'),
    path('create/', views.add_customer, name='create'),
]

urlpatterns+=routers.urlpatterns