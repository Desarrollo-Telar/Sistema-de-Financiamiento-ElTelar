# PATH
from django.urls import path, include

# API
from apps.documents.api import routers

# Views
from . import views

# Decorador
from django.contrib.auth.decorators import login_required

app_name = 'document'

urlpatterns = [
    path('create_document/customer/<str:customer_code>/',views.create_document_customer,name='create_document_customer'),
    path('create_document/financings/guarantee/<int:id>/',views.create_documente_detalle_garantia,name='create_documente_detalle_garantia'),
    path('create_document/address/<int:addrress_id>/<str:customer_code>/',views.create_documente_address,name='create_document_address'),
    path('create_document/guarantee/<int:investment_plan_id>/<str:customer_code>/', views.create_documente_guarantee, name='create_document_guarantee'),
    path('delete_document/<int:id>/<str:customer_code>/',views.delete,name='delete_document'),
    path('update_document/<int:id>/<str:customer_code>/',views.update_document,name='update_document'),
    path('create/',views.subir_banco,name='banco'),
]

urlpatterns += routers.urlpatterns