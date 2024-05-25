# URL
from django.urls import path, include

# VIEWS
from . import views

#API
from apps.codes.api import routers

app_name = 'codes'

urlpatterns = [

]

urlpatterns+= routers.urlpatterns