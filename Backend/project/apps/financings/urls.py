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
    path('credit/create',login_required(views.create_credit),name='create_credit'),
    path('disbursement/create',login_required(views.create_disbursement),name='create_disbursement'),
    path('guarantee/create',login_required(views.create_guarantee),name='create_guarantee'),
    path('credit/',login_required(views.list_credit), name='list_credit'),
    path('credit/<int:id>/',login_required(views.detail_credit), name='detail_credit'),
    path('guarantee/',login_required(views.list_guarantee), name='list_guarantee'),
    path('disbursement/',login_required(views.list_disbursement), name='list_disbursement'),
    path('bank/',login_required(views.list_bank),name='list_bank'),
]

urlpatterns+=routers.urlpatterns