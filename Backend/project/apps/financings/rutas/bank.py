# VISTAS
from apps.financings.views import *

# PATH
from django.urls import path, include

# DECORADOR
from django.contrib.auth.decorators import login_required

urlpatterns_bank = [
    # ---------------- BANCOS --------------------
    path('bank/',login_required(list_bank),name='list_bank'),
    path('bank/vinculado/',login_required(filter_list_bank_vinculado),name='filter_list_bank_vinculado'),
    path('bank/no_viculado/',login_required(filter_list_bank_no_vinculado),name='filter_list_bank_no_vinculado'),
    path('bank/search/',login_required(BankSearch.as_view()),name='bank_search'),
]