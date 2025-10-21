
from functools import wraps

# REDIRECT
from django.contrib.auth import logout
from django.shortcuts import redirect

# htpp
from django.http import HttpResponseNotFound, HttpResponseForbidden

# MODELOS
from apps.roles.models import  Permiso
from apps.users.models import PermisoUsuario

# Manejo de mensajes
from django.contrib import messages

def permiso_requerido(nombre_permiso):
    """
    Decorador que verifica si el usuario tiene un permiso específico.
    """
    def decorador(vista_funcion):
        @wraps(vista_funcion)
        def envoltura(request, *args, **kwargs):
            usuario = request.user
            

            # Asegura que sea un usuario autenticado
            if not usuario.is_authenticated:
                return redirect('login')
            
            # Asegurar que el usuario este vigente en la plataforma
            if not usuario.status:
                logout(request)
                return redirect('login')
            
            
            sucursal = request.session['sucursal_id']

            if sucursal is None:
                return redirect('sucursal:clasificacion')
            
            if usuario.sucursal is not None:             
                request.session['sucursal_id'] = usuario.sucursal.id

            
            

            # Verifica si tiene el permiso
            tiene_permiso = PermisoUsuario.objects.filter(
                user=usuario,
                permiso__codigo_permiso=nombre_permiso,
                permiso__estado=True
            ).exists()

            if tiene_permiso:
                return vista_funcion(request, *args, **kwargs)
            else:
                messages.error(request, 'Tu perfil de usuario no tiene los privilegios necesarios para realizar esta operación')
                return redirect('index')
        return envoltura
    return decorador

