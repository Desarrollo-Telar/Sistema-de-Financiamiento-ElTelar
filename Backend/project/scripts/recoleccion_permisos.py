
from apps.users.models import PermisoUsuario

def recorrer_los_permisos_usuario(request):
   

    if not request.user.is_authenticated:
        return {
            'permisos_usuario': {}
        }

    permisos = {
        codigo: True
        for codigo in PermisoUsuario.objects.filter(
            user=request.user
        ).values_list(
            'permiso__codigo_permiso',
            flat=True
        )
    }

    return permisos