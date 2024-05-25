# PATH
from django.urls import path

# API
from rest_framework import routers
router = routers.DefaultRouter()

urlpatterns = [
    path('api/', include(router.urls)),
]