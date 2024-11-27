# PATH
from django.urls import path, include

# API
from rest_framework import routers

# VIEWS
from . import views

router = routers.DefaultRouter()
router.register(r'credit',views.CreditViewSet,'credit')
router.register(r'garantia',views.GuaranteesViewSet,'guarantee')
router.register(r'detalle_garantia',views.DetailsGuaranteesViewSet,'detail_guarantee')
router.register(r'desembolso',views.DisbursementViewSet,'disbursement')
router.register(r'payment',views.PaymentViewSet,'payment')
router.register(r'factura',views.FacturaViewSet,'factura')
router.register(r'recibo',views.ReciboViewSet,'recibo')
router.register(r'cuota',views.PaymentPlanUltimoViewSet,'cuota')
router.register(r'cuotas',views.PaymentPlanViewSet,'cuotas')
urlpatterns = [
    path('api/', include(router.urls)),
]