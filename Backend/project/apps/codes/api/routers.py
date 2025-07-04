# PATH
from django.urls import path, include

# API
from rest_framework import routers

# VIEWS
from . import views

router = routers.DefaultRouter()
router.register(r'codes',views.CodeViewSet,'codigos')

urlpatterns = [
    path('api/', include(router.urls)),
]