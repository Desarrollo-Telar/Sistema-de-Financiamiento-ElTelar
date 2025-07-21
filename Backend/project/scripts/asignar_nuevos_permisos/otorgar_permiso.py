
# Modelos
from apps.roles.models import Permiso, Role
from apps.users.models import PermisoUsuario, User



def asignar():
    #roles = ['Programador', 'Administrador', 'Secretari@']
    roles = ['Programador', 'Administrador']
    
    usuarios = User.objects.filter(rol__role_name__in = roles )
    permiso_a_otorgar = Permiso.objects.get(codigo_permiso='puede_visualizar_detalle_asesor_credito')

    for usuario in usuarios:
        print(usuario)
        otorgar_permiso_usuario = PermisoUsuario.objects.create(
            user = usuario,
            permiso = permiso_a_otorgar
        )

        print(otorgar_permiso_usuario)