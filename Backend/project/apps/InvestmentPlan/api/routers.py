# PATH
from django.urls import path, include

# API
from rest_framework import routers

# VIEWS
from . import views

router = routers.DefaultRouter()

urlpatterns = [
    path('api/', include(router.urls)),
]