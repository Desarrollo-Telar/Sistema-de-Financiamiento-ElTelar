# PATH
from django.urls import path, include

# API
from rest_framework import routers

# VIEWS
from . import views

router = routers.DefaultRouter()
router.register(r'customers', views.CustomerViewSet, 'clientes')
router.register(r'customers_accept', views.CustomerAcceptViewSet, 'clientes_aceptados')
router.register(r'immigration_status', views.ImmigrationStatusViewSet, 'codicion_migratoria')
router.register(r'asesores',views.CreditCounselorSerializerViewSet,'asesores_creditos')
router.register(r'cobranza',views.CobranzaViewSet,'cobranza')
urlpatterns = [
    path('api/', include(router.urls)),
]