# PATH
from django.urls import path, include

# API
from apps.InvestmentPlan.api import routers

app_name = 'investment_plan'

urlpatterns = [

]

urlpatterns += routers.urlpatterns