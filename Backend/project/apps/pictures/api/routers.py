# PATH
from django.urls import path, include

# API
from rest_framework import routers

# VIEWS
from . import views

router = routers.DefaultRouter()
router.register(r'imagen',views.ImagenViewSet, 'imagen')
router.register(r'imagen_cliente', views.ImagenCustomerViewSet, 'imagen_cliente')
router.register(r'imagen_direccion', views.ImagenAddressViewSet, 'imagen_direccion')

urlpatterns = [
    path('api/', include(router.urls)),
]