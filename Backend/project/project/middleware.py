
from datetime import datetime
from django.conf import settings
from django.utils.timezone import now
from django.http import HttpResponse
from django.shortcuts import render
from .send_mail import send_email_user_conect_or_disconect

class AutoLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Si el usuario está autenticado
        if request.user.is_authenticated:
            last_activity_str = request.session.get('last_activity')
            user = request.user
            hora = datetime.now()

            # Si hay actividad previa
            if last_activity_str:
                # Convertir la cadena de last_activity a un objeto datetime
                last_activity = datetime.fromisoformat(last_activity_str)
                elapsed_time = (now() - last_activity).total_seconds()
                
                # Si el tiempo de inactividad excede el límite
                if elapsed_time > settings.SESSION_COOKIE_AGE:
                    from django.contrib.auth import logout
                    send_email_user_conect_or_disconect(user,hora,'CERRADO SESION AUTOMATICAMENTE, POR FALTA DE ACTIVIDAD')
                    logout(request)
                    
                    request.session.flush()  # Opcional: elimina toda la sesión
                
            # Actualiza el tiempo de la última actividad (almacena como cadena ISO)
            request.session['last_activity'] = now().isoformat()

        response = self.get_response(request)
        return response





from apps.financings.task import cambiar_plan

class RestrictedAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_paths = settings.EXEMPT_PATHS  # Lista de rutas permitidas

    def __call__(self, request):
        # Definir el horario de acceso permitido
        hora_inicio = settings.ALLOWED_ACCESS_START_HOUR
        hora_fin = settings.ALLOWED_ACCESS_END_HOUR

        # Obtener la hora actual
        hora_actual = datetime.now().hour

        # Verificar si la URL de la solicitud está en la lista de rutas exentas
        for path in self.exempt_paths:
            if request.path.startswith(path):
                return self.get_response(request)

        # Verificar si la hora actual está fuera del horario permitido
        if not (hora_inicio <= hora_actual < hora_fin):
            context = {
                'status': 403,
                
            }
            return render(request, 'http/400/403.html', context, status=403)

        # Si está dentro del horario, continúa con la solicitud
        response = self.get_response(request)
        return response

# middleware.py
from django.utils.deprecation import MiddlewareMixin
from apps.actividades.models import UserLog

class UserActionLoggingMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        # Solo registrar acciones para usuarios autenticados
        if request.user.is_authenticated and request.method in ['POST', 'PUT', 'DELETE']:
            action_map = {
                'POST': 'CREACIÓN',
                'PUT': 'ACTUALIZACIÓN',
                'DELETE': 'ELIMINACIÓN'
            }
            
            action = action_map.get(request.method)
            if action:
                UserLog.objects.create(
                    user=request.user,
                    action=action,
                    details=f"{action} en {request.path}",
                    ip_address=request.META.get('REMOTE_ADDR'),
                    user_agent=request.META.get('HTTP_USER_AGENT'),
                    metadata={
                        'view': view_func.__name__,
                        'args': view_args,
                        'kwargs': view_kwargs
                    }
                )