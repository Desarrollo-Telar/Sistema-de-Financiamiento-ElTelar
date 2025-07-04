# PATH
from django.urls import path, include

# API
from apps.InvestmentPlan.api import routers

# Decorador
from django.contrib.auth.decorators import login_required

# VIEWS
from . import views

app_name = 'investment_plan'

urlpatterns = [
    path('create/<str:customer_code>/',views.create_plan_financiamiento, name='create' ),
    path('delete/<int:id>/<str:customer_code>/',views.delete_plan_financiamiento,name='delete'),
    path('update/<int:id>/<str:customer_code>/',views.update_plan_financiamiento, name='update')

]

urlpatterns += routers.urlpatterns