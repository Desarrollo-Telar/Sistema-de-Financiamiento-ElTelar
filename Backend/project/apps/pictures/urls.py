# PATH
from django.urls import path, include

# API
from apps.pictures.api import routers

app_name = 'imagen'

urlpatterns = [
    
]

urlpatterns += routers.urlpatterns