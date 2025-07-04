# PATH
from django.urls import path, include

# API
from rest_framework import routers

# VIEWS
from . import views

router = routers.DefaultRouter()
router.register(r'notificaciones', views.NotificationViewSet,'notificaciones')

urlpatterns = [
    path('api/', include(router.urls)),
]