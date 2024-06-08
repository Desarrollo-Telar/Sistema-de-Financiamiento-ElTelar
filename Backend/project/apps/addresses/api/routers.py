# PATH
from django.urls import path, include

# API
from rest_framework import routers

# VIEWS
from . import views
router = routers.DefaultRouter()
router.register(r'address', views.AddressViewSet,'direccion')
router.register(r'coordinate', views.CoordinateViewSet,'coordinate')
urlpatterns = [
    path('api/', include(router.urls)),
]