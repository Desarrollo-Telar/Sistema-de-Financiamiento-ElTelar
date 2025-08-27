# PATH
from django.urls import path, include

# API
from rest_framework import routers

# VIEWS
from . import views

router = routers.DefaultRouter()
router.register(r'notificaciones', views.NotificationViewSet,'notificaciones')
router.register(r'detalle_informe_cobranza', views.DetalleInformeCobranzaViewSet, 'detalle_informe_cobranza')
router.register(r'porcentajes-cobranza',views.DetalleInformeCobranzaPorcentajesViewSet,'porcentajes-cobranza')

urlpatterns = [
    path('api/', include(router.urls)),
]