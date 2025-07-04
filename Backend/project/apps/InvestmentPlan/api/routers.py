# PATH
from django.urls import path, include

# API
from rest_framework import routers

# VIEWS
from . import views

router = routers.DefaultRouter()
router.register(r'plan_inversion', views.InvestmentPlanViewSet, 'plan_inversion')

urlpatterns = [
    path('api/', include(router.urls)),
]