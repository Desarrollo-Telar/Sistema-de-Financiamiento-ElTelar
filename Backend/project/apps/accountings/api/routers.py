# PATH
from django.urls import path, include

# API
from rest_framework import routers

# VIEWS
from . import views

router = routers.DefaultRouter()
router.register(r'acreedores_vigentes',views.AcreedoresVigentesViewSet, 'acreedores_vigentes')
router.register(r'seguros_vigentes',views.SegurosVigentesViewSet, 'seguros_vigentes')
urlpatterns = [
    path('api/', include(router.urls)),
]