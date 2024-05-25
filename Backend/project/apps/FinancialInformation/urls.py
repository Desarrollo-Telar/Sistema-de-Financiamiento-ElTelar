# URL
from django.urls import path, include

# Views
from . import views

# Decorador
from django.contrib.auth.decorators import login_required

# Routes
from apps.FinancialInformation.api import routers

app_name = 'financial_information'

urlpatterns = [
    
]

urlpatterns+=routers.urlpatterns