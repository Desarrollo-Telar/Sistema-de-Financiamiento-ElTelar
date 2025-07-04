# PATH
from django.urls import path, include

# API
from rest_framework import routers

# VIEWS
from . import views
router = routers.DefaultRouter()
router.register(r'address', views.AddressViewSet,'direccion')
router.register(r'departamento', views.DepartamentoViewSet,'departamento')
router.register(r'municipio', views.MunicipioViewSet,'municipio')
urlpatterns = [
    path('api/', include(router.urls)),
]