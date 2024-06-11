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
    path('search/', login_required(views.CustomerSearch.as_view()), name='search'),
    path('delete/<int:id>/',views.delete_customer,name='delete'),
    path('formulario_ive/<int:id>/', login_required(views.formulario_ive), name='formulario_ive'),
    path('detail/<str:customer_code>/', login_required(views.detail_customer), name='detail'),
]

urlpatterns+=routers.urlpatterns