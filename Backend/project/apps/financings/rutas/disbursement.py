# VISTAS
from apps.financings.views import *

# PATH
from django.urls import path, include

# DECORADOR
from django.contrib.auth.decorators import login_required

urlpatterns_disbursement = [
   # ---------------- DESEMBOLSO ------------
    path('disbursement/create/<int:id>/',login_required(create_disbursement),name='create_disbursement'),  
    path('disbursement/',login_required(DesembolsoList.as_view()), name='list_disbursement'),
    path('disbursement/<int:id>/',login_required(detallar_desembolso), name='detail_disbursement'),
]