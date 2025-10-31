
# VISTAS 
from rest_framework.authtoken import views as v_iews
from rest_framework.documentation import include_docs_urls
from django.contrib.auth import views as auth_views
from project.view_api import view
from project.views import GenerarMensajePagoAPIView, GenerandoMensajeSaldoApi

# DECORADOR
from django.contrib.auth.decorators import login_required

# URLS
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# vistas
from project.view_api.view import CustomTokenObtainPairView, LogoutView

urlpatterns_api = [
    # ------------- API ---------------------------
    path('api/token/login/',view.CustomAuthToken.as_view(), name='login_api'), # TOKEN

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login JWT
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh token

    path('api/login/', CustomTokenObtainPairView.as_view(), name='login_api'), # Login JWT
    path('api/logout/', LogoutView.as_view(), name='logout_api'), # LOGOUT JWT

    
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token-auth/', v_iews.obtain_auth_token),

    # ------------ PARA MANDAR MENSAJES----- 
    path('api/generar-mensaje/<str:customer_code>/<str:cuota_id>/', GenerarMensajePagoAPIView.as_view(), name='generar-mensaje-pago'),
    path('api/generar-mensaje-saldo_actual/<str:credito>/', GenerandoMensajeSaldoApi.as_view(), name='mensaje_saldo_actual'),
    # ----------- DOCUMENTACION DE API -----------
    path('docs/', include_docs_urls(title='Documentacion de la API - EL TELAR', public=False)),

    # ---------------- SE ME OLVIDO LA CONTRASEÑa ------------------------
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name='user/autentication/password-reset.html',email_template_name='user/autentication/password-message.html'),name='password_reset'),
    path('reset_password_send/',auth_views.PasswordResetDoneView.as_view(template_name='user/autentication/password-confirmation1.html'),name='password_reset_done'),
    path('reset_password/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name='user/autentication/password_reset_confirm.html'),name='password_reset_confirm'),    
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='user/autentication/password-confirmation2.html'),name='password_reset_complete'),
]