
from django.contrib import admin
from django.urls import path, include

# Vistas
from . import views
from apps.actividades.views  import subida_documento

from django.contrib.auth import views as auth_views
from . import generate_pdf



# CONFIGURANCION PARA MANEJAR LOS STATICS Y MEDIA
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.decorators import login_required



from django.conf.urls import handler404, handler500, handler400, handler403
from .http import request_400

from django.core.mail import send_mail
from django.conf import settings

from django.urls import re_path
from django.views.static import serve
from django.conf import settings

# RUTAS
from .rutas import urlpatterns_apps, urlpatterns_api, urlpatterns_reports


urlpatterns = [    
    path('',login_required(views.index),name='index'),
    path('accounts/login/',views.login_view, name='login'),
    path('verification/', views.verification, name='verification'),
    path('logout/',views.logout_view, name='logout'),
    path('admin/', admin.site.urls),
    path('search/', login_required(views.Search.as_view()), name='busqueda_general'),
    path('qr/<str:data>/', views.generate_qr, name='generate_qr'),
    path('pdf/<int:id>', generate_pdf.generar_pdf, name='pdf'),
    path('cliente/<str:uuid>/', subida_documento, name='subida_documento_cliente'),

    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:    
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += urlpatterns_apps + urlpatterns_api + urlpatterns_reports

#template_name='user/autentication/password-reset.html'
#email_template_name='user/autentication/password-message.html'

handler404 = request_400.error404
