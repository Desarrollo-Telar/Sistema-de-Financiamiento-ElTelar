# PATH
from django.urls import path, include

# API
from apps.financings.api import routers

# Decorador
from django.contrib.auth.decorators import login_required

# VIEWS
from . import views

app_name = 'financings'

urlpatterns = [
    # -------------- CREDITO -----------
    path('credit/',login_required(views.list_credit), name='list_credit'),
    path('credit/<int:id>/',login_required(views.detail_credit), name='detail_credit'),
    path('credit/create',login_required(views.create_credit),name='create_credit'),

    # ---------------- GARANTIA ------------
    path('guarantee/',login_required(views.list_guarantee), name='list_guarantee'),
    path('guarantee/create',login_required(views.create_guarantee),name='create_guarantee'),

    # ---------------- DESEMBOLSO ------------
    path('disbursement/create',login_required(views.create_disbursement),name='create_disbursement'),  
    path('disbursement/',login_required(views.list_disbursement), name='list_disbursement'),
    path('disbursement/<int:id>/',login_required(views.detallar_desembolso), name='detail_disbursement'),

    # --------------- RECIBO ------------------
    path('recibo/<int:id>/',login_required(views.detallar_recibo), name='recibo'),
    
    # -------------- BOLETAS ---------------------
    path('payment/',login_required(views.list_payment),name='list_payment'),
    path('payment/create/',login_required(views.create_payment),name='create_payment'),
    path('payment/update/<int:id>/',login_required(views.update_pago),name='actualizar_boleta'),
    path('payment/detail/<int:id>/',login_required(views.detalle_boleta),name='detalle_boleta'),
    path('payment/search/',login_required(views.PaymentSearch.as_view()),name='payment_search'),

    # ---------------- BANCOS --------------------
    path('bank/',login_required(views.list_bank),name='list_bank'),
    path('bank/search/',login_required(views.BankSearch.as_view()),name='bank_search'),
]

urlpatterns+=routers.urlpatterns