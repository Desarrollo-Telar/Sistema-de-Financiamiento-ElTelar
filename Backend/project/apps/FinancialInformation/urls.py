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
    path('delete/other_information/<int:id>/<str:customer_code>/',views.delete_other_information, name='delete_other_information'),
    path('delete/working_information/<int:id>/<str:customer_code>/',views.delete_working_information,name='delete_working_information'),
    path('create/working_information/<str:customer_code>/',views.create_working_information, name='create_working_information'),
    path('create/other_information/<str:customer_code>/',views.create_other_information, name='create_other_information'),
    path('create/reference/<str:customer_code>/',views.create_references_customer, name='create_reference_information'),
    path('update/other_information/<int:id>/<str:customer_code>/', views.update_other_information, name='update_other_information'),
    path('update/working_information/<int:id>/<str:customer_code>/',views.update_working_information,name='update_working_information'),
    path('update/reference/<int:id>/<str:customer_code>/',views.update_references_customer,name='update_reference'),
    path('seleccionar/<str:codigo>/<str:customer_code>/', views.seleccionar, name='seleccionar'),
]

urlpatterns+=routers.urlpatterns