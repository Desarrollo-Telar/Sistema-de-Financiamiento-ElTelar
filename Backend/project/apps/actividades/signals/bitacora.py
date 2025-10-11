# signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.core.signals import request_started, request_finished, got_request_exception
from apps.actividades.models import UserLog, SystemLog, LogLevel, LogCategory

from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    UserLog.objects.create(
        user=user,
        action="LOGIN",
        details=f"Inicio de sesión exitoso",
        ip_address=request.META.get('REMOTE_ADDR'),
        user_agent=request.META.get('HTTP_USER_AGENT'),
        category=LogCategory.objects.get_or_create(name="Autenticación", defaults={'description': 'Eventos de login/logout'})[0]
    )

@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    # Intentamos obtener el usuario si existe
    user = None
    username = credentials.get('username')

    if username:
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            pass

    # Obtener IP y User Agent del request
    ip_address = None
    user_agent = None
    if request is not None:
        ip_address = (
            request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0]
            or request.META.get('REMOTE_ADDR')
        )
        user_agent = request.META.get('HTTP_USER_AGENT', '')

    

    # Crear el registro en UserLog
    UserLog.objects.create(
        user=user,        
        action="LOGIN FAILED",
        details=f"Intento de inicio de sesión fallido con usuario '{username}'",
        ip_address=ip_address,
        user_agent=user_agent,
        category=LogCategory.objects.get_or_create(name="Autenticación", defaults={'description': 'Eventos de login/logout'})[0],
        metadata={
            "username_intentado": username,
        }
    )

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    UserLog.objects.create(
        user=user,
        action="LOGOUT",
        details=f"Cierre de sesión",
        ip_address=request.META.get('REMOTE_ADDR'),
        user_agent=request.META.get('HTTP_USER_AGENT'),
        category=LogCategory.objects.get_or_create(name="Autenticación", defaults={'description': 'Eventos de login/logout'})[0]
    )

@receiver(got_request_exception)
def log_request_exception(sender, request, **kwargs):
    error_level = LogLevel.objects.filter(name='ERROR').first()

    if error_level is None:
        error_level = LogLevel.objects.create(
            name='ERROR',
            description= 'Errores que afectan funcionalidad pero no detienen la aplicación',
            priority=40
        )
    
    SystemLog.objects.create(
        level=error_level,
        source="HTTP Request",
        message=f"Excepción en la solicitud: {request.path}",
        category=LogCategory.objects.get_or_create(
            name="Sistema",
            defaults={'description': 'Eventos del sistema web'}
        )[0],
        traceback=kwargs.get('traceback', 'No disponible')
    )

