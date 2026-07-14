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
router.register(r'tipo_gasto', views.TipoGastoViewSet, 'tipo_gasto')
router.register(r'gasto_cliente', views.GastoClienteViewSet, 'gasto_cliente')

urlpatterns = [
    path('api/', include(router.urls)),
]