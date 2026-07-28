
from apps.users.models import PermisoUsuario

def recorrer_los_permisos_usuario(request):
    permisos_tiene = {}
    es_autenticado = request.user.is_authenticated

    if not es_autenticado:
        return None

    for permisos_otorgados in PermisoUsuario.objects.filter(user=request.user):
        nombre = permisos_otorgados.permiso.codigo_permiso
        permisos_tiene[f'{nombre}'] = True
    
    return permisos_tiene