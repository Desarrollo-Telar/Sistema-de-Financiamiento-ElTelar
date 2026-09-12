
from datetime import datetime
from django.conf import settings
from django.utils.timezone import now
from django.http import HttpResponse
from django.shortcuts import render
from .send_mail import send_email_user_conect_or_disconect


from django.contrib.auth import logout
from django.utils import timezone

from apps.actividades.models import LogCategory, UserLog


class AutoLogoutMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity_str = request.session.get("last_activity")
            current_time = timezone.now()

            if last_activity_str:
                try:
                    last_activity = datetime.fromisoformat(last_activity_str)
                    elapsed_time = (current_time - last_activity).total_seconds()

                    # Verificar si superó el límite (e.g., 2700 segundos / 45 minutos o SESSION_COOKIE_AGE)
                    if elapsed_time > getattr(
                        settings, "SESSION_COOKIE_AGE", 2700
                    ):
                        user = request.user

                        # 1. Obtener cliente IP y User Agent
                        ip_address = request.META.get(
                            "HTTP_X_FORWARDED_FOR", request.META.get("REMOTE_ADDR")
                        )
                        if ip_address:
                            ip_address = ip_address.split(",")[0].strip()

                        user_agent = request.META.get("HTTP_USER_AGENT", "")[
                            :255
                        ]

                        # 2. Registrar en UserLog antes de cerrar sesión
                        cat_auth, _ = LogCategory.objects.get_or_create(
                            name="Autenticación"
                        )
                        UserLog.objects.create(
                            user=user,
                            action="AUTO_LOGOUT",
                            details=f"Cierre de sesión automático tras {int(elapsed_time // 60)} min de inactividad.",
                            ip_address=ip_address,
                            user_agent=user_agent,
                            category=cat_auth,
                            metadata={
                                "inactividad_segundos": elapsed_time,
                                "limite_configurado": settings.SESSION_COOKIE_AGE,
                            },
                        )

                        # 3. Notificación y Cierre de Sesión
                        send_email_user_conect_or_disconect(
                            user,
                            current_time,
                            "CERRADO SESION AUTOMATICAMENTE, POR FALTA DE ACTIVIDAD",
                        )
                        logout(request)
                        request.session.flush()

                except (ValueError, TypeError):
                    # En caso de error al parsear la fecha, se reinicia la marca
                    pass

            # Actualizar última actividad con la zona horaria correcta
            request.session["last_activity"] = current_time.isoformat()

        response = self.get_response(request)
        return response





class RestrictedAccessByTimeMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        # Obtener rutas exentas desde settings o usar lista por defecto (login, logout, archivos estáticos/media)
        self.exempt_paths = getattr(
            settings,
            "EXEMPT_PATHS",
            [
                "/admin/login/",
                "/logout/",
                "/static/",
                "/media/",
            ],
        )

    def __call__(self, request):
        # Configuración del horario permitido (Default: De 1 AM a 11 PM)
        # HORA_INICIO = 1  (01:00 AM)
        # HORA_FIN = 23    (23:00 PM / 11:00 PM)
        hora_inicio = getattr(settings, "ALLOWED_ACCESS_START_HOUR", 1)
        hora_fin = getattr(settings, "ALLOWED_ACCESS_END_HOUR", 23)

        # 1. Verificar si la ruta actual está exenta (Archivos estáticos, Login, etc.)
        for path in self.exempt_paths:
            if request.path.startswith(path):
                return self.get_response(request)

        # 2. Obtener hora actual con la zona horaria del sistema (evita desfasaje)
        hora_actual = timezone.localtime(timezone.now()).hour

        # 3. Lógica para verificar el horario permitido:
        # Se permite el acceso si la hora actual está entre HORA_INICIO (1) y HORA_FIN (23)
        # Fuera de este rango (es decir, a las 23:00, 00:00 o antes de la 01:00 AM) se deniega.
        permitido = hora_inicio <= hora_actual < hora_fin

        if not permitido:
            # Capturar IP y User Agent para auditoría
            ip_address = request.META.get(
                "HTTP_X_FORWARDED_FOR", request.META.get("REMOTE_ADDR")
            )
            if ip_address:
                ip_address = ip_address.split(",")[0].strip()

            user_agent = request.META.get("HTTP_USER_AGENT", "")[:255]

            # Si el usuario está autenticado, registrar el intento bloqueado en UserLog
            if request.user.is_authenticated:
                cat_seg, _ = LogCategory.objects.get_or_create(
                    name="Seguridad"
                )
                UserLog.objects.create(
                    user=request.user,
                    action="RESTRICTED_TIME_ACCESS",
                    details=f"Intento de acceso denegado por horario fuera de servicio ({hora_actual}:00 hrs) a la ruta: {request.path}",
                    ip_address=ip_address,
                    user_agent=user_agent,
                    category=cat_seg,
                    metadata={
                        "path": request.path,
                        "hora_intento": hora_actual,
                        "horario_permitido": f"{hora_inicio}:00 a {hora_fin}:00",
                    },
                )

            context = {
                "status": 403,
                "mensaje": f"El sistema se encuentra fuera de servicio de 11:00 PM a 01:00 AM. Hora actual: {hora_actual}:00.",
            }
            return render(request, "http/400/403.html", context, status=403)

        return self.get_response(request)

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


from apps.subsidiaries.models import Subsidiary

class SucursalMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        sucursal = None

        user = getattr(request, 'user',None)

        if user and user.is_authenticated:
            sucursal = getattr(user, 'sucursal',None)

        if not sucursal:
            sucursal_id = request.session.get('sucursal_id')
            if sucursal_id:
                sucursal = Subsidiary.objects.get(id=sucursal_id)

        if not sucursal:
            sucursal_id = request.COOKIES.get('sucursal_id')

            if sucursal_id:
                sucursal = Subsidiary.objects.get(id=sucursal_id)
        
        

        request.sucursal_actual = sucursal

        response = self.get_response(request)

        return response