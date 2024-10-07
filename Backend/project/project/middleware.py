
from datetime import datetime
from django.conf import settings
from django.utils.timezone import now
from django.http import HttpResponse
from django.shortcuts import render

class AutoLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Si el usuario está autenticado
        if request.user.is_authenticated:
            last_activity_str = request.session.get('last_activity')

            # Si hay actividad previa
            if last_activity_str:
                # Convertir la cadena de last_activity a un objeto datetime
                last_activity = datetime.fromisoformat(last_activity_str)
                elapsed_time = (now() - last_activity).total_seconds()
                
                # Si el tiempo de inactividad excede el límite
                if elapsed_time > settings.SESSION_COOKIE_AGE:
                    from django.contrib.auth import logout
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
                'title': 'EL TELAR'
            }
            return render(request, 'http/400/403.html', context)

        # Si está dentro del horario, continúa con la solicitud
        response = self.get_response(request)
        return response
