
import datetime
from django.conf import settings
from django.utils.timezone import now
from django.http import HttpResponse

class AutoLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Si el usuario está autenticado
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')

            # Si hay actividad previa
            if last_activity:
                elapsed_time = (now() - last_activity).total_seconds()
                
                # Si el tiempo de inactividad excede el límite
                if elapsed_time > settings.SESSION_COOKIE_AGE:
                    from django.contrib.auth import logout
                    logout(request)
                    request.session.flush()  # Opcional: elimina toda la sesión
                
            # Actualiza el tiempo de la última actividad
            request.session['last_activity'] = now()

        response = self.get_response(request)
        return response






class RestrictedAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Definir el horario de acceso permitido (en 24 horas)
        hora_inicio = settings.ALLOWED_ACCESS_START_HOUR  # Hora de inicio de acceso permitido
        hora_fin = settings.ALLOWED_ACCESS_END_HOUR  # Hora de fin de acceso permitido

        # Obtener la hora actual
        hora_actual = datetime.now().hour

        # Verificar si la hora actual está fuera del horario permitido
        if not (hora_inicio <= hora_actual < hora_fin):
            return HttpResponse("<h1>Sistema fuera de servicio. Intente nuevamente en el horario permitido.</h1>", status=403)

        # Si está dentro del horario, continúa con la solicitud
        response = self.get_response(request)
        return response
