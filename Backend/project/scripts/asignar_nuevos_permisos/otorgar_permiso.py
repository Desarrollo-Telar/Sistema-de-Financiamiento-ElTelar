
# Modelos
from apps.roles.models import Permiso, Role
from apps.users.models import PermisoUsuario, User



def asignar():
    roles = ['Programador', 'Administrador', 'Secretari@']
    #roles = ['Programador', 'Administrador', 'Asesor de Crédito']
    # puede_crear_registro_cobranza
    # puede_ver_registros_cobranza hay que crear el registro de este permiso
    
    usuarios = User.objects.filter(rol__role_name__in = roles )
    permiso_a_otorgar = Permiso.objects.get(codigo_permiso='puede_emitir_facturas')
    #permiso_a_otorgar = Permiso.objects.get_or_create(codigo_permiso='puede_ver_facturas', )
    #  puede_ver_facturas

    for usuario in usuarios:
        print(usuario)
        otorgar_permiso_usuario = PermisoUsuario.objects.create(
            user = usuario,
            permiso = permiso_a_otorgar
        )

        print(otorgar_permiso_usuario)