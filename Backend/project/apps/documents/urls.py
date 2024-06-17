# PATH
from django.urls import path, include

# API
from apps.pictures.api import routers

app_name = 'document'

urlpatterns = [
    
]

urlpatterns += routers.urlpatterns