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
    path('credit/',login_required(views.list_credit), name='list_credit'),
    
]

urlpatterns+=routers.urlpatterns