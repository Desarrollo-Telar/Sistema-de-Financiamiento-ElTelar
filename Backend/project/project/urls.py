
from django.contrib import admin
from django.urls import path, include

# Vistas
from . import views
from django.contrib.auth import views as auth_views
from . import generate_pdf



# CONFIGURANCION PARA MANEJAR LOS STATICS Y MEDIA
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.decorators import login_required
from rest_framework.documentation import include_docs_urls

from django.conf.urls import handler404, handler500, handler400, handler403
from .http import request_400

from django.core.mail import send_mail
from django.conf import settings

from django.urls import re_path
from django.views.static import serve
from django.conf import settings

urlpatterns = [    
    path('',login_required(views.index),name='index'),
    path('accounts/login/',views.login_view, name='login'),
    path('verification/', views.verification, name='verification'),
    path('logout/',views.logout_view, name='logout'),
    path('admin/', admin.site.urls),
    path('users/', include('apps.users.urls')),
    path('search/', login_required(views.Search.as_view()), name='busqueda_general'),
    path('roles&permissions/', include('apps.roles.urls')),
    #path('prueba/', views.prueba, name='prueba'),
    path('customers/', include('apps.customers.urls')),
    path('addresses/', include('apps.addresses.urls')),
    path('codes/', include('apps.codes.urls')),
    path('financial_information/', include('apps.FinancialInformation.urls')),
    path('plan_inversion/', include('apps.InvestmentPlan.urls')),
    path('imagen/', include('apps.pictures.urls')),
    path('documents/', include('apps.documents.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('docs/', include_docs_urls(title='Documentacion de la API - EL TELAR', public=False)),
    path('test/', views.test, name='test'),
    path('qr/<str:data>/', views.generate_qr, name='generate_qr'),
    #path('pdf/<int:id>',login_required(views.render_pdf_view), name='pdf'),
    path('pdf/<int:id>', login_required(generate_pdf.generar_pdf), name='pdf'),
    path('financings/',include('apps.financings.urls')),
    path('api/',views.list_api,name='list_api'),
    
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name='user/autentication/password-reset.html',email_template_name='user/autentication/password-message.html'),name='password_reset'),
    path('reset_password_send/',auth_views.PasswordResetDoneView.as_view(template_name='user/autentication/password-confirmation1.html'),name='password_reset_done'),
    path('reset_password/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name='user/autentication/password_reset_confirm.html'),name='password_reset_confirm'),    
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='user/autentication/password-confirmation2.html'),name='password_reset_complete'),
    #path('dashboard/', include('django_dash.urls')),
    
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:    
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#template_name='user/autentication/password-reset.html'
#email_template_name='user/autentication/password-message.html'

handler400 = request_400.error400
handler403 = request_400.error403
handler404 = request_400.error404