# URL
from django.urls import path, include

# Views
from . import views

# FILTROS
from . import filters
# Decorador
from django.contrib.auth.decorators import login_required

# Routes
from apps.customers.api import routers
from .rutas import urlpatterns_asesores_creditos

app_name = 'customers'

urlpatterns = [
    path('', login_required(views.CustomerFiltro.as_view()), name='customers'),
    path('create/', views.add_customer, name='create_customer'),
    path('created/', views.create_customer, name='create'), 
    path('update/<str:customer_code>/', views.update_customer, name='update_customer'),
    path('search/', login_required(views.CustomerSearch.as_view()), name='search'),
    path('delete/<int:id>/',views.delete_customer,name='delete'),
    path('delete_customer/<int:id>/',views.delete_customers,name='delete_customer'),
    path('formulario_ive/<int:id>/', login_required(views.formulario_ive), name='formulario_ive'),
    path('detail/<str:customer_code>/', login_required(views.detail_customer), name='detail'),
    path('recent/', login_required(filters.recent_customer), name='recent'),
    path('solicitude/', login_required(filters.solicitude_customer), name='solicitude'),
    path('not_accepted/', login_required(filters.not_accepted_customer), name='not_accepted'),
    path('accepted/', login_required(filters.accepted_customer), name='accepted'),
    path('inactive/', login_required(filters.inactive_customer), name='inactive'),
    path('document_review/', login_required(filters.document_review_customer), name='document_review'),
    path('clasificacion/',views.list_filters, name='list_filters'),


    
]

urlpatterns+=routers.urlpatterns + urlpatterns_asesores_creditos