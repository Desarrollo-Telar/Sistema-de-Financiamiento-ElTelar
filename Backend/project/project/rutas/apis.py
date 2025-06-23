
# VISTAS 
from rest_framework.authtoken import views as v_iews
from project.views import actualizacion_test_api, list_api
from rest_framework.documentation import include_docs_urls
from django.contrib.auth import views as auth_views

# DECORADOR
from django.contrib.auth.decorators import login_required

# URLS
from django.urls import path, include

urlpatterns_api = [
    # ------------- API ---------------------------
    path('api/',list_api,name='list_api'),
    path('api/patch/',actualizacion_test_api,name='actualizacion_test_api'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token-auth/', v_iews.obtain_auth_token),
    path('docs/', include_docs_urls(title='Documentacion de la API - EL TELAR', public=False)),
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name='user/autentication/password-reset.html',email_template_name='user/autentication/password-message.html'),name='password_reset'),
    path('reset_password_send/',auth_views.PasswordResetDoneView.as_view(template_name='user/autentication/password-confirmation1.html'),name='password_reset_done'),
    path('reset_password/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name='user/autentication/password_reset_confirm.html'),name='password_reset_confirm'),    
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='user/autentication/password-confirmation2.html'),name='password_reset_complete'),
]