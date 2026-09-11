import os
import django

# Configura el entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session


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
        forzar_logout_usuario(username_a_cerrar)