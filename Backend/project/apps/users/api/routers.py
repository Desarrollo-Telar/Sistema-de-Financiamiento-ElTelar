# PATH
from django.urls import path, include

# API
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView
# VIEWS
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, 'users')

urlpatterns = [
    path('api/', include(router.urls)),
]