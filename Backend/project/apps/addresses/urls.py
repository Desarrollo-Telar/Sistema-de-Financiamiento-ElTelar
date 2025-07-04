# URL
from django.urls import path, include

# VIEWS
from . import views

#API
from apps.addresses.api import routers

# Decorador
from django.contrib.auth.decorators import login_required

app_name = 'addresses'

urlpatterns = [
    path('add/<str:customer_code>/', login_required( views.AddressCreateView.as_view()), name = 'add'),
    path('update/<int:id>/<str:customer_code>/', login_required(views.addressUpdateView), name = 'update'),
    path('municipio/crear/',login_required(views.crear_municipio),name='crear_municipio'),
]

urlpatterns+=routers.urlpatterns