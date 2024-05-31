
from django.contrib import admin
from django.urls import path, include
# Vistas
from . import views

# CONFIGURANCION PARA MANEJAR LOS STATICS Y MEDIA
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.decorators import login_required
from rest_framework.documentation import include_docs_urls
urlpatterns = [
    
    path('',login_required(views.index),name='index'),
    path('accounts/login/',views.login_view, name='login'),
    path('verification/', views.verification, name='verification'),
    path('logout/',views.logout_view, name='logout'),
    path('admin/', admin.site.urls),
    path('users/', include('apps.users.urls')),
    path('roles&permissions/', include('apps.roles.urls')),
    path('prueba/', views.prueba, name='prueba'),
    path('customers/', include('apps.customers.urls')),
    path('addresses/', include('apps.addresses.urls')),
    path('codes/', include('apps.codes.urls')),
    path('financial_information/', include('apps.FinancialInformation.urls')),
    path('plan_inversion/', include('apps.InvestmentPlan.urls')),
    path('imagen/', include('apps.pictures.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('docs/', include_docs_urls(title='Documentacion de la API - EL TELAR', public=False)),
    #path('dashboard/', include('django_dash.urls')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:    
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
