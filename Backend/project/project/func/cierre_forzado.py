import os
import django

# Configura el entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django.utils import timezone

def sesiones_activas_usuario(username):
    User = get_user_model()
    try:
        usuario = User.objects.get(username=username)

    except User.DoesNotExist:
        print(f"El usuario '{username}' no existe.")
        return 0


    # Cuenta solo las sesiones del usuario que aún no han expirado
    sesiones_activas = 0
    for s in Session.objects.filter(expire_date__gte=timezone.now()):
        data = s.get_decoded()
        if data.get("_auth_user_id") == str(usuario.pk):
            sesiones_activas += 1

    print(f"Sesiones de {username} realmente activas: {sesiones_activas}")

def forzar_logout_usuario(username):
    User = get_user_model()

    try:
        usuario = User.objects.get(username=username)
    except User.DoesNotExist:
        print(f"El usuario '{username}' no existe.")
        return 0

    sesiones_eliminadas = 0

    # Recorremos todas las sesiones activas en la base de datos
    for sesion in Session.objects.all():
        datos_sesion = sesion.get_decoded()

        # Comprobamos si el ID del usuario coincide con el de la sesión
        if str(usuario.pk) == str(datos_sesion.get("_auth_user_id")):
            sesion.delete()
            sesiones_eliminadas += 1

    print(
        f"Se cerraron {sesiones_eliminadas} sesión(es) para el usuario '{username}'."
    )
    return sesiones_eliminadas


if __name__ == "__main__":
    # Ejemplo de uso
    from apps.users.models import User
    for username_a_cerrar in User.objects.values_list('username', flat=True):
        sesiones_activas_usuario(username_a_cerrar)