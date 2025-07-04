# PATH
from django.urls import path, include

# API
from rest_framework import routers

# VIEWS
from . import views

router = routers.DefaultRouter()
router.register(r'working_information', views.WorkingInformationViewSet, 'working_information')
router.register(r'other_sources', views.OtherSourcesOfIncomeViewSet, 'other_sources')
router.register(r'reference', views.ReferenceViewSet, 'reference')

urlpatterns = [
    path('api/', include(router.urls)),
]