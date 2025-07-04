# PATH
from django.urls import path, include

# API
from apps.pictures.api import routers

# Decorador
from django.contrib.auth.decorators import login_required

# VIEWS
from . import views

app_name = 'imagen'

urlpatterns = [
    path('create_image/<str:customer_code>/', views.create_imagen_customer, name='create_image'),
    path('create_image/address/<int:address_id>/<str:customer_code>/', views.create_imagen_customer_address, name='create_image_address'),
    path('create_image/guarantee/<int:investment_plan_id>/<str:customer_code>/', views.create_imagen_customer_guarantee, name='create_image_guarantee'),
    path('delete_image/<int:id>/<str:customer_code>/',views.delete_imagen, name='delete_image'),
    path('update_image/<int:id>/<str:customer_code>/',views.update_imagen, name='update_image'),

    
]

urlpatterns += routers.urlpatterns