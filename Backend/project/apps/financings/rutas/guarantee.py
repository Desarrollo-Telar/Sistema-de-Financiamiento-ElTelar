# VISTAS
from apps.financings.views import *

# PATH
from django.urls import path, include

# DECORADOR
from django.contrib.auth.decorators import login_required

urlpatterns_guarantee = [
    # ---------------- GARANTIA ------------
    path('guarantee/',login_required(list_guarantee), name='list_guarantee'),
    path('guarantee/create/',login_required(create_guarantee),name='create_guarantee'),
    path('guarantee/detail/<int:id>/',login_required(detallar_garantia),name='detallar_garantia'),
]