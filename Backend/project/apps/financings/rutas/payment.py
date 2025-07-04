# VISTAS
from apps.financings.views import *

# PATH
from django.urls import path, include

# DECORADOR
from django.contrib.auth.decorators import login_required

urlpatterns_payment = [
    # -------------- BOLETAS ---------------------
    path('payment/',login_required(list_payment),name='list_payment'),
    path('payment/pendiente/',login_required(filter_list_payment_pendiente),name='filter_list_payment_pendiente'),
    path('payment/completado/',login_required(filter_list_payment_completados),name='filter_list_payment_completados'),
    path('payment/create/',login_required(create_payment),name='create_payment'),
    path('payment/create/<int:id>/',login_required(create_payment_credit),name='create_payment_credit'),
    path('payment/update/<int:id>/',login_required(update_pago),name='actualizar_boleta'),
    path('payment/detail/<int:id>/',login_required(detalle_boleta),name='detalle_boleta'),
    path('payment/search/',login_required(PaymentSearch.as_view()),name='payment_search'),
    path('payment/cuota/update/<int:id>/',login_required(update_cuota), name='paymente_update_cuota'),
]