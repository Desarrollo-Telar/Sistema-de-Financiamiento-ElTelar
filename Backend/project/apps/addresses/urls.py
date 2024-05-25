# URL
from django.urls import path, include

# VIEWS
from . import views

#API
from apps.addresses.api import routers

app_name = 'addresses'

urlpatterns = [
    
]

urlpatterns+=routers.urlpatterns