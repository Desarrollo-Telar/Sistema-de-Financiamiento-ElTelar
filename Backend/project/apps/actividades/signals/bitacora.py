# signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.core.signals import request_started, request_finished, got_request_exception
from apps.actividades.models import UserLog, SystemLog, LogLevel, LogCategory

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
    UserLog.objects.create(
        user=None,
        action="LOGIN_FAILED",
        details=f"Intento de inicio de sesión fallido para usuario: {credentials.get('username', '')}",
        ip_address=request.META.get('REMOTE_ADDR'),
        user_agent=request.META.get('HTTP_USER_AGENT'),
        category=LogCategory.objects.get_or_create(name="Autenticación", defaults={'description': 'Eventos de login/logout'})[0]
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
    error_level = LogLevel.objects.get_or_create(
        name="ERROR",
        defaults={'description': 'Errores del sistema', 'priority': 3}
    )[0]
    
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

