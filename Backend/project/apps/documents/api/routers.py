# PATH
from django.urls import path, include

# API
from rest_framework import routers

# VIEWS
from . import views

router = routers.DefaultRouter()
router.register(r'documento',views.DocumentViewSet, 'documento')
router.register(r'documento_direccion',views.DocumentAddressViewSet, 'documento_direccion')
router.register(r'documento_cliente',views.DocumentCustomerViewSet, 'documento_cliente')
router.register(r'otro_documento',views.DocumentOtherViewSet, 'otro_documento')
router.register(r'documento_garantia',views.DocumentGuaranteeViewSet, 'documento_garantia')

urlpatterns = [
    path('api/', include(router.urls)),
]